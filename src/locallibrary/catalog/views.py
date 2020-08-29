from django.shortcuts import render

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # here we create a filter of titles that contain the case insensitive word "China"
    # this is done with the field `title` and using __icontains as the filter
    # see https://docs.djangoproject.com/en/3.1/topics/db/queries/
    num_books_from_china = Book.objects.filter(title__icontains='China').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_from_china': num_books_from_china
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)