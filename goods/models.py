from django.db import models


class Category(models.Model):
    """
    Класс моделей категорий
    Содержит в себе:
    title - название категории;
    imagen - картинка категории;
    activity - флаг активности новости;
    goods - товары.
    """
    title = models.CharField(max_length=50, blank=True, null=True)
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)
    activity = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return f'{self.title},{self.activity}'


class Goods(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    activity = models.BooleanField(default=False, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f'{self.title},{self.activity}'