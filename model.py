from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_email = db.Column(db.String)
    admin_password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Admin admin_id={self.admin_id} admin_email={self.admin_email}>"

class Employee(db.Model):
    __tablename__ = 'employees'
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_email = db.Column(db.String)
    employee_password = db.Column(db.String, nullable=True)
    employee_name = db.Column(db.String)
    employee_cell = db.Column(db.String)
    employee_total_packages_delivered = db.Column(db.Integer)

    address = db.relationship('Address', back_populates='employee')
    order = db.relationship('Order', back_populates='employee')
    # warehouse = db.relationship('Warehouse', back_populates='employee')

    def __repr__(self):
        return f"<Employee employee_id={self.employee_id} employee_name={self.employee_name}>"

class Address(db.Model):
    __tablename__ = 'addresses'
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), autoincrement=True, primary_key=True)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    employee = db.relationship('Employee', back_populates='address')

    def __repr__(self):
        return f"<Address employee_id={self.employee_id} lat={self.lat} lng={self.lng}>"

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_status = db.Column(db.String)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    warehouse_id = db.Column(db.Integer)

    employee = db.relationship('Employee', back_populates='order')
    warehouse = db.relationship('Warehouse', back_populates='order')

    def __repr__(self):
        return f"<Order order_id={self.order_id} delivery_address={self.delivery_address}>"

class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    warehouse_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    warehouse_name = db.Column(db.String)
    # employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    warehouse_location = db.Column(db.String)
    warehouse_lat = db.Column(db.Float)
    warehouse_lng = db.Column(db.Float)

    # employee = db.relationship('Employee', back_populates='warehouse')
    order = db.relationship('Order', back_populates='warehouse')

    def __repr__(self):
        return f"<Warehouse warehouse_id={self.warehouse_id} warehouse_location={self.warehouse_location}>"






def connect_to_db(flask_app, db_uri="postgresql:///mapin", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app
    connect_to_db(app)