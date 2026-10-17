from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# naming convention keeps migrations consistent
metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # a customer has many reviews
    reviews = db.relationship('Review', back_populates='customer')

    # items the customer reviewed, reached through reviews
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # an item has many reviews
    reviews = db.relationship('Review', back_populates='item')

    # customers who reviewed the item, reached through reviews
    customers = association_proxy('reviews', 'customer')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'


# ---------- Schemas ----------
# Foreign keys are left out because include_fk is False by default.
# Each nested field excludes the way back to its parent,
# so serializing never loops forever.

class CustomerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

    reviews = fields.Nested(lambda: ReviewSchema(exclude=('customer', 'item')), many=True)
    items = fields.Nested(lambda: ItemSchema(exclude=('reviews', 'customers')), many=True)


class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item

    reviews = fields.Nested(lambda: ReviewSchema(exclude=('customer', 'item')), many=True)
    customers = fields.Nested(lambda: CustomerSchema(exclude=('reviews', 'items')), many=True)


class ReviewSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Review

    customer = fields.Nested(lambda: CustomerSchema(exclude=('reviews', 'items')))
    item = fields.Nested(lambda: ItemSchema(exclude=('reviews', 'customers')))