from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from .models import User
from quizzes.models import Quiz


@receiver(user_signed_up)
def user_signed_up_callback(**kwargs):
    user_count = User.objects.filter(is_staff=False).count()
    quizzes = Quiz.objects.filter(published=True).prefetch_related('solved_users')

    if user_count == 0:
        return

    for quiz in quizzes:
        solved_user_count = quiz.solved_users.filter(is_staff=False).count()
        new_point = 50 + int(450 * (1 - solved_user_count / user_count))
        quiz.point = new_point
        quiz.save()
