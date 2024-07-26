from flask import Blueprint
from flask import jsonify, request, send_file
from .models import *
from io import BytesIO, StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import pandas as pd

views = Blueprint('views', __name__)



@views.route('/')
def home():
    return "<h1>Hello Konfhub</h1>"

@views.route('/add-get-products', methods = ['GET', 'POST'])
def manage_products():
    try:
        if request.method == 'GET':
            products = Product.query.all()
            products_list = [product.to_dict() for product in products]
            return jsonify({
                'data': products_list,
                'message': 'Products retrieved successfully',
                'status': 200,
                'success': True
            }), 200

        elif request.method == 'POST':
            data = request.json
            if not data or 'name' not in data or 'category' not in data or 'price' not in data or 'quantity' not in data:
                return jsonify({
                    'data': {},
                    'message': 'Missing required fields',
                    'status': 400,
                    'success': False
                }), 400
            product = Product(
                name=data['name'],
                category=data['category'],
                price=data['price'],
                quantity=data['quantity']
            )
            db.session.add(product)
            db.session.commit()

            return jsonify({
                'data': {},
                'message': 'Product added successfully',
                'status': 201,
                'success': True
            }), 201
    except Exception as e:
        return jsonify({
            'data': {},
            'message': str(e),
            'status': 500,
            'success': False
        }), 500
        
@views.route('/update-delete-product/<int:product_id>', methods=['PUT', 'DELETE'])
def update_delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({
                'data': {},
                'message': 'Product not found',
                'status': 404,
                'success': False
            }), 404
            
        if request.method == 'PUT':
            data = request.json
            if 'name' in data:
                product.name = data['name']
            if 'category' in data:
                product.category = data['category']
            if 'price' in data:
                product.price = data['price']
            if 'quantity' in data:
                product.quantity = data['quantity']

            db.session.commit()

            return jsonify({
                'data': product.to_dict(),
                'message': 'Product updated successfully',
                'status': 200,
                'success': True
            }), 200
            
        elif request.method == 'DELETE':
            db.session.delete(product)
            db.session.commit()

            return jsonify({
                'data': {},
                'message': 'Product deleted successfully',
                'status': 200,
                'success': True
            }), 200

    except Exception as e:
        return jsonify({
            'data': {},
            'message': str(e),
            'status': 500,
            'success': False
        }), 500
        
@views.route('/sales', methods=['POST'])
def record_sale():
    try:
        data = request.get_json()
        if not all(key in data for key in ('product_id', 'quantity', 'price', 'customer_id')):
            return jsonify({
                'data': {},
                'message': 'Missing required fields',
                'status': 400,
                'success': False,
                }), 400

        product = Product.query.get_or_404(data['product_id'])
        if product.quantity < data['quantity']:
            return jsonify({
                'data': {},
                'message': 'Insufficient quantity',
                'status': 400,
                'success': False,
                }), 400
        sale = Sale(
            product_id=data['product_id'],
            quantity=data['quantity'],
            price=data['price'],
            customer_id=data['customer_id']
        )
        product.quantity -= data['quantity']
        db.session.add(sale)
        db.session.commit()
        return jsonify({
                'data': sale.to_dict(),
                'message': 'Sale recorded successfully',
                'status': 201,
                'success': True,
                }), 201
    except Exception as e:
        return jsonify({
            'data': {},
            'message': str(e),
            'status': 500,
            'success': False
        }), 500
        
@views.route('/returns', methods=['POST'])
def record_return():
    try:
        data = request.get_json()

        if not all(key in data for key in ('product_id', 'quantity', 'price', 'reason')):
            return jsonify({
                'data': {},
                'message': 'Missing required fields',
                'status': 400,
                'success': False
            }), 400
        product = Product.query.get_or_404(data['product_id'])
        return_record = Return(
            product_id=data['product_id'],
            quantity=data['quantity'],
            price=data['price'],
            reason=data['reason']
        )
        product.quantity += data['quantity']
        db.session.add(return_record)
        db.session.commit()
        return jsonify({
                'data': return_record.to_dict(),
                'message': 'Return recorded successfully',
                'status': 201,
                'success': True
            }), 201
    except Exception as e:
        return jsonify({
            'data': {},
            'message': str(e),
            'status': 500,
            'success': False
        }), 500
        
@views.route('/invoices/generate', methods=['POST'])
def generate_invoice():
    try:
        data = request.get_json()
        sales = Sale.query.filter(Sale.id.in_(data['sale_ids'])).all()
        if not sales:
            return jsonify({
                'data': {},
                'message': 'No sales found for the given IDs',
                'status': 404,
                'success': False
            }), 404

        invoice = Invoice()
        invoice.transactions = sales
        invoice.total_amount = sum(sale.price * sale.quantity for sale in sales)
        db.session.add(invoice)
        db.session.commit()
        
        file_stream = BytesIO()
        c = canvas.Canvas(file_stream, pagesize=letter)
        c.drawString(100, 750, f"Invoice ID: {invoice.id}")
        c.drawString(100, 730, f"Date: {invoice.date.strftime('%Y-%m-%d')}")
        y = 710
        for sale in invoice.transactions:
            c.drawString(100, y, f"Product ID: {sale.product_id}, Quantity: {sale.quantity}, Price: {sale.price}")
            y -= 20
        c.drawString(100, y, f"Total Amount: {invoice.total_amount}")
        c.save()
        
        file_stream.seek(0)
        file_name = f'invoice_{invoice.id}.pdf'
        local_file = os.path.join('Invoices', file_name)
        with open(local_file, 'wb') as f:
            f.write(file_stream.getbuffer())
            
        file_stream.seek(0)
        return send_file(
            file_stream,
            as_attachment=True,
            download_name=file_name,
            mimetype='application/pdf'
        )

    except Exception as e:
        return jsonify({
            'data': {},
            'message': str(e),
            'status': 500,
            'success': False
        }), 500
        
@views.route('/export_csv', methods=['GET'])
def export_csv():
    try:
        product_id = request.args.get('product_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        transaction_type = request.args.get('type')

        query = db.session.query(Transaction)

        if product_id:
            query = query.filter(Transaction.product_id == product_id)
        if start_date:
            query = query.filter(Transaction.date >= datetime.strptime(start_date, '%Y-%m-%d'))
        if end_date:
            query = query.filter(Transaction.date <= datetime.strptime(end_date, '%Y-%m-%d'))
        if transaction_type:
            query = query.filter(Transaction.type == transaction_type)

        transactions = query.all()
        transactions_data = [trans.to_dict() for trans in transactions]

        df = pd.DataFrame(transactions_data)
        
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        local_file_path = '/var/www/DJProject/AIMSI/CSV/transactions.csv'
        with open(local_file_path, 'wb') as f:
            f.write(csv_buffer.getvalue())
        return send_file(
            csv_buffer,
            mimetype='text/csv',
            as_attachment=True,
            download_name='transactions.csv'
        )
    except Exception as e:
        return jsonify({
            'data': {},
            'message': str(e),
            'status': 500,
            'success': False
        }), 500