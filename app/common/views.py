from django.contrib.auth.mixins import UserPassesTestMixin

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


class QuizViewableUserContextTestMixin(UserContextMixin, UserPassesTestMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ongoing"] = Configuration.game_ongoing()
        context["paused"] = Configuration.game_paused()
        context["quiz_viewable"] = Configuration.quiz_viewable()

        return context

    def test_func(self):
        user = self.request.user
        game_ongoing = Configuration.game_ongoing()
        quiz_viewable = Configuration.quiz_viewable()

        return user.is_staff or game_ongoing or quiz_viewable


class RankingViewableUserContextTestMixin(CommonSystemUserContextMixin, UserPassesTestMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ranking_viewable"] = Configuration.ranking_viewable()
        context["enable_ranking"], context["freeze_time"] = Configuration.enable_ranking()

        return context

    def test_func(self):
        user = self.request.user
        ranking_open = Configuration.ranking_viewable()

        return ranking_open or user.is_staff
