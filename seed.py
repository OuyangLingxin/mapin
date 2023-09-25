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

userList = RandomUser.generate_users(12, {'nat': 'us'})
print(userList)

with open('data/order.json') as o:
    order_data = json.loads(o.read())

with open('data/warehouse.json') as w:
    warehouse_data = json.loads(w.read())

users = []
addresses = []


for user in userList:
    name = user.get_full_name()
    cell = user.get_cell()
    email = user.get_email()
    password = user.get_password()
    picture = user.get_picture()
    total_delivered = randint(100, 1000)
    days_worked = randint(1, 20)
    newUser = model.Employee(employee_name=name, employee_cell=cell, employee_email=email, employee_password=password,
                             employee_total_packages_delivered=total_delivered, employee_picture=picture, employee_days_worked=days_worked)
    users.append(newUser)

    location = random_address.real_random_address_by_state('CA')
    lat = location["coordinates"]["lat"]
    lng = location["coordinates"]["lng"]
    address1 = location["address1"]
    address2 = location["address2"]
    city = location["city"]
    state = location["state"]
    postalCode = location["postalCode"]
    address = model.Address(lat=lat, lng=lng, address1=address1,
                            address2=address2, city=city, state=state, postalCode=postalCode)
    addresses.append(address)

orders = []
for order in order_data:
    order_status = order["order_status"]
    employee_id = order["employee_id"]
    warehouse_id = order["warehouse_id"]
    order = model.Order(order_status=order_status,
                        employee_id=employee_id, warehouse_id=warehouse_id)
    orders.append(order)

warehouses = []
for warehouse in warehouse_data:
    warehouse_name = warehouse['warehouse_name']
    warehouse_location = warehouse["warehouse_location"]
    warehouse_lat = warehouse['coord']['lat']
    warehouse_lng = warehouse['coord']['lng']
    warehouse = model.Warehouse(warehouse_name=warehouse_name, warehouse_location=warehouse_location,
                                warehouse_lat=warehouse_lat, warehouse_lng=warehouse_lng)
    warehouses.append(warehouse)


model.db.session.add_all(users)
model.db.session.add_all(addresses)
model.db.session.add_all(orders)
model.db.session.add_all(warehouses)
model.db.session.commit()
