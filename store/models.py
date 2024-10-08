from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    order_history = models.TextField(blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='store_user_groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='store_user_permissions',
        blank=True
    )


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover_art = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    download_link = models.URLField(max_length=400)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Ebook(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover_art = models.ImageField(upload_to='ebooks/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    download_link = models.URLField(max_length=400)

    def __str__(self):
        return self.title


    # Accessory model
class Accessory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Book Wraps as a subcategory of Accessories
class BookWrap(models.Model):
    accessory = models.OneToOneField(Accessory, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Book Wrap - {self.accessory.name}"


# Bookmark as a subcategory of Accessories
class Bookmark(models.Model):
    accessory = models.OneToOneField(Accessory, on_delete=models.CASCADE)
    design = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Bookmark - {self.accessory.name}"

    # School and Office Supplies model
class SchoolOffice(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    # Booklets/Folders as a subcategory of School and Office
class BookletFolder(models.Model):
    school_office = models.OneToOneField(SchoolOffice, on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Booklet/Folder - {self.school_office.name}"


    # Pencils as a subcategory of School and Office
class Pencil(models.Model):
    school_office = models.OneToOneField(SchoolOffice, on_delete=models.CASCADE)
    pencil_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Pencil - {self.school_office.name}"


    # Other supplies as a subcategory of School and Office
class Other(models.Model):
    school_office = models.OneToOneField(SchoolOffice, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Other - {self.school_office.name}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, blank=True, null=True)
    ebook = models.ForeignKey('Ebook', on_delete=models.CASCADE, blank=True, null=True)
    rating = models.IntegerField()
    review_text = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review on {self.book or self.ebook}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE, blank=True, null=True)
    book_wrap = models.ForeignKey(BookWrap, on_delete=models.CASCADE, blank=True, null=True)
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE, blank=True, null=True)
    pencil = models.ForeignKey(Pencil, on_delete=models.CASCADE, blank=True, null=True)
    other = models.ForeignKey(Other, on_delete=models.CASCADE, blank=True, null=True)
    booklet_folder = models.ForeignKey(BookletFolder, on_delete=models.CASCADE, blank=True, null=True)
    fav_rating = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.book or self.ebook or self.book_wrap or self.bookmark or self.pencil or self.other or self.booklet_folder}"



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE, blank=True, null=True)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, blank=True, null=True)
    pencil = models.ForeignKey(Pencil, on_delete=models.CASCADE, blank=True, null=True)
    other = models.ForeignKey(Other, on_delete=models.CASCADE, blank=True, null=True)
    book_wrap = models.ForeignKey(BookWrap, on_delete=models.CASCADE, blank=True, null=True)
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE, blank=True, null=True)
    booklet_folder = models.ForeignKey(BookletFolder, on_delete=models.CASCADE, blank=True, null=True)
    school_office = models.ForeignKey(SchoolOffice, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    # Add fields for all item types
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE, blank=True, null=True)
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, blank=True, null=True)
    pencil = models.ForeignKey(Pencil, on_delete=models.CASCADE, blank=True, null=True)
    other = models.ForeignKey(Other, on_delete=models.CASCADE, blank=True, null=True)
    book_wrap = models.ForeignKey(BookWrap, on_delete=models.CASCADE, blank=True, null=True)
    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE, blank=True, null=True)
    booklet_folder = models.ForeignKey(BookletFolder, on_delete=models.CASCADE, blank=True, null=True)
    school_office = models.ForeignKey(SchoolOffice, on_delete=models.CASCADE, blank=True, null=True)
    delivery_method = models.CharField(max_length=100,
                                       choices=[('parcel_machine', 'Parcel Machine'), ('post_office', 'Post Office'),
                                                ('courier', 'Courier'), ('pickup', 'Pick up by Yourself')], null=True,
                                       blank=True)
    parcel_machine_location = models.CharField(max_length=255, blank=True, null=True)
    post_office_location = models.CharField(max_length=255, blank=True, null=True)
    home_address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')
    payment_method = models.CharField(max_length=50, blank=False, null=False)
    payment_status = models.CharField(max_length=50)
    delivery_email = models.CharField(max_length=255)
    email_sent_date = models.DateTimeField(null=True, blank=True)
    download_link = models.CharField(max_length=255, null=True, blank=True)
    download_expiry_date = models.DateTimeField(null=True, blank=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.book.title} - {self.order.user.username}'



