from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Stat(models.Model):
    donater = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='stats',
        verbose_name='Пользователь',
    )
    count_unisender = models.IntegerField(
        blank=True,
        verbose_name='Счётчик запросов unisender'
    )
    balance = models.FloatField(
        blank=True,
        verbose_name='баланс'
    )
    donat = models.FloatField(
        blank=True,
        verbose_name='Всего поступлений'
    )


class Connect(models.Model):
    donater = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='connects',
        verbose_name='Пользователь',
    )
    feedback = models.TextField(
        verbose_name='Отзыв',
    )