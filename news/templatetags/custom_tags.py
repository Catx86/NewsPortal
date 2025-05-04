from datetime import datetime

from django import template


register = template.Library()


@register.simple_tag()
def current_time(format_string='%d %m %Y'):
   return datetime.now().strftime(format_string)

@register.simple_tag()
def pub_date(dt, format_string='%d %m %Y'):
   return dt.strftime(format_string)