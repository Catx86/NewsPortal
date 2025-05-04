from django import template


register = template.Library()

bad_list = ['Редиска', 'редиска']  # Список запрещенных к публикации слов

@register.filter(name='censor')
def censor(data):
    """ Заменяет запрещенные слова в строке из списка censored_list
     на "'первая буква слова' + n'*'" """
    if isinstance(data, str):
        words = data.split()
        censored_text = []

        for word in words:
            replaced = 0
            for bad_word in bad_list:
                idx = word.find(bad_word)
                if idx >= 0:
                    replace = bad_word[0] + '*' * (len(bad_word) - 1)
                    censored_word = word.replace(bad_word, replace)
                    censored_text.append(censored_word)
                    replaced = 1
                    break
            if not replaced:
                censored_text.append(word)
        return ' '.join(censored_text)
    else:
        raise ValueError("Фильтр censor может быть применен только к строкам.")

# Использование в шаблоне:
# {{ new.title|censor }}