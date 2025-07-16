from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.shortcuts import (
    get_object_or_404, redirect)
from django.urls import reverse_lazy

from blog.forms import CommentForm, PostForm, ProfileUpdateForm
from blog.mixins import OnlyAuthorMixin, OnlyUserMixin, SuccessUrlMixin
from blog.models import (
    Category,
    Comment,
    Post,
    User)


POST_PER_PAGE = 10


class IndexListView(ListView):
    """Главная страница."""

    model = Post
    paginate_by = POST_PER_PAGE
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.published.get_posts_qs().order_by('-pub_date')


class CategoryView(ListView):
    """Страница категории."""

    model = Category
    template_name = 'blog/category.html'
    paginate_by = POST_PER_PAGE

    def get_category(self):
        category = get_object_or_404(
            Category, slug=self.kwargs['category_slug'],
            is_published=True)
        return category

    def get_queryset(self):
        return Post.objects.base_filters().filter(
            category__title=self.get_category().title
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class ProfileDetailView(ListView):
    """Страница профиля пользователя."""

    model = Post
    template_name = 'blog/profile.html'
    paginate_by = POST_PER_PAGE

    def get_user(self):
        user = get_object_or_404(
            User, username=self.kwargs['username'])
        return user

    def get_queryset(self):
        self.author = self.get_user().id
        if self.author != self.request.user.id:
            return Post.objects.base_filters().filter(
                author_id=self.author)
        return Post.objects.post_filter().filter(
            author_id=self.author).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_user()
        return context


class ProfileUpdateView(OnlyUserMixin, UpdateView):
    """Страница редактирования профиля."""

    model = User
    form_class = ProfileUpdateForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        obj = form.save()
        return redirect('blog:profile', obj.username)


class PostCreateView(OnlyUserMixin, CreateView):
    """Создание поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = User.objects.get(
            username=self.request.user.username)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username})


class PostEditView(OnlyAuthorMixin, SuccessUrlMixin, UpdateView):
    """Редактирование поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        post_id = self.kwargs['post_id']
        return redirect(
            reverse_lazy('blog:post_detail', kwargs={'post_id': post_id})
        )


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    """Удаление поста."""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        form = self.form_class(instance=post)
        context['form'] = form
        context['object'] = post
        return context


class PostDetailView(SuccessUrlMixin, DetailView):
    """Полробное описание поста."""

    model = Post
    template_name = 'blog/detail.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(
            Post.objects.post_filter(),
            pk=self.kwargs['post_id'])
        if post.author != self.request.user:
            post = get_object_or_404(
                Post.objects.base_filters(),
                pk=self.kwargs['post_id'])
        comments = Comment.objects.filter(
            post_id=post.id
        ).order_by('created_at')
        context['post'] = post
        context['comments'] = comments
        if self.request.method == 'POST':
            form = CommentForm(self.request.POST, instance=post)
            if form.is_valid():
                obj = form.save()
                form.save()
                return redirect('blog:detail', obj.post_id)
        else:
            form = CommentForm()
        return {
            'form': form,
            **context
        }


class CommentCreateView(OnlyUserMixin, SuccessUrlMixin, CreateView):
    """Создание комментария."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author_id = self.request.user.id
        comment.post_id = self.kwargs['post_id']
        comment.save()
        return super().form_valid(form)


class CommentEditView(OnlyAuthorMixin, SuccessUrlMixin, UpdateView):
    """Редактирование комментария."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class CommentDeleteView(OnlyAuthorMixin, SuccessUrlMixin, DeleteView):
    """Удаление комментария."""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = self.get_object()
        context['comment'] = comment
        return context
