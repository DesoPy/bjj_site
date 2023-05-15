from .models import *

menu = [{'title': 'Головна', 'url_name': 'home'},
        {'title': 'Галерея', 'url_name': 'gallery'},
        {'title': 'Розклад тренувань', 'url_name': 'schedule'},
        {'title': 'Про нас', 'url_name': 'about'},
        {'title': 'Контакти', 'url_name': 'contacts'},
        ]


class DataMixin:
    paginate_by = 10

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context
