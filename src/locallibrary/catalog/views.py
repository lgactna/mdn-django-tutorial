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
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    #if, perhaps, you wanted to list five books with war
    #context_object_name = 'my_book_list'   # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    #template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    
    #this caps the max books shown at once on the All Books page to a number
    #additional pages are done with GET query strings, e.g., /catalog/books/?page=2
    paginate_by = 1

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    #we could paginate here but i dont have enough authors

class AuthorDetailView(generic.DetailView):
    model = Author