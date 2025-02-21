from django.urls import path
from . import views

app_name = 'LocalLibrary'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorView.as_view(), name='authors'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('loans/', views.BooksOnLoanListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),

]

urlpatterns += [
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
]

urlpatterns += [
    path('book/create', views.BookCreateView.as_view(), name='book-create'),
    path('book/<int:pk>/update', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete', views.BookDeleteView.as_view(), name='book-delete'),
]