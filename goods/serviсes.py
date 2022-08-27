from models import Goods

def final_price(price_discount):
    pass


class CatalogMixin:

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
