from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, F, Q
from django.db.models.expressions import Window
from django.db.models.functions import Rank
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views import generic

from common.views import UserContextMixin
from configurations.models import Configuration

from .forms import CheckFlagForm
from .models import Quiz, QuizAppendedUrl, QuizFile, Solved, SubmitLog

QUIZ_STATUS_COLLECT = 1
QUIZ_STATUS_INVALID = 2


class QuizListView(UserContextMixin, LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Quiz
    template_name = "quizzes/quizzes.html"
    context_object_name = "quizzes"
    raise_exception = True

    def test_func(self) -> Optional[bool]:
        return Configuration.game_ongoing() or self.request.user.is_staff

    def get_quizzes(self, is_extra=False):
        quizzes = (
            Quiz.objects.filter(is_extra=is_extra)
            .select_related("category")
            .order_by("number")
            .annotate(is_solved=Count("solved_users", filter=Q(solved__user=self.request.user)))
            .annotate(winners=Count("solved_users", filter=Q(solved__user__is_staff=False)))
        )

        if self.request.user.is_staff:
            return quizzes
        else:
            return quizzes.filter(published=True)

    def get_queryset(self):
        return self.get_quizzes()

    def get_context_data(self, **kwargs):
        extra_quizzes = self.get_quizzes(is_extra=True)

        context = super().get_context_data(**kwargs)
        context["extra_quizzes"] = extra_quizzes

        return context


class QuizView(UserContextMixin, LoginRequiredMixin, UserPassesTestMixin, generic.FormView):
    template_name = "quizzes/quiz.html"
    form_class = CheckFlagForm

    def test_func(self):
        return Configuration.game_ongoing() or self.request.user.is_staff

    def get_success_url(self) -> str:
        return self.request.path

    def get_quiz_or_404(self, number):
        quiz = get_object_or_404(
            Quiz.objects.select_related("category"),
            number=number,
        )
        if not quiz.published and not self.request.user.is_staff:
            raise Http404

        return quiz

    def get_solved_users(self, quiz):
        return (
            Solved.objects.filter(quiz=quiz, user__is_staff=False)
            .prefetch_related("user")
            .annotate(
                rank=Window(
                    expression=Rank(),
                    order_by=F("solved_at").asc(),
                )
            )
            .annotate(username=F("user__username"))
            .values("username", "solved_at", "rank")
            .order_by("rank", "username")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        quiz = self.get_quiz_or_404(self.kwargs.get("number"))
        if Solved.objects.filter(user=self.request.user, quiz=quiz).exists():
            quiz.status = QUIZ_STATUS_COLLECT
        elif (flag := context["form"].data.get("flag")) and flag != quiz.flag:
            quiz.status = QUIZ_STATUS_INVALID

        context["quiz"] = quiz
        context["quiz_files"] = QuizFile.objects.filter(quiz=quiz)
        context["appended_url"] = QuizAppendedUrl.objects.filter(quiz=quiz)
        context["solved_users"] = self.get_solved_users(quiz)

        return context

    def form_valid(self, form):
        quiz = self.get_quiz_or_404(self.kwargs.get("number"))
        if form.data["flag"] == quiz.flag:
            solved, _ = Solved.objects.get_or_create(user=self.request.user, quiz=quiz)
            SubmitLog.objects.create(user=self.request.user, quiz=quiz, flag=form.data["flag"], solved=solved)
        else:
            SubmitLog.objects.create(user=self.request.user, quiz=quiz, flag=form.data["flag"])

        return self.render_to_response(self.get_context_data(form=form))
