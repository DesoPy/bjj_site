from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CommentForm, ReactionForm
from .models import *


menu = [{'title': 'Головна', 'url_name': 'home'},
        {'title': 'Галерея', 'url_name': 'gallery'},
        {'title': 'Розклад тренувань', 'url_name': 'schedule'},
        {'title': 'Про нас', 'url_name': 'about'},
        {'title': 'Контакти', 'url_name': 'contacts'},
        {'title': 'Реєстрація/Увійти', 'url_name': 'login'},
        ]


def index(request):
    post = News.objects.prefetch_related('comments', 'reactions').all()
    context = {'post': post,
               'menu': menu,
               'title': 'Yamasaki Academy Jiu Jitsu Dnipro',
               'reactions': NewsReaction.REACTION_CHOICES}
    return render(request, 'bjj_app/index.html', context=context)


def add_comment(request, news_id):
    post = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'bjj_app/addcomment.html', {'form': form, 'menu': menu})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
    return redirect('index')


@login_required
def add_reaction(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = ReactionForm(request.POST)
        if form.is_valid():
            # Отримання обраної реакції з форми
            reaction_type = form.cleaned_data['reaction_type']
            # Створення нового екземпляру NewsReaction з отриманою реакцією та іншими полями
            reaction = NewsReaction.objects.create(
                reaction_type=reaction_type,
                news=news,
                author=request.user
            )
            # Додавання реакції до новини
            news.reactions.add(reaction)
            messages.success(request, "Reaction added successfully.")
            return redirect('news_detail', slug=news.slug)

    form = ReactionForm()
    context = {'form': form, 'menu': menu, 'reactions': NewsReaction.REACTION_CHOICES, 'news': news}
    return render(request, 'bjj_app/news_detail.html', context)


def gallery(request):
    return render(request, 'bjj_app/gallery.html', {'menu': menu, 'title': 'Gallery'})


def schedule(request):
    return render(request, 'bjj_app/schedule.html', {'menu': menu, 'title': 'Schedule'})


def about(request):
    return render(request, 'bjj_app/about.html', {'menu': menu, 'title': 'About us'})


def contacts(request):
    return render(request, 'bjj_app/contacts.html', {'menu': menu, 'title': 'Contacts'})


def login(request):
    return render(request, 'bjj_app/contacts.html', {'menu': menu, 'title': 'Login'})


def post_detail(request, post_slug):
    # post = News.objects.prefetch_related('comments', 'reactions').get(pk=pk)
    post = get_object_or_404(News, slug=post_slug)
    context = {
        'post': post,
        'menu': menu,
        'title': post.title
    }
    return render(request, 'bjj_app/post_detail.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('Page not found')
