from flask import Flask, render_template, request, session, flash, redirect, jsonify
from model import connect_to_db, db, Employee, Order, Warehouse, Address, Admin
from jinja2 import StrictUndefined
import googlemaps
from random import randint

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

gmaps = googlemaps.Client(key='AIzaSyABVLqKXuX8k_JDyL9dWR7jIZxs_XV9fhg')


@app.route('/')
def home():
  return render_template('home.html')

@app.route('/', methods=["POST"])
def login():
  email = request.form.get('email')
  user = Admin.query.filter(Admin.admin_email == email).first()
  if user is None:
    flash('Try again')
    return redirect('/')
  else:
    return redirect('/maps')

@app.route('/signup')
def signup():
  return render_template('sign_up_form.html')

@app.route('/signup', methods=["POST"])
def create_account():
  email = request.form.get('email')
  password = request.form.get('password')
  admin = Admin(admin_email = email, admin_password = password)
  db.session.add(admin)
  db.session.commit()
  return redirect('/')

@app.route('/map', methods=["GET"])
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
def get_all_employee():
    data = Employee.query.all()
    result = []
    for i in data:
      result.append({'name': i.employee_name, 'cell': i.employee_cell, 'id': i.employee_id})
    return jsonify(result)

@app.route('/newemployee')
def add_new_emp():
    return render_template('newemployee.html')

@app.route('/newemployee', methods=["POST"])
def get_new_emp_data():
    new_emp_name = request.form.get('name')
    new_emp_cell = request.form.get('cell')
    new_emp_email = request.form.get('email')
    new_emp_address = request.form.get('address')
    geocode_result = gmaps.geocode(f"'{new_emp_address}'")
    # print(geocode_result[0])
    # print(geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng'])
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    emp = Employee(employee_name = new_emp_name, employee_cell = new_emp_cell, employee_email = new_emp_email)
    db.session.add(emp)
    db.session.commit()
    new_emp = Employee.query.filter(Employee.employee_cell == new_emp_cell).first()
    new_emp_addr = Address(employee_id = new_emp.employee_id, lat = lat, lng = lng)
    db.session.add(new_emp_addr)
    db.session.commit()
    return redirect('/maps')

@app.route('/maps')
def map():
  return render_template('map.html')

@app.route('/maps/<id>')
def emp_details(id):
   emp_detail = Employee.query.get(id)
   id = id
   name = emp_detail.employee_name
   delivered = emp_detail.employee_total_packages_delivered
  #  delivered = randint(100, 500)
   return render_template('empdetails.html', name=name, id=id, delivered=delivered)


@app.route('/maps/<id>', methods=["POST"])
def delete_emp(id):
  target_emp = Employee.query.get(id)
  target_addr = Address.query.get(id)
  db.session.delete(target_emp)
  db.session.delete(target_addr)
  db.session.commit()
  #  delivered = randint(100, 500)
  return redirect('/maps')
















if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)