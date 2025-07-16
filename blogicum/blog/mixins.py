from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin)
from django.urls import reverse_lazy


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин для доступа только автору."""

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class OnlyUserMixin(LoginRequiredMixin):
    """Миксин для доступа только залогиненному пользователю."""

    pass


class SuccessUrlMixin:
    """Миксин переадресации на страницу поста."""

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})
