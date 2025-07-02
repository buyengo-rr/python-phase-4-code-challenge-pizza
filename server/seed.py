#!/usr/bin/env python3

from random import randint, choice as rc
from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

def seed_data():
    with app.app_context():
        print("Clearing existing data...")
        RestaurantPizza.query.delete()
        Restaurant.query.delete()
        Pizza.query.delete()
        
        print("Creating restaurants...")
        restaurants = [
            Restaurant(name="Sottocasa NYC", address="298 Atlantic Ave, Brooklyn, NY 11201"),
            Restaurant(name="PizzArte", address="69 W 55th St, New York, NY 10019"),
            Restaurant(name="Roberta's", address="261 Moore St, Brooklyn, NY 11206"),
            Restaurant(name="Emmett's", address="50 MacDougal St, New York, NY 10012"),
            Restaurant(name="Joe's Pizza", address="7 Carmine St, New York, NY 10014"),
            Restaurant(name="Lucali", address="575 Henry St, Brooklyn, NY 11231"),
            Restaurant(name="Prince Street Pizza", address="27 Prince St, New York, NY 10012"),
            Restaurant(name="Di Fara", address="1424 Ave J, Brooklyn, NY 11230"),
        ]
        
        db.session.add_all(restaurants)
        db.session.commit()
        
        print("Creating pizzas...")
        pizzas = [
            Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese"),
            Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni"),
            Pizza(name="California", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard"),
            Pizza(name="Margherita", ingredients="Dough, Tomato Sauce, Fresh Mozzarella, Basil"),
            Pizza(name="Sausage", ingredients="Dough, Tomato Sauce, Cheese, Italian Sausage"),
            Pizza(name="Mushroom", ingredients="Dough, Tomato Sauce, Cheese, Mushrooms"),
            Pizza(name="Veggie Supreme", ingredients="Dough, Tomato Sauce, Cheese, Bell Peppers, Onions, Mushrooms, Olives"),
            Pizza(name="Hawaiian", ingredients="Dough, Tomato Sauce, Cheese, Ham, Pineapple"),
            Pizza(name="Meat Lovers", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni, Sausage, Ham, Bacon"),
            Pizza(name="White Pizza", ingredients="Dough, Olive Oil, Ricotta, Mozzarella, Garlic"),
            Pizza(name="BBQ Chicken", ingredients="Dough, BBQ Sauce, Cheese, Chicken, Red Onions"),
            Pizza(name="Buffalo Chicken", ingredients="Dough, Buffalo Sauce, Cheese, Chicken, Blue Cheese"),
        ]
        
        db.session.add_all(pizzas)
        db.session.commit()
        
        print("Creating restaurant-pizza relationships...")
        restaurant_pizzas = []
        
        for restaurant in restaurants:
            num_pizzas = randint(3, 6)
            selected_pizzas = rc(pizzas, k=num_pizzas) if len(pizzas) >= num_pizzas else pizzas
            
            for pizza in selected_pizzas:
                existing = RestaurantPizza.query.filter_by(
                    restaurant_id=restaurant.id, 
                    pizza_id=pizza.id
                ).first()
                
                if not existing:
                    price = randint(10, 30)
                    restaurant_pizza = RestaurantPizza(
                        restaurant_id=restaurant.id,
                        pizza_id=pizza.id,
                        price=price
                    )
                    restaurant_pizzas.append(restaurant_pizza)
        
        for _ in range(20):
            restaurant = rc(restaurants)
            pizza = rc(pizzas)
            
            existing = RestaurantPizza.query.filter_by(
                restaurant_id=restaurant.id, 
                pizza_id=pizza.id
            ).first()
            
            if not existing:
                price = randint(1, 30)
                restaurant_pizza = RestaurantPizza(
                    restaurant_id=restaurant.id,
                    pizza_id=pizza.id,
                    price=price
                )
                restaurant_pizzas.append(restaurant_pizza)
        
        db.session.add_all(restaurant_pizzas)
        db.session.commit()
        
        print(f"✅ Seeded {len(restaurants)} restaurants")
        print(f"✅ Seeded {len(pizzas)} pizzas")
        print(f"✅ Seeded {len(restaurant_pizzas)} restaurant-pizza relationships")
        print("🌱 Database seeded successfully!")

if _name_ == '_main_':
    seed_data()