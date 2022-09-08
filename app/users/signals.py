from math import ceil
from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from quizzes.models import Quiz, Solved
from users.models import User

initial: int = 500  # 初期の点数
decay: int = 20  # 回答者数の閾値
minimum: int = 50  # 閾値を超えた際の点数


def recalculate_quiz_score(quiz_id=None):
    quizzes: list[Quiz] = Quiz.objects.filter(published=True).prefetch_related('solved_users')
    if quiz_id is not None:
        quizzes = quizzes.filter(id=quiz_id)

    for quiz in quizzes:
        solve_count: int = quiz.solved_users.filter(is_staff=False).count()
        value = (((minimum - initial) / (decay**2)) * (solve_count**2)) + initial
        value = ceil(value)
        quiz.point = value if value > minimum else minimum
        quiz.save()


@receiver(user_signed_up)
def user_signed_up_callback(**kwargs):
    recalculate_quiz_score()


@receiver(post_delete, sender=User)
def user_deleted_callback(**kwargs):
    recalculate_quiz_score()


@receiver([post_save, post_delete], sender=Solved)
def solved_post_delete_callback(sender, instance, **kwargs):
    recalculate_quiz_score(quiz_id=instance.quiz.id)
