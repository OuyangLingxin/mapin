from flask import Flask, render_template, request, session, flash, redirect, jsonify
from model import connect_to_db, db, Employee, Order, Warehouse, Address
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def home():
  return render_template('home.html')

@app.route('/', methods=["POST"])
def login():
  email = request.form.get('email')
  user = Employee.query.filter(Employee.employee_email == email).first()
  print(user)
  if user is None:
    flash('Try again')
    return redirect('/')
  else:
    flash("Logged In")
    return render_template('welcome.html')


@app.route('/signup')
def signup():
  return render_template('sign_up_form.html')

@app.route('/signup', methods=["POST"])
def create_account():
  email = request.form.get('email')
  password = request.form.get('password')
  admin = Employee(employee_email = email, employee_password = password)
  db.session.add(admin)
  db.session.commit()
  return redirect('/')



@app.route('/map', methods=["GET"])
def get_data():
    data = Employee.query.all()
    # print(data) # [<Employee employee_id=1 employee_name=Brooklyn Bell>, <Employee employee_id=2 employee_name=Mike Mitchell>, <Employee employee_id=3 employee_name=Michele Johnston>]
    emp_addre = []
    for employee in data:
      emp_addre.append({"lat": employee.address[0].lat, "lng": employee.address[0].lng}) #[<Address employee_id=3 lat=37.5538472 lng=-122.0122099>]
    # print(emp_addre) #[{'lat': 37.679629, 'lng': -121.739175}, {'lat': 36.5616476, 'lng': -119.6175431}, {'lat': 37.5538472, 'lng': -122.0122099}]
    return jsonify(emp_addre)
    # return render_template('map.html')



@app.route('/maps')
def map():
  return render_template('map.html')

















if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)