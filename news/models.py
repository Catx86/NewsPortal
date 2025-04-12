from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.FloatField(default = 0.0)

    def update_rating(self):
        # суммарный рейтинг каждой статьи автора умножается на 3;
        # суммарный рейтинг всех комментариев автора;
        # суммарный рейтинг всех комментариев к статьям автора.
        pass


class Category(models.Model):
    category = models.CharField(max_length = 255, unique = True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE) # связь «один ко многим» с моделью Author;
    is_article = models.BooleanField(default=False) # поле с выбором: новость - False, статья - True
    date_time_out = models.DateTimeField(auto_now_add=True) # автоматически добавляемая дата и время создания;
    # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length=255) # заголовок статьи/новости;
    content = models.TextField() # текст статьи/новости;
    rate = models.FloatField(default=0.0) # рейтинг статьи/новости.

    def preview(self):
        """Метод возвращает начало статьи (предварительный просмотр) длиной 124 символа, добавляет многоточие в конце"""
        return self.content[:124] + '...'

    # в моделях Comment и Post,
    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()


class PostCategory(models.Model):
    """Промежуточная модель для связи «многие ко многим»:"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # связь «один ко многим» с моделью Post;
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # связь «один ко многим» с моделью Category.


class Comment(models.Model):
    """Модель для хранения комментариев"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # связь «один ко многим» с моделью Post;
    user = models.ForeignKey(User, on_delete=models.CASCADE) # связь «один ко многим» с моделью User (автор коммент.);
    comment = models.TextField() # текст комментария;
    date_time_out = models.DateTimeField(auto_now_add=True) # дата и время создания комментария;
    rate = models.FloatField(default=0.0) # рейтинг комментария.

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()
