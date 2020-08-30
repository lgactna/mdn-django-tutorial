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



from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    #This has exactly the same redirect behaviour as the login_required decorator.
    #You can also specify an alternative location to redirect the user to if they are not authenticated (login_url),
    # and a URL parameter name instead of "next" to insert the current absolute path (redirect_field_name).
    #there is no need to do that here since ridirecting to /login is already desired
    '''
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    '''
    
    #apart from pagination restricting the returned count to 10
    #here we filter the results returned by borrower, then by those with a status of on loan
    #then we sort by the due back date
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

#this mixin allows us to restrict views to those with specific permissions
#(note that admins/superusers are treated as having ALL permissions)
#decorators can be used as well, though this can be at the cost of some flexibility
#for example, changing a view based on individual permissions; then additional views would need to be
#declared
from django.contrib.auth.mixins import PermissionRequiredMixin

#orignally this inherited LoginRequiredMixin as well...
#but that broke the page and always routed to a 403
class BorrowedBooksListView(PermissionRequiredMixin,LoginRequiredMixin,generic.ListView):
    #notice how there is no explicit redirect to login.html if lacking permissions
    #see https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication#Login_template
    #if the user is logged in but lacking permissions, it will throw 403 forbidden at them
    #see https://docs.djangoproject.com/en/3.1/ref/views/ for what happens
    permission_required = 'catalog.can_mark_returned'
    #again, not needed
    '''
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    '''
   
    model = BookInstance
    template_name ='catalog/borrowed_books_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

