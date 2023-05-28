from django.urls import path
from .views import *


urlpatterns = [
    path('', BjjHome.as_view(), name='index'),
    path('home/', BjjHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('gallery/', Gallery.as_view(), name='gallery'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('contacts/', Contacts.as_view(), name='contacts'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('post/<slug:post_slug>/', PostDetail.as_view(), name='post_detail'),
    path('add_comment/<int:news_id>/', add_comment, name='add_comment'),
    # path('add_comment/<slug:post_slug>/', AddComment.as_view(), name='add_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('add_reaction/<int:news_id>/', add_reaction, name='add_reaction'),
    path('delete_reaction/delete/<int:reaction_id>/', delete_reaction, name='delete_reaction'),
    path('photo/<slug:photo_slug>/', photo_detail, name='photo_detail'),
    path('add_comment_photo/<int:photo_id>/', add_comment_photo, name='add_comment_photo'),
    path('delete_comment_photo/<int:comment_id>/', delete_comment_photo, name='delete_comment_photo'),
]
