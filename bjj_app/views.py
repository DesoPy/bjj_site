from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView


from .forms import *
from .utils import *


class BjjHome(DataMixin, ListView):
    model = News
    template_name = 'bjj_app/index.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Yamasaki Academy Jiu Jitsu Dnipro')
        context['reaction_choices'] = NewsReaction.REACTION_CHOICES
        return dict(list(context.items()) + list(c_def.items()))


# @login_required(login_url='login')
# class AddComment(LoginRequiredMixin, DataMixin, CreateView):
#     form_class = CommentForm
#     template_name = 'bjj_app/addcomment.html'
#     success_url = reverse_lazy('home')
#     login_url = reverse_lazy('home')
#     raise_exception = True
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Yamasaki Academy Jiu Jitsu Dnipro')
#         return dict(list(context.items()) + list(c_def.items()))


@login_required(login_url='login')
def add_comment(request, news_id):
    post = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = post
            comment.author = request.user
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()

    return render(request, 'bjj_app/addcomment.html', {'form': form, 'menu': menu, 'title': 'Add comment'})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
    return redirect('index')


def add_reaction(request, news_id):
    post = get_object_or_404(News, id=news_id)
    form = NewsReactionForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            try:
                existing_reaction = NewsReaction.objects.get(news=post, author=request.user)
                existing_reaction.reaction_type = form.cleaned_data['reaction_type']
                existing_reaction.save()
            except ObjectDoesNotExist:
                reaction = form.save(commit=False)
                reaction.news = post
                reaction.author = request.user
                reaction.save()
            return redirect('index')

    else:
        form = NewsReactionForm()

    try:
        existing_reaction = NewsReaction.objects.get(news=post, author=request.user)
        reaction_type = existing_reaction.reaction_type
    except ObjectDoesNotExist:
        reaction_type = None

    context = {
        'post': post,
        'reaction_form': form,
        'existing_reaction_type': reaction_type
    }
    return render(request, 'bjj_app/index.html', context=context)


@login_required
def delete_reaction(request, reaction_id):
    reaction = get_object_or_404(NewsReaction, id=reaction_id)
    if request.method == 'POST':
        if reaction.author.id == request.user.id or request.user.is_staff:
            reaction.delete()

    return redirect('index')


class Gallery(DataMixin, ListView):
    model = Photo
    template_name = 'bjj_app/gallery.html'
    context_object_name = 'photo'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Gallery')
        return dict(list(context.items()) + list(c_def.items()))


@login_required(login_url='login')
def add_comment_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if request.method == 'POST':
        form = CommentPhotoForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.author = request.user
            comment.save()
            return redirect('gallery')

    else:
        form = CommentForm()

    return render(request, 'bjj_app/addcomment.html', {'form': form, 'menu': menu})


@login_required
def delete_comment_photo(request, comment_id):
    comment = get_object_or_404(CommentPhoto, id=comment_id)
    if request.user == comment.author:
        comment.delete()
    return redirect('gallery')


class ScheduleView(DataMixin, ListView):
    model = Schedule
    template_name = 'bjj_app/schedule.html'
    context_object_name = 'schedule'
    paginate_by = 25

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Schedule')
        return dict(list(context.items()) + list(c_def.items()))


def about(request):
    return render(request, 'bjj_app/about.html', {'menu': menu, 'title': 'About us'})


class Contacts(DataMixin, ListView):
    model = Trainer
    template_name = 'bjj_app/contacts.html'
    context_object_name = 'trainer'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Contacts')
        return dict(list(context.items()) + list(c_def.items()))


# class PhotoDetail(DataMixin, ListView):
#     model = Photo
#     template_name = 'bjj_app/photodetail.html'
#     slug_url_kwarg = 'photo_slug'
#     context_object_name = 'photo'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title=context['photo.title'])
#         print(c_def)
#         return {
#             **context,
#             **c_def
#         }


def photo_detail(request, photo_slug):
    photo = get_object_or_404(Photo, slug=photo_slug)
    context = {
        'photo': photo,
        'menu': menu,
        'title': photo.title,
    }
    return render(request, 'bjj_app/photodetail.html', context=context)


class PostDetail(DataMixin, DetailView):
    model = News
    template_name = 'bjj_app/post_detail.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context['reaction_choices'] = NewsReaction.REACTION_CHOICES
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'bjj_app/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Реєстрація')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'bjj_app/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизація')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound('Page not found')
