from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('home/', index, name='home'),
    path('about/', about, name='about'),
    path('gallery/', gallery, name='gallery'),
    path('schedule/', schedule, name='schedule'),
    path('contacts/', contacts, name='contacts'),
    path('login/', login, name='login'),
    path('post/<slug:post_slug>/', post_detail, name='post_detail'),
    path('add_comment/<int:news_id>/', add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('add_reaction/<int:news_id>/', add_reaction, name='add_reaction')
]
