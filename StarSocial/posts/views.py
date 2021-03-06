from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.http import Http404
from braces.views import SelectRelatedMixin
from django.contrib import messages
from .models import Post
from groups.models import Group
from . import forms
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

class PostList(SelectRelatedMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    select_related = ('user', 'group')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_groups'] = Group.objects.filter(members__in=[self.request.user.pk])
        context['all_groups'] = Group.objects.all()
        return context

class UserPosts(ListView):
    model = Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            # Let's try a different way to achieve this goal
            self.post_user = User.objects.prefetch_related('posts').get(
                username__iexact=self.kwargs.get('username')
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetail(DetailView, SelectRelatedMixin):
    model = Post
    select_related = ('user', 'group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin, SelectRelatedMixin, CreateView):
    fields = ('message', 'group')
    model = Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin, SelectRelatedMixin, DeleteView):
    model = Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)
