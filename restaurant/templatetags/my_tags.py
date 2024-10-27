"""Файл для создания шаблонного фильтра"""
from django import template

register = template.Library()


@register.filter
def media_filter(path):
    if path:
        return f'/media/{path}'
    return '#'
