from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import User
from quizzes.models import Quiz, Solved


def recalculate_quiz_score(quiz_id=None):
    user_count = User.objects.filter(is_staff=False).count()
    if user_count == 0:
        return

    quizzes = Quiz.objects.filter(published=True).prefetch_related('solved_users')
    if quiz_id is not None:
        quizzes = quizzes.filter(id=quiz_id)

    for quiz in quizzes:
        solved_user_count = quiz.solved_users.filter(is_staff=False).count()
        new_point = 50 + int(450 * (1 - solved_user_count / user_count))
        quiz.point = new_point
        quiz.save()


@receiver(user_signed_up)
def user_signed_up_callback(**kwargs):
    recalculate_quiz_score()


@receiver([post_save, post_delete], sender=Solved)
def solved_post_delete_callback(sender, instance, **kwargs):
    recalculate_quiz_score(quiz_id=instance.quiz.id)
