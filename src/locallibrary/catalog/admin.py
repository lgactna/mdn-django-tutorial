from django.contrib import admin

# Register your models here.

from .models import Author, Genre, Book, BookInstance

#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)

# Fields and fieldsets change the appearance of the admin form to modify and add the below classes/fields
# Defining `fields` change the layout; items in tuples are placed on the same line, with all elements placed vertically
# Similarly, fieldsets put a large header above the involved items

#This allows us to have an inline editor of the author's books while editing an Author
class BookInline(admin.TabularInline):
    extra = 0
    model = Book

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

#This allows us to have an inline editor of the book instances while also editing a book
class BooksInstanceInline(admin.TabularInline):
    extra = 0
    model = BookInstance

# Register the Admin classes for Book using the decorator
# note that the decorator method is functionally identical to the above definitions
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'language')
    inlines = [BooksInstanceInline]

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )