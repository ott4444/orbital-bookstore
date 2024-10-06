from django.contrib import admin
from .models import User, Category, Subcategory, Book, Review, Favorite, Cart, Order
from .models import Ebook, Accessory, BookWrap, Bookmark, SchoolOffice, BookletFolder, Pencil, Other

# Register each model in the admin interface

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_admin', 'is_active')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'availability', 'category', 'subcategory')
    search_fields = ('title', 'author')
    list_filter = ('category', 'subcategory', 'availability')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'fav_rating')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'quantity', 'total_cost', 'created_at')
    list_filter = ('user',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'total_cost', 'status', 'payment_method', 'payment_status')
    list_filter = ('status', 'payment_method', 'payment_status')



# Admin for Ebooks
@admin.register(Ebook)
class EbookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'availability')
    search_fields = ('title', 'author')

# Admin for Accessories
@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'availability')
    search_fields = ('name',)

# Admin for Book Wraps
@admin.register(BookWrap)
class BookWrapAdmin(admin.ModelAdmin):
    list_display = ('accessory', 'color')

# Admin for Bookmark
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('accessory', 'design')

# Admin for School and Office Supplies
@admin.register(SchoolOffice)
class SchoolOfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'availability')
    search_fields = ('name',)

# Admin for Booklets/Folders
@admin.register(BookletFolder)
class BookletFolderAdmin(admin.ModelAdmin):
    list_display = ('school_office', 'size')

# Admin for Pencils
@admin.register(Pencil)
class PencilAdmin(admin.ModelAdmin):
    list_display = ('school_office', 'pencil_type')

# Admin for Other Supplies
@admin.register(Other)
class OtherSupplyAdmin(admin.ModelAdmin):
    list_display = ('school_office', 'description')

