from django import forms
from .models import Post, Category


class NewsSearchForm(forms.Form):
    author = forms.CharField(label='Автор', required=False)
    title = forms.CharField(label='Название', required=False)
    date_after = forms.DateField(label='Позднее даты', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def clean_date_after(self): # Валидация даты
        date_after = self.cleaned_data.get('date_after')
        return date_after


class PostForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Категории'
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category']