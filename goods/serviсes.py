import datetime
import decimal
from django.db.models import Q

from django.db.models import QuerySet

from discounts.models import Discount
from goods.models import Goods, ViewHistory, GoodsInMarket
from django.db.models import Sum
from customers.models import CustomerUser


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
        for param in list_params:
            value_param = query_params.get(param)
            if value_param:
                params[param] = value_param
                if params.get('trend') == '+':
                    params['trend'] = ''
        return params

    def get_filter_parameters(self) -> dict:
        """
        Метод формирует словарь из полей блока фильтра страницы каталога, сохраняет его в сессии с ключём
        'filter_params' и возвращает его для дальнейшего формирования ОРМ-запроса с этими параметрами фильтрации.
        Когда пользователь в первый раз за сеанс заходит на страницу каталога, то значение в сессии по ключу
        'filter_params' становится пустым словарём.
        :return: self.request.session.get('filter_params')
        """
        self.request.session.setdefault('filter_params', {})
        if not self.request.GET:
            self.request.session['filter_params'].clear()
        elif self.request.GET.get('filter') == 'filter':
            self.request.session.update({'filter_params': {}})
            filter_query_params = self.request.GET.dict()
            range_price = filter_query_params.pop('price').split(';')
            min_price = int(range_price[0])
            max_price = int(range_price[1])
            filter_query_params.update({'price__gte': min_price, 'price__lte': max_price})
            list_filter_params = list(filter_query_params.keys())
            filter_params = self.get_params_from_request(list_filter_params, filter_query_params)
            filter_params.update({'price__gte': min_price, 'price__lte': max_price})
            filter_params.pop('filter')
            self.request.session.update({'filter_params': filter_params})
        return self.request.session.get('filter_params')

    def get_category_filter(self) -> dict:
        """
        Метод формирует словарь с ключом 'category__title' из значения, выбранного в выпадающем меню 'category'
        на странице каталога и переданного на сервер в виде гет-параметра 'category__title'. Если в гет-параметрах
        ничего не передано (пользователь только зашёл на страницу каталога) или передан параметр
        category__title=all, то словарь очищается и передаётся пустым, в противном случае в словарь передаётся
        значение равное полю title выбранной категории. Словарь сохраняется в сессии с ключом
        'category_filter_parameter'.
        :return: category_filter
        """
        self.request.session.setdefault('category_filter_parameter', {})
        category_filter = self.request.session.get('category_filter_parameter')
        if not self.request.GET:
            category_filter.clear()
        current_category = self.get_params_from_request(['category__title'], self.request.GET)
        if current_category.get('category__title') == 'all':
            print(current_category.get('category__title'))
            current_category.clear()
            category_filter.clear()
            print(current_category)
        category_filter.update(current_category)
        self.request.session['category_filter_parameter'] = category_filter
        return category_filter

    def get_sort_parameters(self) -> dict:
        """
        Метод создаёт в сессии словарь с ключом 'sort', значением которого является словарь с параметрами сортировки.
        По умолчанию сортировка происводится по цене по возрастанию.
        :return: sortparams
        """
        self.request.session.setdefault('sort', {'sort': 'price', 'trend': ''})
        sort_params = self.request.session.get('sort')
        list_sort_params = list(sort_params.keys())
        current_sort_params = {}
        if self.request.GET:
            current_sort_params.update(self.get_params_from_request(list_sort_params, self.request.GET))
        sort_params.update(current_sort_params)
        return sort_params

    def get_all_parameters(self) -> dict:
        """
        Метод формирует словарь с ключами 'all_filter', 'sort_params'. Значения этих ключей являются словарями
        с параметрами фильтрации и сортировки. Эти словари используются в ОРМ выражении для получения нужного кверисета
        :return: all_parameters
        """
        filter_parameters = self.get_filter_parameters()
        category_filter = self.get_category_filter()
        sort_params = self.get_sort_parameters()
        all_parameters = {'all_filter': {**filter_parameters, **category_filter}, 'sort_params': sort_params}
        return all_parameters

    def select_orm_statement(self) -> QuerySet:
        """
        Возвращает кверисет с использованием метода annotate или без него в зависимости от значений
        словаря, возвращаемого методом get_parameters()
        :return: queryset
        """

        all_params = self.get_all_parameters()
        filter_params = all_params.get('all_filter')
        sort_params = all_params.get('sort_params')
        if filter_params.get('delivery__gte') or filter_params.get('in_stock__gte') or sort_params[
            'sort'
        ] == 'quantity':
            queryset = Goods.objects.select_related('category').annotate(
                delivery=Sum('goods_in_market__free_delivery'),
                in_stock=Sum('goods_in_market__quantity'),
                quantity=Sum('goods_in_market__order__quantity')
            ).filter(**filter_params).order_by(f"{sort_params['trend']}{sort_params['sort']}")
            return queryset

        queryset = Goods.objects.select_related('category').filter(
            **filter_params).order_by(f"{sort_params['trend']}{sort_params['sort']}")
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

        list_checked_params = ['delivery__gte', 'in_stock__gte']
        for param in list_checked_params:
            if params_for_form_filter.get(param) == '1':
                params_for_form_filter[param] = 'checked'
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


