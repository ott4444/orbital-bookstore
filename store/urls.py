from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('add-to-cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/logout.html'), name='logout'),
    path('add-to-favorites/<str:item_type>/<int:item_id>/', views.add_to_favorites,name='add_to_favorites'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('favorites/remove/<int:favorite_id>/', views.remove_from_favorites,name='remove_from_favorites'),
    path('reviews/', views.view_reviews, name='view_reviews'),
    path('add-review/<int:book_id>/', views.add_review, name='add_review'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update_quantity/<int:item_id>/<str:operation>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('search/', views.search, name='search'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('shipping-information/', views.shipping_information, name='shipping_information'),
    path('books/', views.books_view, name='books'),
    path('ebooks/', views.ebooks_view, name='ebooks'),
    path('accessories/', views.accessories, name='accessories'),
    path('accessories/book-wraps/', views.book_wraps, name='book_wraps'),
    path('accessories/bookmarks/', views.bookmarks, name='bookmarks'),
    path('school-and-office/', views.school_and_office, name='school_and_office'),
    path('school-and-office/booklets-folders/', views.booklets_folders, name='booklets_folders'),
    path('school-and-office/pencils/', views.pencils, name='pencils'),
    path('school-and-office/other/', views.other, name='other'),
    path('ebook/<int:ebook_id>/', views.ebook_detail, name='ebook_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

