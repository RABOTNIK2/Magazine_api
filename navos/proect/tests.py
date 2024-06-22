from django.test import TestCase
from .models import *
from urllib.parse import urlencode
from django.urls import reverse

class TestProduct(TestCase):
    def test_list(self):
        response = self.client.get('/magazine_api/product/')
        self.assertEqual(response.status_code, 200)
        
    def setUp(self):
        self.category = Category.objects.create(name='Булыга')
        self.product = Product.objects.create(name='cyka', description='fgfhfdv', category=self.category, rating=3, image='fgfhbbb', price=999)
        self.product2 = Product.objects.create(name='gnida', description='fgfhfdv', category=self.category, rating=3, image='fgfhbbb', price=999)
        self.user = User.objects.create(login = 'козявка', password = 'бибзявка', image= 'xyi')
        self.user.cart.set([])
        self.order = Order.objects.create(number = 12, delivery_date ='2024-06-04', owner = self.user, products = self.user)
        
    def test_create(self):
        data = {'name':'pyki kaki', 'description':'fdfgdgdg', 'category': self.category.pk, 'rating': 2, 'image':'fgfhgf', 'price':777}
        response = self.client.post('/magazine_api/product/', data, content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 200)        
        
    def test_update(self):
        data = urlencode({'name':'gnida','description':'жи есть', 'category':self.category.pk, 'rating':1, 'image':'xyi', 'price':99999})
        response = self.client.put(reverse('product-detail', kwargs={'pk':self.product.pk}), data, content_type="application/x-www-form-urlencoded")
        updated_product = Product.objects.get(pk = self.product.pk)
        self.assertEqual(updated_product.name, 'gnida')
        self.assertEqual(updated_product.description, 'жи есть')
        self.assertEqual(updated_product.category, self.category)
        self.assertEqual(updated_product.rating, 1)
        self.assertEqual(updated_product.image, 'xyi')
        self.assertEqual(updated_product.price, 99999)
        
    def test_delete(self):
        response = self.client.delete(reverse('product-detail', kwargs={'pk':self.product.pk}))
        self.assertEqual(response.status_code, 204)
        
    def test_product_search(self):
        data = {'q': self.product.name}
        response = self.client.get(reverse('product-products-search'), data)
        # self.assertEqual(response.status_code, 200)
        self.assertIn(self.product.description, response.content.decode())
        
    def test_search_by_category(self):
        data = {'category': self.category.pk}
        response = self.client.get(reverse('product-search-by-category'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product.name, response.content.decode())
        self.assertIn(self.product2.name, response.content.decode())
        
    def test_del_product(self):
        data = {'id':self.user.pk, 'name': self.product.name}
        response = self.client.get(reverse('user-del-product'), data)
        self.assertTrue(str(self.product2.pk) in response.content.decode())
        
    def test_add_to_cart(self):
        data = {'id': self.user.pk, 'q':self.product2.pk}
        response = self.client.get(reverse('user-add-to-cart'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str(self.product2.pk), response.content.decode())
        
    def test_get_orders(self):
        data = {'id':self.user.pk}
        response = self.client.get(reverse('user-get-orders'), data)
        self.assertIn(self.order.delivery_date, response.content.decode())
# Create your tests here.
