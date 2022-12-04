from django.test import TestCase
from django.urls import reverse

from customers.models import CustomerUser
from goods.models import Category, Goods, Image


class ComparePageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(title='TestCategory')
        category2 = Category.objects.create(title='TestCategory2')
        product1 = Goods.objects.create(name='test1', price=1, category=category)
        product2 = Goods.objects.create(name='test2', price=5, category=category)
        product3 = Goods.objects.create(name='test3', price=10, category=category2)
        test_user = CustomerUser.objects.create(email='testuser1',
                                                full_name='Test1',
                                                phone='89522611692',
                                                password='TestPass12')
        cls.id1 = product1.id
        cls.id2 = product2.id
        cls.id3 = product3.id
        cls.user = test_user

    def test_add_product_to_compare(self):
        response = self.client.get(reverse(viewname='compare_add', args=[self.id1]), HTTP_REFERER='http://login')
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse(viewname='compare'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['compare_list']), 1)

    def test_remove_product_to_compare(self):
        self.client.get(reverse(viewname='compare_add', args=[self.id1]), HTTP_REFERER='http://login')
        self.client.get(reverse(viewname='compare_add', args=[self.id2]), HTTP_REFERER='http://login')
        response = self.client.get(reverse(viewname='compare'))
        self.assertEqual(len(response.context['compare_list']), 2)
        response = self.client.get(reverse(viewname='compare_delete', args=[self.id1]))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse(viewname='compare'))
        self.assertEqual(len(response.context['compare_list']), 1)

    def test_compare_page(self):
        self.client.get(reverse(viewname='compare_add', args=[self.id1]), HTTP_REFERER='http://login')
        self.client.get(reverse(viewname='compare_add', args=[self.id3]), HTTP_REFERER='http://login')
        response = self.client.get(reverse(viewname='compare'))
        self.assertEqual(len(response.context['compare_list']), 2)
        self.assertFalse(response.context['different_features'])


class GoodsDetailPageTest(TestCase):
    def setUp(self) -> None:
        test_category = Category.objects.create(title='testcategory',
                                                imagen=None,
                                                activity=True,
                                                supercat=None
                                                )

        self.test_goods = Goods.objects.create(name='testproduct',
                                          slug='TestProduct1',
                                          brand='TestBrand',
                                          price=1.0,
                                          describe='TestProductDescribe',
                                          limit_edition=True,
                                          category=test_category,
                                          rating=5,
                                          pk=0
                                          )

        self.test_image = Image.objects.create(name='TestImage', product=self.test_goods, image='None')

    def test_detail_goods_page(self):
        url = reverse('detail', kwargs={'pk': self.test_goods.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
