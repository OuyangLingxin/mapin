import os
import server
import model
from datetime import datetime
from randomuser import RandomUser
import random_address
import json
from random import randint

os.system("dropdb mapin")
os.system("createdb mapin")
model.connect_to_db(server.app)
model.db.create_all()

userList = RandomUser.generate_users(10, {'nat':'us'})

with open('data/order.json') as o:
    order_data = json.loads(o.read())

with open('data/warehouse.json') as w:
    warehouse_data = json.loads(w.read())

users = []
addresses = []

orders_delivered = randint(100, 500)

for user in userList:
    name = user.get_full_name()
    cell = user.get_cell()
    email = user.get_email()
    password = user.get_password()
    orders_delivered = orders_delivered
    newUser = model.Employee(employee_name = name, employee_cell = cell, employee_email=email, employee_password=password, employee_total_packages_delivered=orders_delivered)
    users.append(newUser)

    coordinates = random_address.real_random_address_by_state('CA')
    lat = coordinates["coordinates"]["lat"]
    lng = coordinates["coordinates"]["lng"]
    address = model.Address(lat=lat, lng=lng)
    addresses.append(address)

orders = []
for order in order_data:
    order_status = order["order_status"]
    employee_id = order["employee_id"]
    warehouse_id = order["warehouse_id"]
    order = model.Order(order_status=order_status, employee_id=employee_id, warehouse_id=warehouse_id)
    orders.append(order)

warehouses = []
for warehouse in warehouse_data:
    warehouse_name = warehouse['warehouse_name']
    warehouse_location = warehouse["warehouse_location"]
    warehouse_lat = warehouse['coord']['lat']
    warehouse_lng = warehouse['coord']['lng']
    warehouse = model.Warehouse(warehouse_name=warehouse_name, warehouse_location=warehouse_location, warehouse_lat=warehouse_lat, warehouse_lng=warehouse_lng)
    warehouses.append(warehouse)








model.db.session.add_all(users)
# model.db.session.commit()
model.db.session.add_all(addresses)
# model.db.session.commit()
model.db.session.add_all(orders)
# model.db.session.commit()
model.db.session.add_all(warehouses)
model.db.session.commit()

