import unittest
from webapp import create_app, db
from webapp.models import Product, Sale, Return, Invoice

class ViewsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()  
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()  
        
    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all() 
        cls.app_context.pop()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello Konfhub', response.data)

    def test_manage_products_get(self):
        response = self.client.get('/add-get-products')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('data', data)
        self.assertEqual(data['status'], 200)

    def test_manage_products_post(self):
        """Test adding a new product"""
        response = self.client.post('/add-get-products', json={
            'name': 'Test Product',
            'category': 'Test Category',
            'price': 50.0,
            'quantity': 100
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'Product added successfully')

    def test_update_product(self):
        product = Product(name='Update Product', category='Old Category', price=30.0, quantity=50)
        db.session.add(product)
        db.session.commit()

        response = self.client.put(f'/update-delete-product/{product.id}', json={
            'name': 'Updated Product',
            'category': 'New Category'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Product updated successfully')

    def test_delete_product(self):
        product = Product(name='Delete Product', category='Delete Category', price=20.0, quantity=10)
        db.session.add(product)
        db.session.commit()

        response = self.client.delete(f'/update-delete-product/{product.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Product deleted successfully')

    def test_record_sale(self):
        product = Product(name='Sale Product', category='Sale Category', price=50.0, quantity=100)
        db.session.add(product)
        db.session.commit()

        response = self.client.post('/sales', json={
            'product_id': product.id,
            'quantity': 5,
            'price': 50.0,
            'customer_id': 1
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'Sale recorded successfully')

    def test_record_return(self):
        product = Product(name='Return Product', category='Return Category', price=30.0, quantity=20)
        db.session.add(product)
        db.session.commit()

        response = self.client.post('/returns', json={
            'product_id': product.id,
            'quantity': 3,
            'price': 30.0,
            'reason': 'Defective'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'Return recorded successfully')

    def test_generate_invoice(self):
        product = Product(name='Invoice Product', category='Invoice Category', price=40.0, quantity=50)
        db.session.add(product)
        db.session.commit()

        sale = Sale(product_id=product.id, quantity=10, price=40.0, customer_id=1)
        db.session.add(sale)
        db.session.commit()

        response = self.client.post('/invoices/generate', json={
            'sale_ids': [sale.id]
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/pdf')

    def test_export_csv(self):
        product = Product(name='CSV Product', category='CSV Category', price=60.0, quantity=30)
        db.session.add(product)
        db.session.commit()

        sale = Sale(product_id=product.id, quantity=7, price=60.0, customer_id=1)
        db.session.add(sale)
        db.session.commit()

        response = self.client.get('/export_csv', query_string={
            'product_id': product.id,
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'type': 'sale'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/csv')

if __name__ == '__main__':
    unittest.main()
