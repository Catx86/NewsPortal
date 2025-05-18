from django.contrib.sessions.backends.base import UpdateError
from django.shortcuts import render

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from .models import Post, Author
from .forms import NewsSearchForm, PostForm
from django.urls import reverse


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_time_out'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10  # указываем количество записей на странице


class NewDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной публикации
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'new'


def news_search(request):
    form = NewsSearchForm(request.GET)  # Заполняем форму данными из GET-запроса

    if form.is_valid():
        title = form.cleaned_data.get('title')
        author = form.cleaned_data.get('author')
        date_after = form.cleaned_data.get('date_after')

        news = []
        if title or author or date_after:
            news = Post.objects.all()  # Получаем все новости, затем фильтруем
            # Фильтрация
            if title:
                news = news.filter(title__icontains=title)  # Поиск по названию
            if author:
                news = news.filter( author__author__username__icontains=author)  # Поиск по автору
            if date_after:
                news = news.filter(date_time_out__gte=date_after)  # Дата публикации позже либо равна указанной

    context = {
        'form': form,
        'news': news,
    }
    return render(request, 'news_search.html', context)


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'  # Убедитесь, что этот шаблон существует

    def get_success_url(self):
        return reverse('news_list')  # Перенаправляем на news_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post_type'] = 'статью' if post.is_article == True else 'новость'
        return context

class NewDelete(PostDelete):
    pass

class ArticleDelete(PostDelete):
    pass


class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        author = Author.objects.get(author=self.request.user)
        post.author = author
        post.is_article = self.is_article
        post.save()

        return super().form_valid(form)  # Или return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        # Вызывается, если форма не прошла валидацию.
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('news_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_type'] = 'статью' if self.is_article == True else 'новость'
        return context

class NewCreate(PostCreate):
    is_article = False

class ArticleCreate(PostCreate):
    is_article = True



class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'

    def get_success_url(self):
        return reverse('news_list')  # Перенаправляем на news_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post_type'] = 'статью' if post.is_article == True else 'новость'
        return context

class NewUpdate(PostUpdate):
    pass

class ArticleUpdate(PostUpdate):
    pass
