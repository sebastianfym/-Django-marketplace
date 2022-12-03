from django.db.models import QuerySet
from goods.models import Goods
from django.db.models import Sum


def final_price(price_discount):
    pass


def create_compare(compare_list: list) -> [list, list, dict]:
    """
    Функция получния категорий, отдельно характеристик по товарову и параметры товаров от всех товаров в сравнении
    :param compare_list: список id товаров в сравнении
    :return:
    compare_list_products,
    categories_list,
    product_features
    """
    compare_list_products = list()
    categories_list = list()
    for element in compare_list:
        product = Goods.objects.filter(
            id=element
        ).select_related('category').prefetch_related('feature').first()
        compare_list_products.append(product)
        categories_list.append(product.category.title)
    product_features = {
        product.id: product.feature.all() for product in compare_list_products
    }
    return compare_list_products, categories_list, product_features


def get_all_features(product_features: dict) -> dict:
    """
    Функция получния всех характеристик от всех товаров в сравнении
    :param product_features:
    :return: all_features
    """
    all_features = dict()
    for product, features in product_features.items():
        for feature in features:
            if all_features.get(feature.name, 0):
                all_features.get(feature.name).update(
                    {product: feature.value}
                )
            else:
                all_features[feature.name] = {
                    product: feature.value
                }
    return all_features


def get_different_features(all_features: dict, compare_list: list) -> dict:
    """
    Функция получния различных характеристик от всех товаров в сравнении
    :param all_features: словарь из всех характеристик
    :param compare_list: список id товаров
    :return: different_features
    """
    different_features = dict()
    for key, values in all_features.items():
        if len(values.values()) != len(compare_list):
            different_features.update({key: {'diff': values}})
            for product_id in compare_list:
                if product_id not in values.keys():
                    values.update({product_id: 0})
        else:
            value_list = list()
            for prod_id, value in values.items():
                value_list.append(value)
            if len(set(value_list)) > 1:
                different_features.update({key: {'diff ': values}})
            else:
                different_features.update({key: {'same': values}})
    return different_features


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
                if params.get('trend') == 'asc':
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
        elif self.request.GET.get('name__icontains'):
            filter_query_params = self.request.GET.dict()
            list_filter_params = list(filter_query_params.keys())
            filter_params = self.get_params_from_request(list_filter_params, filter_query_params)
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
            current_category.clear()
            category_filter.clear()
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
            ).filter(**filter_params).order_by(f"{sort_params['trend']}{sort_params['sort']}").defer(
                'feature', 'describe', 'goods_in_market', 'brand'
            )
            return queryset

        queryset = Goods.objects.select_related('category').filter(
            **filter_params).order_by(f"{sort_params['trend']}{sort_params['sort']}").defer(
            'feature', 'describe', 'goods_in_market', 'brand'
        )

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




