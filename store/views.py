import logging
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import Book, Ebook, Accessory, BookWrap, Bookmark, SchoolOffice, BookletFolder, Pencil, Other, Cart, Order, Favorite, Review
from django import forms
from .models import Review
from .forms import ReviewForm



User = get_user_model()


def home(request):
    cart_items_count = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    return render(request, 'store/home.html', {'cart_items_count': cart_items_count})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = Review.objects.filter(book=book)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            messages.success(request, 'Your review has been added.')
            return redirect('book_detail', book_id=book.id)
    else:
        form = ReviewForm()

    return render(request, 'store/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'form': form
    })

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'store/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'store/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'store/register.html')

        # Create the user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password1)  # Hash the password manually
        )

        # Log the user in after registration (optional)
        login(request, user)

        messages.success(request, f'Account created for {user.username}!')
        return redirect('home')

    return render(request, 'store/register.html')


@login_required
def add_to_cart(request, item_type, item_id):
    # Fetch the item based on the item_type
    item_model_mapping = {
        "book": Book,
        "ebook": Ebook,
        "accessory": Accessory,
        "pencil": Pencil,
        "other": Other,
        "book_wrap": BookWrap,
        "bookmark": Bookmark,
        "booklet_folder": BookletFolder,
        "school_office": SchoolOffice
    }

    item_model = item_model_mapping.get(item_type)
    if not item_model:
        messages.error(request, "Invalid item type.")
        return redirect('home')

    item = item_model.objects.filter(id=item_id).first()

    if item:
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            **{f'{item_type}': item}
        )
        item_price = item.price
        if created:
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1
        cart_item.total_cost = cart_item.quantity * item_price
        cart_item.save()
    else:
        messages.error(request, "Item not found.")
        return redirect('home')

    return redirect('view_cart')


@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'store/cart.html', {'cart_items': cart_items})


logger = logging.getLogger(__name__)


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')


# Define a form for delivery options
class DeliveryForm(forms.Form):
    DELIVERY_CHOICES = [
        ('parcel_machine', 'Parcel Machine'),
        ('post_office', 'Pick up at the Post Office'),
        ('courier', 'Home Delivery by Courier'),
        ('self_pickup', 'Pick up by Yourself'),
    ]
    delivery_option = forms.ChoiceField(choices=DELIVERY_CHOICES, widget=forms.RadioSelect)
    delivery_address = forms.CharField(max_length=255, required=False)


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    total_price = sum(
        (item.book.price if item.book else 0) +
        (item.ebook.price if item.ebook else 0) +
        (item.accessory.price if item.accessory else 0) +
        (item.pencil.price if item.pencil else 0) +
        (item.other.price if item.other else 0) +
        (item.book_wrap.price if item.book_wrap else 0) +
        (item.bookmark.price if item.bookmark else 0) +
        (item.booklet_folder.price if item.booklet_folder else 0) +
        (item.school_office.price if item.school_office else 0)
        for item in cart_items
    )

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        delivery_email = request.POST.get('email')

        if not payment_method:
            return render(request, 'store/checkout.html', {
                'cart_items': cart_items,
                'total_price': total_price,
                'error_message': 'Please select a payment method.'
            })

        for item in cart_items:
            order_data = {
                'user': request.user,
                'price': item.total_cost / item.quantity,
                'quantity': item.quantity,
                'total_cost': item.total_cost,
                'status': 'Pending',
                'payment_method': payment_method,
                'payment_status': 'Unpaid',
                'delivery_email': delivery_email,
            }

            if item.book:
                order_data['book'] = item.book
            elif item.ebook:
                order_data['ebook'] = item.ebook
            elif item.accessory:
                order_data['accessory'] = item.accessory
            elif item.pencil:
                order_data['pencil'] = item.pencil
            elif item.other:
                order_data['other'] = item.other
            elif item.book_wrap:
                order_data['book_wrap'] = item.book_wrap
            elif item.bookmark:
                order_data['bookmark'] = item.bookmark
            elif item.booklet_folder:
                order_data['booklet_folder'] = item.booklet_folder
            elif item.school_office:
                order_data['school_office'] = item.school_office

            # Create the Order
            Order.objects.create(**order_data)

        cart_items.delete()  # Clear the cart after order creation
        return redirect('order_success')

    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total_price': total_price})




@login_required
def order_success(request):
    # Fetch recent orders for the user
    orders = Order.objects.filter(user=request.user).order_by('-order_date')[:5]

    # Check if the order contains ebooks or other downloadable items
    for order in orders:
        if order.ebook:
            order.download_link = order.ebook.download_link  # eBooks have a download link
        # If you have other downloadable items (e.g., audiobooks), add them here

    return render(request, 'store/order_success.html', {'orders': orders})

@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        rating = request.POST['rating']
        review_text = request.POST['review_text']

        Review.objects.create(
            user=request.user,
            book=book,
            rating=rating,
            review_text=review_text
        )
        messages.success(request, 'Your review has been added.')
        return redirect('book_detail', book_id=book_id)

    return render(request, 'store/add_review.html', {'book': book})


@login_required
def view_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'store/reviews.html', {'reviews': reviews})