def add_to_view_history(customer, goods: Goods) -> None:
    ViewHistory.objects.update_or_create(customer=customer,
                                         goods=goods,
                                         defaults={'last_view': datetime.datetime.now()})


def remove_from_view_history(customer, goods: Goods) -> None:
    ViewHistory.objects.delete(customer=customer, goods=goods)


def is_in_view_history(customer, goods: Goods) -> bool:
    if ViewHistory.objects.get(customer=customer, goods=goods):
        return True
    else:
        return False


def price_with_discount(goods: Goods, old_price=0.00) -> decimal:
    """
    Метод для расчета скидки по товару. Если не указана старая цена, выбирается максимальная из всех предложенных.
    Выбираются все действующие скидки на товар, или на его категорию, возвращается цена с максимальной скидкой,
    но не меньше 1 руб.
    :param goods: товар, по которому ищем цену
    :param old_price: старая цена
    :return: цена с учетом скидки
    """
    if not old_price:
        old_price = GoodsInMarket.objects.filter(goods=goods).aggregate(max('price'))
    today = datetime.date.today()
    goods_discounts = Discount.objects.filter(Q(goods_1=goods) | Q(category_1=goods.category),
                                              discount_type__pk=1,
                                              date_start__lte=today,
                                              date_end__gte=today
                                              )
    percent_discount = goods_discounts.objects.filter(discount_mech__pk=1).aggregate(max('discount_value'))
    percent_discount_price = round((1 - percent_discount) / 100 * old_price, 2)
    absolute_discount = goods_discounts.objects.filter(discount_mech__pk=2).aggregate(max('discount_value'))
    absolute_discount_price = old_price - absolute_discount
    if absolute_discount_price <= 0:
        return 1.00
    if percent_discount_price < absolute_discount_price:
        return percent_discount_price
    return absolute_discount_price


def cart_cost(cart: dict) -> dict:
    """
    Метод получает в качестве параметра словарь вида «товар и исходная цена» и пытается применить
    самую приоритетную скидку на корзину или на набор. Если такая скидка есть, то применяется она; если нет,
    то тогда метод получает цену на каждый товар словаря.
    :param cart: {товар: исходная цена}
    :return: {товар: исходная цена, цена со скидкой, применена ли скидка}
    :rtype: dict
    """
    today = datetime.date.today()
    goods_count = len(cart)
    goods_cost = sum(cart.values())
    cart_discount = Discount.objects.filter(Q(discount_type__pk=3),
                                            date_start__lte=today,
                                            date_end__gte=today,
                                            min_amount__lte=goods_count,
                                            max_amount__gte=goods_count,
                                            min_cost__lte=goods_cost,
                                            max_cost__lte=goods_cost,
                                            ).order_by('-weight').first()

    set_discount = Discount.objects.filter(Q(discount_type__pk=2),
                                           Q(goods_1__in=cart.keys()) | Q(category_1__in=cart.keys.category),
                                           Q(goods_2__in=cart.keys()) | Q(category_2__in=cart.keys.category),
                                           date_start__lte=today,
                                           date_end__gte=today,
                                           ).order_by('-weight').first()
    res = {}
    if cart_discount.weight >= set_discount.weight:
        total_discount = cart_discount.value
    elif set_discount:
        total_discount = set_discount.value
    else:
        for goods, price in cart.items():
            new_price = price_with_discount(goods, price)
            if new_price < price:
                res[goods] = (price, new_price, True)
            else:
                res[goods] = (price, price, False)
        else:
            return res
    for goods, price in cart.items():
        res[goods] = (price, round(price * (1 - total_discount / 100)), True)
    return res
