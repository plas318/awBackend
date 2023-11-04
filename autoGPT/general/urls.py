from django.urls import path
from .views import RegisterView, LoginView, LogoutView, PostView, PostRetrieveUpdateDestroyView, CategoryView, TagView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('posts/', PostView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post_retrieve_update_destroy'),
    path('categories/', CategoryView.as_view(), name='category_list_create'),
    path('tags/', TagView.as_view(), name='tag_list_create')
]