@login_required
def update_cart_quantity(request, item_id, operation):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)

    # Handle the quantity increase/decrease
    if operation == 'increase':
        cart_item.quantity += 1
    elif operation == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    elif operation == 'decrease' and cart_item.quantity == 1:
        # If quantity reaches 0, remove the item
        cart_item.delete()
        return redirect('view_cart')

    # Update the total cost based on the item type
    if cart_item.book:
        cart_item.total_cost = cart_item.quantity * cart_item.book.price
    elif cart_item.ebook:
        cart_item.total_cost = cart_item.quantity * cart_item.ebook.price
    elif cart_item.accessory:
        cart_item.total_cost = cart_item.quantity * cart_item.accessory.price
    elif cart_item.pencil:
        cart_item.total_cost = cart_item.quantity * cart_item.pencil.price
    elif cart_item.other:
        cart_item.total_cost = cart_item.quantity * cart_item.other.price
    elif cart_item.book_wrap:
        cart_item.total_cost = cart_item.quantity * cart_item.book_wrap.price
    elif cart_item.exlibris:
        cart_item.total_cost = cart_item.quantity * cart_item.exlibris.price
    elif cart_item.booklet_folder:
        cart_item.total_cost = cart_item.quantity * cart_item.booklet_folder.price
    elif cart_item.school_office:
        cart_item.total_cost = cart_item.quantity * cart_item.school_office.price
    else:
        cart_item.total_cost = 0  # Set a default value or handle the error

    cart_item.save()
    return redirect('view_cart')


def search(request):
    query = request.GET.get('q', '')

    if query:
        # Fetching books, ebooks, and other items based on query
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
        ebooks = Ebook.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
        accessories = Accessory.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        book_wraps = BookWrap.objects.filter(
            Q(accessory__name__icontains=query) |
            Q(color__icontains=query)
        )
        booklets_folders = BookletFolder.objects.filter(
            Q(school_office__name__icontains=query) |
            Q(size__icontains=query)
        )
        bookmarks = Bookmark.objects.filter(
            Q(accessory__name__icontains=query) |
            Q(design__icontains=query)
        )
        pencils = Pencil.objects.filter(
            Q(school_office__name__icontains=query) |
            Q(pencil_type__icontains=query)
        )
        school_and_office = SchoolOffice.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

        # Combine results from all item types into one list
        items = list(books) + list(ebooks) + list(accessories) + list(book_wraps) + \
                list(school_and_office) + list(bookmarks) + list(pencils) + list(booklets_folders)
    else:
        items = []

    return render(request, 'store/search_results.html', {'items': items})


def about_us(request):
    return render(request, 'store/about_us.html')


def contact_us(request):
    return render(request, 'store/contact_us.html')


def terms_and_conditions(request):
    return render(request, 'store/terms_and_conditions.html')


def shipping_information(request):
    return render(request, 'store/shipping_information.html')


def books(request):
    return render(request, 'store/books.html')


def ebooks(request):
    return render(request, 'store/ebooks.html')


def accessories(request):
    return render(request, 'store/accessories.html')


def book_wraps(request):
    book_wraps = BookWrap.objects.all()  # Fetch all book wraps
    return render(request, 'store/book_wraps.html', {'book_wraps': book_wraps})


def bookmarks(request):
    bookmarks = Bookmark.objects.all()  # Fetch all bookmarks
    return render(request, 'store/bookmarks.html', {'bookmarks': bookmarks})


def school_and_office(request):
    return render(request, 'store/school_and_office.html')


def booklets_folders(request):
    booklets_folders = BookletFolder.objects.all()  # Fetch all booklets/folders
    return render(request, 'store/booklets_folders.html', {'booklets_folders': booklets_folders})


def pencils(request):
    pencils = Pencil.objects.all()  # Fetch all pencils
    return render(request, 'store/pencils.html', {'pencils': pencils})



def other(request):
    other_items = Other.objects.all()  # Fetch all "Other" products
    return render(request, 'store/other.html', {'other_items': other_items})



def books_view(request):
    books = Book.objects.all()  # Fetch all books from the database
    return render(request, 'store/books.html', {'books': books})


# View for E-books page
def ebooks_view(request):
    ebooks = Ebook.objects.all()  # Fetch all e-books
    return render(request, 'store/ebooks.html', {'ebooks': ebooks})


def ebook_detail(request, ebook_id):
    ebook = get_object_or_404(Ebook, id=ebook_id)
    reviews = Review.objects.filter(ebook=ebook)
    form = ReviewForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.ebook = ebook
        review.save()
        return redirect('ebook_detail', ebook_id=ebook_id)

    return render(request, 'store/ebook_details.html', {
        'ebook': ebook,
        'reviews': reviews,
        'form': form,
    })


@login_required
def add_to_favorites(request, item_type, item_id):
    # Fetch item based on type
    item = None
    if item_type == 'book':
        item = Book.objects.get(id=item_id)
    elif item_type == 'ebook':
        item = Ebook.objects.get(id=item_id)
    elif item_type == 'book_wrap':
        item = BookWrap.objects.get(id=item_id)
    elif item_type == 'bookmark':
        item = Bookmark.objects.get(id=item_id)
    elif item_type == 'pencil':
        item = Pencil.objects.get(id=item_id)
    elif item_type == 'other':
        item = Other.objects.get(id=item_id)
    elif item_type == 'booklet_folder':
        item = BookletFolder.objects.get(id=item_id)

    if item:
        # Add item to user's favorites
        favorite, created = Favorite.objects.get_or_create(user=request.user, **{f'{item_type}': item})
        if created:
            messages.success(request, f"{getattr(item, 'title', getattr(item, 'name', 'Item'))} has been added to your favorites!")
        else:
            messages.info(request, f"{getattr(item, 'title', getattr(item, 'name', 'Item'))} is already in your favorites.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def view_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'store/favorites.html', {'favorites': favorites})

@login_required
def remove_from_favorites(request, favorite_id):
    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    favorite.delete()
    messages.success(request, 'Item removed from favorites.')
    return redirect('view_favorites')