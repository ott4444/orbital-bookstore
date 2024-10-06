from django import template
from store.models import Book, Ebook, Accessory, BookWrap, Bookmark, SchoolOffice, BookletFolder, Pencil, Other

register = template.Library()

@register.filter
def is_book(item):
    return isinstance(item, Book)

@register.filter
def is_ebook(item):
    return isinstance(item, Ebook)

@register.filter
def is_accessory(item):
    return isinstance(item, Accessory)

@register.filter
def is_book_wrap(item):
    return isinstance(item, BookWrap)

@register.filter
def is_bookmark(item):
    return isinstance(item, Bookmark)

@register.filter
def is_booklet_folder(item):
    return isinstance(item, BookletFolder)

@register.filter
def is_pencil(item):
    return isinstance(item, Pencil)

@register.filter
def is_school_office(item):
    return isinstance(item, SchoolOffice)

@register.filter
def is_other(item):
    return isinstance(item, Other)
