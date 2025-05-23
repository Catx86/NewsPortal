from datetime import datetime

from django import template


register = template.Library()


@register.simple_tag()
def current_time(format_string='%d %m %Y'):
   return datetime.now().strftime(format_string)

@register.simple_tag()
def pub_date(dt, format_string='%d %m %Y'):
   return dt.strftime(format_string)

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
   d = context['request'].GET.copy()
   for k, v in kwargs.items():
       d[k] = v
   return d.urlencode()