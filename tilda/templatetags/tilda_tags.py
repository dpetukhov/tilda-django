from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def tilda_scripts(article):
    return mark_safe(article.prepare_scripts())


@register.simple_tag
def tilda_styles(article):
    return mark_safe(article.prepare_styles())


@register.simple_tag
def tilda_content(article):
    return mark_safe(article.prepare_content())
