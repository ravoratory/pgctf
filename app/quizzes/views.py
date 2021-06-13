from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .forms import CheckFlagForm
from .models import Quiz, QuizAppendedUrl, QuizFile, Solved


QUIZ_STATUS_COLLECT = 1
QUIZ_STATUS_INVALID = 2


class QuizView(LoginRequiredMixin, generic.View):
    template_name = 'quizzes/quiz.html'

    def get_quiz_or_404(self, quiz_number):
        return get_object_or_404(
            Quiz.objects.select_related('category'),
            quiz_number=quiz_number,
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
            {'form': form, 'quiz': quiz, 'user': user, 'quiz_files': quiz_files, 'appended_url': appended_url}
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
            quiz.status = 1
        else:
            quiz.status = QUIZ_STATUS_INVALID
        print(form.data['flag'])

        user.points = Solved.objects.filter(user=user, quiz__published=True).aggregate(points=Sum('quiz__point'))['points'] or 0
        return render(
            request,
            'quizzes/quiz.html',
            {'form': form, 'quiz': quiz, 'user': user, 'quiz_files': quiz_files}
        )
