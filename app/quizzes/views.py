from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, Sum
from django.db.models import F, Max, Sum
from django.db.models.expressions import Window
from django.db.models.functions import Rank
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.decorators.http import require_GET

from .forms import CheckFlagForm
from .models import Quiz, QuizAppendedUrl, QuizFile, Solved


User = get_user_model()

QUIZ_STATUS_COLLECT = 1
QUIZ_STATUS_INVALID = 2


@login_required
@require_GET
def quiz_list_view(request, *args, **kwargs):
    user = request.user
    user.points = Solved.objects.filter(user=user, quiz__published=True).aggregate(points=Sum('quiz__point'))['points'] or 0
    quizzes = (Quiz.objects
        .select_related('category')
        .order_by('quiz_number')
        .annotate(is_solved=Count('solved_users', filter=Q(solved__user=request.user)))
        .annotate(winners=Count('solved_users', filter=Q(solved__user__is_staff=False)))
    )

    if not user.is_staff:
        quizzes = quizzes.filter(published=True)

    return render(request, 'quizzes/quizzes.html', {'user': user, 'quizzes': quizzes})


class QuizView(LoginRequiredMixin, generic.View):
    template_name = 'quizzes/quiz.html'

    def get_quiz_or_404(self, quiz_number):
        quiz = get_object_or_404(
            Quiz.objects.select_related('category'),
            quiz_number=quiz_number,
        )
        if not quiz.published and not self.request.user.is_staff:
            raise Http404

        return quiz

    def get_solved_users(self, quiz):
        return (Solved.objects
            .filter(quiz=quiz, user__is_staff=False)
            .prefetch_related('user')
            .annotate(rank=Window(
                expression=Rank(),
                order_by=F('solved_datetime').asc(),
            ))
            .annotate(username=F('user__username'))
            .values('username', 'solved_datetime', 'rank')
            .order_by('-solved_datetime')
        )

    def get(self, request, *arg, **kwargs):
        user = request.user
        user.points = Solved.objects.filter(user=user, quiz__published=True).aggregate(points=Sum('quiz__point'))['points'] or 0
        quiz = self.get_quiz_or_404(self.kwargs.get('quiz_number'))
        quiz_files = QuizFile.objects.filter(quiz=quiz)
        appended_url = QuizAppendedUrl.objects.filter(quiz=quiz)

        if Solved.objects.filter(user=request.user, quiz=quiz).exists():
            quiz.status = QUIZ_STATUS_COLLECT

        form = CheckFlagForm()

        return render(
            request,
            'quizzes/quiz.html',
            {
                'form': form,
                'quiz': quiz,
                'user': user,
                'quiz_files': quiz_files,
                'appended_url': appended_url,
                'solved_users': self.get_solved_users(quiz),
            }
        )

    def post(self, request, *args, **kwargs):
        user = request.user
        form = CheckFlagForm(data=request.POST)
        quiz = self.get_quiz_or_404(self.kwargs.get('quiz_number'))
        quiz_files = QuizFile.objects.filter(quiz=quiz)

        if not form.is_valid():
            return render(request, self.template_name, {'form': CheckFlagForm(), 'quiz': quiz, 'user': user})
        elif form.data['flag'] == quiz.flag:
            Solved.objects.get_or_create(user=request.user, quiz=quiz)

            user_count = User.objects.filter(is_staff=False).count()
            solved_user_count = Solved.objects.filter(quiz=quiz, user__is_staff=False).count()
            if user_count != 0:
                new_point = 50 + int(450 * (1 - solved_user_count / user_count))
                Quiz.objects.filter(pk=quiz.id).update(point=new_point)
                quiz.point = new_point

            quiz.status = QUIZ_STATUS_COLLECT
        else:
            quiz.status = QUIZ_STATUS_INVALID

        user.points = Solved.objects.filter(user=user, quiz__published=True).aggregate(points=Sum('quiz__point'))['points'] or 0

        return render(
            request,
            'quizzes/quiz.html',
            {
                'form': form,
                'quiz': quiz,
                'user': user,
                'quiz_files': quiz_files,
                'solved_users': self.get_solved_users(quiz),
            }
        )
