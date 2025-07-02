from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    _tablename_ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant', cascade='all, delete-orphan')
    
    pizzas = association_proxy('restaurant_pizzas', 'pizza',
                              creator=lambda pizza_obj: RestaurantPizza(pizza=pizza_obj))

    serialize_rules = ('-restaurant_pizzas.restaurant',)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'restaurant_pizzas': [rp.to_dict() for rp in self.restaurant_pizzas]
        }

    def _repr_(self):
        return f'<Restaurant {self.name}>'


class Pizza(db.Model, SerializerMixin):
    _tablename_ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza', cascade='all, delete-orphan')
    
    restaurants = association_proxy('restaurant_pizzas', 'restaurant',
                                  creator=lambda restaurant_obj: RestaurantPizza(restaurant=restaurant_obj))

    serialize_rules = ('-restaurant_pizzas.pizza',)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients
        }

    def _repr_(self):
        return f'<Pizza {self.name}>'


class RestaurantPizza(db.Model, SerializerMixin):
    _tablename_ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    serialize_rules = ('-restaurant.restaurant_pizzas', '-pizza.restaurant_pizzas',)

    @validates('price')
    def validate_price(self, key, price):
        if price is None:
            raise ValueError("Price is required")
        if not isinstance(price, int):
            raise ValueError("Price must be an integer")
        if price < 1 or price > 30:
            raise ValueError("Price must be between 1 and 30")
        return price

    def to_dict(self):
        return {
            'id': self.id,
            'price': self.price,
            'pizza_id': self.pizza_id,
            'restaurant_id': self.restaurant_id,
            'pizza': self.pizza.to_dict(),
            'restaurant': {
                'id': self.restaurant.id,
                'name': self.restaurant.name,
                'address': self.restaurant.address
            }
        }

    def _repr_(self):
        return f'<RestaurantPizza {self.restaurant.name} - {self.pizza.name} - ${self.price}>'