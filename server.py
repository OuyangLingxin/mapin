from flask import Flask, render_template, request, session, flash, redirect, jsonify
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from model import connect_to_db, db, Employee, Order, Warehouse, Address, Admin
from jinja2 import StrictUndefined
import googlemaps
from random import randint
import os

api_key = os.environ['api_key']

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id):
   return Admin.query.get(id)


gmaps = googlemaps.Client(key=api_key)


@app.route('/')
def home():
  return render_template('home.html')

@app.route('/', methods=["POST"])
def login():
  email = request.form.get('email')
  password = request.form.get('password')
  user = Admin.query.filter(Admin.admin_email == email).first()
  pw_hash = bcrypt.generate_password_hash(user.admin_password).decode('utf-8')
  if bcrypt.check_password_hash(pw_hash, password):
    login_user(user)
    return redirect('/maps')
  flash('Authentication Failed, Please Try Again')
  return redirect('/')

@app.route('/logout')
def logout():
  logout_user()
  return redirect('/')


@app.route('/signup')
def signup():
  return render_template('signUpForm.html')

@app.route('/signup', methods=["POST"])
def create_account():
  email = request.form.get('email')
  password = request.form.get('password')
  admin = Admin(admin_email = email, admin_password = password)
  db.session.add(admin)
  db.session.commit()
  return redirect('/')

@app.route('/maps')
@login_required
def map():
  return render_template('map.html', api_key=api_key)

@app.route('/maps/<id>')
def emp_details(id):
   emp_detail = Employee.query.get(id)
   id = id
   name = emp_detail.employee_name
   delivered = emp_detail.employee_total_packages_delivered
   picture = emp_detail.employee_picture
   return render_template('empDetails.html', name=name, id=id, delivered=delivered, picture=picture)

@app.route('/maps/<id>/edit')
@login_required
def edit_emp(id):
  target_emp = Employee.query.get(id)
  name = target_emp.employee_name
  delivered = target_emp.employee_total_packages_delivered
  cell = target_emp.employee_cell
  email = target_emp.employee_email
  target_addr = Address.query.get(id)
  address1 = target_addr.address1
  address2 = target_addr.address2
  city = target_addr.city
  state = target_addr.state
  postalCode = target_addr.postalCode
  return render_template('empEdit.html', name=name, delivered=delivered, id=id, cell=cell, email=email, address2=address2, city=city, state=state, postalCode=postalCode, address1=address1)

@app.route('/maps/<id>/edit', methods=["POST"])
@login_required
def update_emp(id):
  target_emp = Employee.query.get(id)
  target_emp_addr = Address.query.get(id)
  new_name = request.form.get('name')
  new_total = request.form.get('delivered')
  new_cell = request.form.get('cell')
  new_email = request.form.get('email')
  new_address1 = request.form.get('address1')
  new_address2 = request.form.get('address2')
  new_city = request.form.get('city')
  new_zip = request.form.get('zip')

  target_emp.employee_name = new_name
  target_emp.employee_cell = new_cell
  target_emp.employee_email = new_email
  target_emp_addr.address1 = new_address1
  target_emp_addr.address2 = new_address2
  target_emp_addr.city = new_city
  target_emp_addr.postalCode = new_zip

  target_emp.employee_total_packages_delivered = new_total

  target_emp.verified = True
  target_emp_addr.verified = True
  db.session.commit()
  return redirect('/maps')

@app.route('/maps/<id>', methods=["POST"])
@login_required
def delete_emp(id):
  target_emp = Employee.query.get(id)
  target_addr = Address.query.get(id)
  db.session.delete(target_emp)
  db.session.delete(target_addr)
  db.session.commit()
  return redirect('/maps')



@app.route('/newemployee')
@login_required
def add_new_emp():
    return render_template('newEmployee.html')

@app.route('/newemployee', methods=["POST"])
@login_required
def get_new_emp_data():
    new_emp_name = request.form.get('name')
    new_emp_cell = request.form.get('cell')
    new_emp_email = request.form.get('email')
    # new_emp_address = request.form.get('address1')
    address1 = request.form.get('address1')
    address2 = request.form.get('address2')
    city = request.form.get('city')
    state = request.form.get('state')
    zip = request.form.get('zip')
    geocode_result = gmaps.geocode(f"'{address1, city, state, zip}'")
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    emp = Employee(employee_name = new_emp_name, employee_cell = new_emp_cell, employee_email = new_emp_email)
    db.session.add(emp)
    db.session.commit()

    new_emp = Employee.query.filter(Employee.employee_cell == new_emp_cell).first()
    new_emp_addr = Address(employee_id = new_emp.employee_id, address1=address1, address2=address2, city=city, state=state, postalCode=zip, lat=lat, lng=lng)
    db.session.add(new_emp_addr)
    db.session.commit()
    return redirect('/maps')









@app.route('/map', methods=["GET"])
@login_required
def get_employee_data():
    empData = Employee.query.all()
    empDataResult = []
    for emp in empData:
      empDataResult.append({'name': emp.employee_name, 'cell': emp.employee_cell, 'id': emp.employee_id})
    # print(empDataResult)
    emp_addre = []
    for employee in empData:
      emp_addre.append({"lat": employee.address[0].lat, "lng": employee.address[0].lng, 'id': employee.address[0].employee_id})
    # print(emp_addre)
    return jsonify(empDataResult, emp_addre)


@app.route('/employee', methods=["GET"])
@login_required
def get_all_employee():
    data = Employee.query.all()
    result = []
    for i in data:
      result.append({'name': i.employee_name, 'cell': i.employee_cell, 'id': i.employee_id})
    return jsonify(result)










if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)