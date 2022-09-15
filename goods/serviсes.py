from goods.models import Goods
from urllib.parse import parse_qs, urlparse
from django.db.models import Sum
from django.core.cache import cache
from typing import Dict



def final_price(price_discount):
    pass


class CatalogMixin:

    def get_params_from_request(self, list_params: list, query_params: dict):
        """
        Извлекает параметры из гет-запроса согласно заданному списку
        :param query_params:
        :param list_params:
        :return: params
        """
        params = {}
        for param in list_params:
            value_param = query_params.get(param)
            if value_param:
                if isinstance(value_param, list):
                    value_param = value_param[0]
                if value_param == '+':
                    value_param = ''
                if param != 'trend' or value_param != '':  # если параметр не "тренд" или его значение не пустое
                    params[param] = value_param            # заносим значение в словарь

        return params

    def get_parameters(self) -> dict:
        """
        Возвращает словерь с ключами 'filter' и 'sort'. Значениями являются словари с параметрами
        фильтрации и параметрами сортировки соответственно.
        :return
        """
        self.request.session.setdefault('filter_params', {})
        filter_params = self.request.session.get('filter_params')
        list_filter_params = ['name__icontains',
                              'delivery__gte',
                              'in_stock__gte',
                              'goods_in_market__seller__title',
                              'delivery__gte',
                              'price__gte',
                              'price__lte'
                              ]

        # Проверяем была ли нажата кнопка filter
        if self.request.GET.get('filter') is not None:
            filter_params.clear()
            filter_params.update(self.get_params_from_request(list_filter_params, self.request.GET))

        sort_params = {'sort': 'price', 'trend': ''}        # Параметры сортировки по умолчанию
        previous_params = {}
        list_sort_params = list(sort_params.keys())
        current_param = self.get_params_from_request(list_sort_params, self.request.GET)

        # Получение словаря из предыдущего гет-запроса с параметрами
        referer_url = self.request.headers.get('Referer')
        if referer_url:
            previous_query_params = parse_qs(urlparse(referer_url).query)
            previous_params.update(self.get_params_from_request(list_sort_params, previous_query_params))

        # Обновляем словарь с параметрами сортировки сначала словарём с предыдущими параметрами, потом с текущими
        # параметрами
        sort_params.update(previous_params)
        sort_params.update(current_param)
        result_params = {'filter': filter_params, 'sort': sort_params}
        return result_params

        # Выбираем ОРМ-запрос. Если есть параметры, которые требую использование метода annotate то:
    def select_orm_statement(self):
        """
        Возвращает кверисет с использованием метода annotate или без него в зависимости от значений
        словаря, возвращаемого методом get_parameters()
        :return: queryset
        """
        params = self.get_parameters()
        filter_params = params.get('filter')
        sort_params = params.get('sort')
        if filter_params.get('delivery__gte') or filter_params.get('in_stock__gte'):
            queryset = Goods.objects.annotate(
                delivery=Sum('goods_in_market__free_delivery'),
                in_stock=Sum('goods_in_market__quantity')
            ).filter(**filter_params).order_by(f"{sort_params['trend']}{sort_params['sort']}")
            return queryset

        # Если фильтрация не требует метода annotate, то выражение ОРМ-запроса будет таким:
        queryset = Goods.objects.filter(**filter_params).order_by(f"{sort_params['trend']}{sort_params['sort']}")
        return queryset

    def normalises_values_parameters(self) -> dict:
        """
        Преобразует значения в словаре с параметрами фильтрации для подстановки их в качестве
        атрибутов в html тегах. Если чекбокс нажат, то значение '1' заменяется на 'checked'
        :return: dict
        """
        filter_params = self.get_parameters().get('filter').copy()
        list_checked_params = ['delivery__gte', 'in_stock__gte']
        for param in list_checked_params:
            if filter_params.get(param) == '1':
                filter_params[param] = 'checked'
        return filter_params



### написать функцию для извлечения нормальных гетпараметров.


    def final_price_calculation(self):
        pass

    def get_number_sellers(self):
        pass

    def get_numbers_reviews(self):
        pass

    def list_sorting(self, query_param):
        pass


class GoodsMixin:
    """Класс-миксин для модели goods"""

    def add_review(self, user_id: int, goods_id: int, review: str):
        """
        Добавляет отзыв на товар от определённого пользователя в модель review
        :param user_id:
        :param goods_id:
        :param review
        :return: None
        Метод добавляет отзыв
        """
        pass

    def price_calculation(self) -> int:
        """
        Метод расчитывает значение поля price как среднее значение полей price всех записей модели goods_in_market
        имеющих отношение к текущей записи модели goods и с учётом скидки из модели Promotion, если она есть.
        :param:
        :return: int
        """
        pass

    def add_to_view_history(self):
        """
        Добавляет товар, который был открыт в detail_view в список просмотренных товаров пользователя
        :return: None
        """
        pass


class GoodsInMarketMixin:
    """
    Класс-миксин для модели GoodsInMarket
    """

    def add_to_cart(self):
        """
        Добавляет товар от определённого продавца в корзину
        :return:
        """
        pass
