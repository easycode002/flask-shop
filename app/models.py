from app import db
from datetime import datetime

class User(db.Model): # One user have many address
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}  # Ensures table modifications apply

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, name="createdAt")
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, name="updatedAt")
    deletedAt = db.Column(db.DateTime, nullable=True, name="deletedAt")
    isDeleted = db.Column(db.Boolean, default=False, name="isDeleted")
    
    # Relationship
    addresses = db.relationship('UserAddress', backref='user', lazy=True)
    
class UserAddress(db.Model):
    __tablename__='user_addresses'
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    address_id=db.Column(db.Integer, primary_key=True)
    address=db.Column(db.Text, nullable=False)
    createdAt=db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt=db.Column(db.DateTime, default=datetime.utcnow)
    
class PaymentType(db.Model):
    __tablename__='payment_types'
    
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=False)
 
class Order(db.Model):
    __tablename__='orders'
    
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    payment_type_id=db.Column(db.Integer,db.ForeignKey('payment_types.id'),nullable=False)
    amount=db.Column(db.Numeric(10,2),nullable=False)
    
    # Relationship
    delivery_address=db.relationship('OrderDeliveryAddress',backref='order',uselist=False)
    billing_address=db.relationship('OrderBillingAddress',backref='order',uselist=False)

class OrderDeliveryAddress(db.Model):
    __tablename__='order_delivery_addresses'
    
    order_id=db.Column(db.Integer,db.ForeignKey('orders.id'),primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    address_id=db.Column(db.Integer,nullable=False)
    
class OrderBillingAddress(db.Model):
    __tablename__='order_billing_addresses'
    
    order_id=db.Column(db.Integer,db.ForeignKey('orders.id'),primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    address_id=db.Column(db.Integer,nullable=False)
    
    # Relationship