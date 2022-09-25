import datetime
import json
from decimal import Decimal
from django.db.models import QuerySet
from goods.models import *
from urllib.parse import parse_qs, urlparse
from django.db.models import Sum
from django.core.cache import cache
from typing import Dict
from .forms import FilterForm


def final_price(price_discount):
    pass


class CatalogMixin:

    def get_params_from_request(self, list_params: list, query_params: dict) -> dict:
        """
        Извлекает параметры из гет-запроса согласно заданному списку
        :param query_params:
        :param list_params:
        :return: params
        """
        params = {}
        # print(list_params)
        for param in list_params:
            value_param = query_params.get(param)
            if isinstance(value_param, list):  # Значения параметров приходят ввиде списка с одним элементом
                value_param = value_param[0]  # при исользовании urlparse значения необходимо извлекать вручную
            if value_param:
                params[param] = value_param
                if params.get('trend') == '+':
                    params['trend'] = ''
        # print('this params', params)
        return params

    def get_filter_parameters(self):
        """

        :return:
        """
        self.request.session.setdefault('filter_params', {})
        if not self.request.GET:
            self.request.session['filter_params'].clear()
        elif self.request.GET.get('filter') == 'filter':  # Если нажата кнопка filter
            print('кнопка нажата')
            self.request.session.update({'filter_params': {}})  # обнуляем фильтр-параметры в сессии
            filter_query_params = self.request.GET.dict()
            range_price = filter_query_params.pop('price').split(';')
            min_price = Decimal(range_price[0])
            max_price = Decimal(range_price[1])
            #filter_query_params.update({'price__gte': min_price, 'price__lte': max_price})
            list_filter_params = list(filter_query_params.keys())
            filter_params = self.get_params_from_request(list_filter_params, filter_query_params)
            filter_params.update({'price__gte': min_price, 'price__lte': max_price})
            filter_params.pop('filter')
            self.request.session.update({'filter_params': filter_params})
        return self.request.session.get('filter_params')

    def get_all_parameters(self):
        all_parameters = self.get_filter_parameters()
        return all_parameters

    # def get_parameters(self) -> dict:
    #    """
    #    Возвращает словерь с ключами 'filter' и 'sort'. Значениями являются словари с параметрами
    #    фильтрации и параметрами сортировки соответственно.
    #    :return
    #    """
    #
    #    #print('this session parameters', self.request.session.get('filter_params'))
    #    # self.request.session.setdefault('category_filter_parameter', {})
    #    # category_filter = self.request.session.get('category_filter_parameter')
    #    # new_category_param = self.get_params_from_request(['category__title'], self.request.GET)
    #    # category_filter.update(new_category_param)
    #    # if category_filter.get('category__title') == 'all':
    #    #    category_filter = {}
    #
    #    #self.request.session.setdefault('filter_params', {})
    #    if not self.request.GET:
    #        print('обнулили сессию')
    #        self.request.session['filter_params'] = {}
    #    filter_params = self.request.session.get('filter_params')
    #    list_filter_params = ['name__icontains',
    #                          'delivery__gte',
    #                          'in_stock__gte',
    #                          'goods_in_market__seller__title',
    #                          'price'
    #                          ]
    #
    #    # Проверяем была ли нажата кнопка filter. Если нажата, то заполняем filter_params новыми значениями.
    #    if self.request.GET.get('filter') is not None:
    #        print('нажата кнопка')
    #        filter_params.clear()
    #        filter_params.update(self.get_params_from_request(list_filter_params, self.request.GET))
    #        #range_price = filter_params.pop('price').split(';')
    #        #min_price = Decimal(range_price[0])
    #        #max_price = Decimal(range_price[1])
    #        #filter_params.update({'price__gte': min_price, 'price__lte': max_price})
    #
    #    sort_params = {'sort': 'price', 'trend': ''}  # Параметры сортировки по умолчанию
    #    previous_params = {}
    #    list_sort_params = list(sort_params.keys())
    #    current_param = self.get_params_from_request(list_sort_params, self.request.GET)
    #
    #    # Получение словаря из предыдущего гет-запроса с параметрами
    #    referer_url = self.request.headers.get('Referer')
    #    if referer_url:
    #        previous_query_params = parse_qs(urlparse(referer_url).query)
    #        previous_params.update(self.get_params_from_request(list_sort_params, previous_query_params))
    #
    #    # Обновляем словарь с параметрами сортировки сначала словарём с предыдущими параметрами, потом с текущими
    #    # параметрами
    #    sort_params.update(previous_params)
    #    sort_params.update(current_param)
    #    result_params = {'filter': filter_params, 'sort': sort_params}
    #    return result_params
    #
    #    # Выбираем ОРМ-запрос. Если есть параметры, которые требую использование метода annotate то:
    #
    def select_orm_statement(self) -> QuerySet:
        """
        Возвращает кверисет с использованием метода annotate или без него в зависимости от значений
        словаря, возвращаемого методом get_parameters()
        :return: queryset
        """
        print('this session', self.request.session.get('filter_params'))
        filter_params = self.get_filter_parameters()
        print(filter_params)
        # print('this params', params)
        # category_params = params.get('category_filter')
        # sort_params = params.get('sort')
        if filter_params.get('delivery__gte') or filter_params.get('in_stock__gte'):  # or sort_params[
            #    'sort'
            # ] == 'quantity':
            queryset = Goods.objects.select_related('category').annotate(
                delivery=Sum('goods_in_market__free_delivery'),
                in_stock=Sum('goods_in_market__quantity')
                # quantity=Sum('goods_in_market__order__quantity')
            ).filter(**filter_params)  # .order_by(f"{sort_params['trend']}{sort_params['sort']}")
            # print('this more session', self.request.session.get('filter_params'))
            return queryset

        ## Если фильтрация не требует метода annotate, то выражение ОРМ-запроса будет таким:
        queryset = Goods.objects.select_related('category').filter(
            **filter_params)  # .order_by(f"{sort_params['trend']}{sort_params['sort']}")
        return queryset

    def normalises_values_parameters(self) -> dict:
        """
       Преобразует значения в словаре с параметрами фильтрации для подстановки их в качестве
       атрибутов в html тегах. Если чекбокс нажат, то значение '1' заменяется на 'checked'
       :return: dict
       """
        params_for_form_filter = self.request.session.get('filter_params').copy()
        if not params_for_form_filter:
            return params_for_form_filter

        list_checked_params = ['delivery__gte', 'in_stock__gte', 'price__lte', 'price__gte']
        for param in list_checked_params:
            params_for_form_filter[param] = str(params_for_form_filter[param])
            print('--------', type(params_for_form_filter[param]))
            if params_for_form_filter.get(param) == '1':
                params_for_form_filter[param] = 'checked'
        print('this more session', params_for_form_filter)
        return params_for_form_filter

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
