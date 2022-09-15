from configurations.models import Configuration
from users.models import User


class UserContextMixin:
    def get_context_data(self, **kwargs):
        user: User = self.request.user
        if user.is_authenticated:
            user.points = user.total_score()

        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user

        return context


class CommonSystemUserContextMixin(UserContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ongoing"] = Configuration.game_ongoing()
        context["paused"] = Configuration.game_paused()

        return context
