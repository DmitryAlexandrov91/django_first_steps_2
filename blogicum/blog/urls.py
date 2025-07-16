from django.urls import path

from blog.views import (
    IndexListView,
    PostCreateView,
    PostDetailView,
    PostEditView,
    PostDeleteView,
    CategoryView,
    ProfileDetailView,
    ProfileUpdateView,
    CommentCreateView,
    CommentEditView,
    CommentDeleteView)


app_name = 'blog'

urlpatterns = [
    path('',
         IndexListView.as_view(),
         name='index'),
    path('posts/create/',
         PostCreateView.as_view(),
         name='create_post'),
    path('posts/<int:post_id>/',
         PostDetailView.as_view(),
         name='post_detail'),
    path('posts/<int:post_id>/edit/',
         PostEditView.as_view(),
         name='edit_post'),
    path('posts/<int:post_id>/delete/',
         PostDeleteView.as_view(),
         name='delete_post'),
    path('category/<slug:category_slug>/',
         CategoryView.as_view(),
         name='category_posts'),
    path('profile/edit/',
         ProfileUpdateView.as_view(),
         name='edit_profile'),
    path('profile/<slug:username>/',
         ProfileDetailView.as_view(),
         name='profile'),
    path('posts/<int:post_id>/comment/',
         CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         CommentEditView.as_view(),
         name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         CommentDeleteView.as_view(),
         name='delete_comment')
]
