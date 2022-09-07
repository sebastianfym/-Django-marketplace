from goods.models import Goods
from django.http import HttpRequest
from urllib.parse import parse_qs, urlparse


def final_price(price_discount):
    pass


class CatalogMixin:

    def get_sort_param(self) -> dict:
        """
        Получает из get-параметров значения по ключам 'sort' и 'trend'
        :return tuple
        """
        query_param = {'sort': 'price', 'trend': ''}
        print('Словарь ГЕТ', self.request.GET.dict())
        previous_param = {}
        current_param = self.request.GET.dict()
        referer_url = self.request.headers.get('Referer')
        if referer_url:
            previous_param = parse_qs(urlparse(referer_url).query)
            for param in previous_param:
                previous_param[param] = previous_param[param][0]
        query_param.update(previous_param)
        query_param.update(current_param)
        return query_param

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
