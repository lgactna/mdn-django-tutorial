from django.urls import path
from . import views

# how does book_list.html get rendered?

# Note: This awkward path for the template location isn't a misprint — the generic views look for templates in 
# /application_name/the_model_name_list.html (catalog/book_list.html in this case) inside the application's 
# /application_name/templates/ directory (/catalog/templates/).

# our model name is called BookListView; thus, to camel_case, book_list(_view).


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [   
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('allbooks/', views.BorrowedBooksListView.as_view(), name='all-borrowed')
]