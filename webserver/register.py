import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


DATABASEURI = "postgresql://yw3692:6367@35.211.155.104/proj1part2"

# This line creates a database engine that knows how to connect to the URI above.
engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
    """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback;
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
    try:
        g.conn.close()
    except Exception as e:
        pass


@app.route('/')
def register_page():
    return render_template('registerpage.html')


@app.route('/register', methods=['POST'])
def register():
    print(request.args)

    cursor = g.conn.execute("SELECT address_id FROM address")
    address_ids = []
    for result in cursor:
        address_ids.append(result['address_id'])  # can also be accessed using result[0]
    cursor.close()
    print(address_ids[-1])
    address_id = address_ids[-1] + 1
    customer_id = address_id
    print(address_id, customer_id, type(address_ids), type(customer_id))

    cursor = g.conn.execute("SELECT email FROM customers_live_in")
    emails = []
    for result in cursor:
        emails.append(result['email'])  # can also be accessed using result[0]
    cursor.close()


    # cursor = g.conn.execute("SELECT email FROM address")
    # emails = []
    # for result in cursor:
    #     emails.append(result['email'])  # can also be accessed using result[0]
    # cursor.close()


    #get data from web
    first_name = request.form['first name']
    last_name = request.form['last name']
    email = request.form['email']
    age = request.form['age']
    street = request.form['street']
    apartment = request.form['apartment']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zip code']
    password = request.form['password']

    print(password)


    if email in emails:
        print(email)
        print(emails)
        return render_template('emailerror.html')
    else:
        g.conn.execute(
            """INSERT INTO address (address_id,apartment,street,city,state,zip_code) VALUES (%s,%s,%s,%s,%s,%s);""",
            (address_id, apartment, street, city, state, zip_code))
        g.conn.execute(
            """INSERT INTO customers_live_in (customer_id,address_id,email,password,first_name,last_name,age) VALUES
            (%s,%s,%s,%s,%s,%s,%s);""", (customer_id, address_id, email, password, first_name, last_name, age))

        return redirect('/registersuccess')


    # g.conn.execute(
    #     """INSERT INTO address (address_id,apartment,street,city,state,zip_code) VALUES (%s,%s,%s,%s,%s,%s);""",
    #     (address_id, apartment, street, city, state, zip_code))
    # g.conn.execute(
    #     """INSERT INTO customers_live_in (customer_id,address_id,email,password,first_name,last_name,age) VALUES
    #     (%s,%s,%s,%s,%s,%s,%s);""", (customer_id, address_id, email, password, first_name, last_name, age))
    #
    # return redirect('/registersuccess')

@app.route('/registersuccess')
def register_successfully():
    return render_template('registersuccess.html')


@app.route('/loginpage')
def loginpage():
    return render_template('loginpage.html')



@app.route('/login', methods=['POST'])
def login():
    print(request.args)

    # get email and password from login form
    email = request.form['email']
    password = request.form['password']
    print(email,password)


    # print(user)

    #get email&password from datebase
    cursor = g.conn.execute("SELECT email,password FROM customers_live_in")
    customers = {}
    for result in cursor:
        # emails.append(result['email'])  # can also be accessed using result[0]
        customers[result['email']] = result['password']
    cursor.close()
    print(customers)


    # judge
    if email in customers.keys():
        if password == customers[email]:
            return render_template('mainpage.html')
        else:
            return render_template('passworderror.html')
    else:
        return render_template('emailerror.html')


@app.route('/logoutpage', methods=['POST'])
def logout():
    return redirect('loginpage')


if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


    run()