from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE) # , primary_key=True  ???
    rate = models.FloatField(default = 0.0)

    def __str__(self):
        return self.author.username

    def update_rating(self):

        # суммарный рейтинг каждой статьи автора умножается на 3;
        qs = Post.objects.filter(author=self).values('rate')
        qs1_sum_rate = 0
        for item in qs:
            qs1_sum_rate += 3 * item.get('rate')
        print(qs1_sum_rate)

        # суммарный рейтинг всех комментариев автора;
        qs2 = Comment.objects.filter(user=self.author).values('rate')
        qs2_sum_rate = 0
        for item in qs2:
            qs2_sum_rate += item.get('rate')
        print(qs2_sum_rate)

        # суммарный рейтинг всех комментариев к статьям автора.
        qs3 = Post.objects.filter(author=self).values('id')
        qs3_sum_rate = 0
        for item in qs3:
            post_id = item.get('id')
            qs4 = Comment.objects.filter(post=post_id).values('rate')
            for item in qs4:
                qs3_sum_rate += item.get('rate')
        print(qs3_sum_rate)

        self.rate =  qs1_sum_rate + qs2_sum_rate + qs3_sum_rate
        self.save()


class Category(models.Model):
    category = models.CharField(max_length = 255, unique = True)

    def __str__(self):
        return f'{self.category}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE) # связь «один ко многим» с моделью Author;
    is_article = models.BooleanField(default=False) # поле с выбором: новость - False, статья - True
    date_time_out = models.DateTimeField(auto_now_add=True) # автоматически добавляемая дата и время создания;
    # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length=255) # заголовок статьи/новости;
    content = models.TextField() # текст статьи/новости;
    rate = models.FloatField(default=0.0) # рейтинг статьи/новости.

    def __str__(self):
        return f'{self.title.title()}: {self.content[:20]}'

    def preview(self):
        """Метод возвращает начало статьи (предварительный просмотр) длиной 124 символа, добавляет многоточие в конце"""
        return self.content[:124] + '...'

    # Like, Dislike в моделях Comment и Post
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
