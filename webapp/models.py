from webapp import db
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity
        }

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('transactions', lazy=True))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(50))  # Added type column for polymorphic identity

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'transaction'
    }

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price": self.price,
            "date": self.date
        }

class Sale(Transaction):
    __tablename__ = 'sale'
    id = db.Column(db.Integer, db.ForeignKey('transaction.id'), primary_key=True)
    customer_id = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'sale',
    }

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "customer_id": self.customer_id
        })
        return data

class Return(Transaction):
    __tablename__ = 'return'
    id = db.Column(db.Integer, db.ForeignKey('transaction.id'), primary_key=True)
    reason = db.Column(db.String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'return',
    }

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "reason": self.reason
        })
        return data

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transactions = db.relationship('Sale', secondary='invoice_sale', backref='invoices')
    total_amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def generate_invoice(self):
        self.total_amount = sum(sale.price * sale.quantity for sale in self.transactions)
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "transactions": [sale.to_dict() for sale in self.transactions],
            "total_amount": self.total_amount,
            "date": self.date
        }

invoice_sale = db.Table('invoice_sale',
    db.Column('invoice_id', db.Integer, db.ForeignKey('invoice.id'), primary_key=True),
    db.Column('sale_id', db.Integer, db.ForeignKey('sale.id'), primary_key=True)
)