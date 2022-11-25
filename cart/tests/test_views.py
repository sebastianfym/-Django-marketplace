import simplejson
from django.test import TestCase
from django.urls import reverse

from app_shop.models import Seller
from cart.models import CartItems
from customers.models import CustomerUser
from goods.models import Goods, Category, GoodsInMarket


class CartViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(title='TestCategory')
        product = Goods.objects.create(name='test', price=1, category=category)
        test_user = CustomerUser.objects.create(email='testuser1',
                                                full_name='Test1',
                                                phone='89522611692',
                                                password='TestPass12')
        seller1 = Seller.objects.create(title='test', slug='test', owner_id=1)
        seller2 = Seller.objects.create(title='test2', slug='test_2', owner_id=1)
        goodinmarket1 = GoodsInMarket.objects.create(price=15,
                                              quantity=4,
                                              goods=product,
                                              seller_id=1)
        goodinmarket2 = GoodsInMarket.objects.create(price=22,
                                                    quantity=4,
                                                    goods=product,
                                                    seller_id=2)
        cls.id = product.id
        cls.user = test_user
        cls.seller = seller1
        cls.goodinmarket = goodinmarket1
        cls.category = category

    def setUp(self):
        self.client.force_login(user=self.user)
        self.get_response = self.client.get(reverse(viewname='cart:mycart'))

    def test_cart_add(self):
        self.client.login(email='testuser1', password='TestPass12')
        response = self.client.get(reverse(viewname='cart:add', args=[self.id]), HTTP_REFERER='http://login')
        self.assertEqual(response.status_code, 302)


    def test_delete_cart(self):
        self.client.login(email='testuser1', password='TestPass12')
        CartItems.objects.create(user=self.user, product_in_shop=self.goodinmarket, quantity=4, category=self.category)
        items = CartItems.objects.filter(user=self.user).all()
        self.assertEqual(len(items), 1)
        response = self.client.get(reverse(viewname='cart:remove', args=[self.id]))
        self.assertEqual(response.status_code, 302)
        items = CartItems.objects.filter(user=self.user).all()
        self.assertEqual(len(items), 0)

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)

    def test_view_use_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'cart/cart.html')
