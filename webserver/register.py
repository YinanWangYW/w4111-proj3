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
    cursor = g.conn.execute("SELECT email,password,first_name,last_name FROM customers_live_in")
    customers = {}
    username = {}
    for result in cursor:
        # emails.append(result['email'])  # can also be accessed using result[0]
        customers[result['email']] = result['password']

        useremail = result['email']
        username[useremail] = result['first_name'] + str(' ') + result['last_name']

        # username[result['email']] = result['first_name'] + str(' ') + result['last_name']

    cursor.close()
    print(customers)
    print(username)

    # judge
    if email in customers.keys():
        if password == customers[email]:
            for k,v in username.items():
                if k == email:
                    name = v
                else:
                    continue
            print(name)
            return render_template('mainpage.html', name=name)
        else:
            return render_template('passworderror.html')
    else:
        return render_template('emailerror.html')


@app.route('/logoutpage', methods=['POST'])
def logout():
    return redirect('loginpage')


# @app.route('/logoutpage', methods=['POST'])
# def logout():
#     return redirect('loginpage')


@app.route('/mainpage')
def mainpage():
    return render_template('mainpage.html')


@app.route('/planselection', methods=['POST'])
def planselection():
    print(request.args)

    # get email and password from login form
    chosen_diet_plan_id = request.form['diet_plan_id']
    chosen_fitness_plan_id = request.form['fitness_plan_id']
    print(chosen_diet_plan_id, chosen_fitness_plan_id)
    return render_template('mainpage.html',a=chosen_diet_plan_id,b=chosen_fitness_plan_id)


@app.route('/dietplanpage')
def dietplanpage():
    # print(request.args)

    # could use dict, but bug
    #line1
    cursor = g.conn.execute("SELECT * FROM diet_plan WHERE diet_plan_id=1")
    dietplan1 = []
    for result in cursor:
        dietplan1.append(result['diet_plan_id'])  # can also be accessed using result[0]
        dietplan1.append(result['diet_plan_name'])
        dietplan1.append(result['breakfast'])
        dietplan1.append(result['lunch'])
        dietplan1.append(result['dinner'])
        dietplan1.append(result['expected_calorie_input'])
    cursor.close()
    print(dietplan1)
    diet_plan_1 = dict( dietplan1 = dietplan1 )
    print(diet_plan_1)
    # return render_template('dietplanpage.html', **diet_plan_1)

    #line2
    cursor = g.conn.execute("SELECT * FROM diet_plan WHERE diet_plan_id=2")
    dietplan2 = []
    for result in cursor:
        dietplan2.append(result['diet_plan_id'])  # can also be accessed using result[0]
        dietplan2.append(result['diet_plan_name'])
        dietplan2.append(result['breakfast'])
        dietplan2.append(result['lunch'])
        dietplan2.append(result['dinner'])
        dietplan2.append(result['expected_calorie_input'])
    cursor.close()
    # print(dietplan2)
    diet_plan_2 = dict( dietplan2 = dietplan2 )
    # print(diet_plan_2)

    #line3
    cursor = g.conn.execute("SELECT * FROM diet_plan WHERE diet_plan_id=3")
    dietplan3 = []
    for result in cursor:
        dietplan3.append(result['diet_plan_id'])  # can also be accessed using result[0]
        dietplan3.append(result['diet_plan_name'])
        dietplan3.append(result['breakfast'])
        dietplan3.append(result['lunch'])
        dietplan3.append(result['dinner'])
        dietplan3.append(result['expected_calorie_input'])
    cursor.close()

    diet_plan_3 = dict( dietplan3 = dietplan3 )

    # return render_template('dietplanpage.html', **diet_plan_1, **diet_plan_2, **diet_plan_3)

    #line4
    cursor = g.conn.execute("SELECT * FROM diet_plan WHERE diet_plan_id=4")
    dietplan4 = []
    for result in cursor:
        dietplan4.append(result['diet_plan_id'])  # can also be accessed using result[0]
        dietplan4.append(result['diet_plan_name'])
        dietplan4.append(result['breakfast'])
        dietplan4.append(result['lunch'])
        dietplan4.append(result['dinner'])
        dietplan4.append(result['expected_calorie_input'])
    cursor.close()

    diet_plan_4 = dict( dietplan4 = dietplan4 )

    # return render_template('dietplanpage.html', **diet_plan_1, **diet_plan_2, **diet_plan_3, **diet_plan_4)

    #line5
    cursor = g.conn.execute("SELECT * FROM diet_plan WHERE diet_plan_id=5")
    dietplan5 = []
    for result in cursor:
        dietplan5.append(result['diet_plan_id'])  # can also be accessed using result[0]
        dietplan5.append(result['diet_plan_name'])
        dietplan5.append(result['breakfast'])
        dietplan5.append(result['lunch'])
        dietplan5.append(result['dinner'])
        dietplan5.append(result['expected_calorie_input'])
    cursor.close()

    diet_plan_5 = dict( dietplan5 = dietplan5)

    # return render_template('dietplanpage.html', **diet_plan_1, **diet_plan_2, **diet_plan_3, **diet_plan_4, **diet_plan_5)

    #line6
    cursor = g.conn.execute("SELECT * FROM diet_plan WHERE diet_plan_id=6")
    dietplan6 = []
    for result in cursor:
        dietplan6.append(result['diet_plan_id'])  # can also be accessed using result[0]
        dietplan6.append(result['diet_plan_name'])
        dietplan6.append(result['breakfast'])
        dietplan6.append(result['lunch'])
        dietplan6.append(result['dinner'])
        dietplan6.append(result['expected_calorie_input'])
    cursor.close()

    diet_plan_6 = dict( dietplan6 = dietplan6)

    # return render_template('dietplanpage.html', **diet_plan_1, **diet_plan_2, **diet_plan_3, **diet_plan_4, **diet_plan_5, **diet_plan_6)

    #line7
    cursor = g.conn.execute("SELECT * FROM diet_plan WHERE diet_plan_id=7")
    dietplan7 = []
    for result in cursor:
        dietplan7.append(result['diet_plan_id'])  # can also be accessed using result[0]
        dietplan7.append(result['diet_plan_name'])
        dietplan7.append(result['breakfast'])
        dietplan7.append(result['lunch'])
        dietplan7.append(result['dinner'])
        dietplan7.append(result['expected_calorie_input'])
    cursor.close()

    diet_plan_7 = dict( dietplan7 = dietplan7)

    # return render_template('dietplanpage.html', **diet_plan_1, **diet_plan_2, **diet_plan_3, **diet_plan_4, **diet_plan_5, **diet_plan_6, **diet_plan_7)

    #line8
    cursor = g.conn.execute("SELECT * FROM diet_plan WHERE diet_plan_id=8")
    dietplan8 = []
    for result in cursor:
        dietplan8.append(result['diet_plan_id'])  # can also be accessed using result[0]
        dietplan8.append(result['diet_plan_name'])
        dietplan8.append(result['breakfast'])
        dietplan8.append(result['lunch'])
        dietplan8.append(result['dinner'])
        dietplan8.append(result['expected_calorie_input'])
    cursor.close()

    diet_plan_8 = dict( dietplan8 = dietplan8)

    #line9
    cursor = g.conn.execute("SELECT * FROM diet_plan WHERE diet_plan_id=9")
    dietplan9 = []
    for result in cursor:
        dietplan9.append(result['diet_plan_id'])  # can also be accessed using result[0]
        dietplan9.append(result['diet_plan_name'])
        dietplan9.append(result['breakfast'])
        dietplan9.append(result['lunch'])
        dietplan9.append(result['dinner'])
        dietplan9.append(result['expected_calorie_input'])
    cursor.close()

    diet_plan_9 = dict( dietplan9 = dietplan9)

    # return render_template('dietplanpage.html', **diet_plan_1, **diet_plan_2, **diet_plan_3, **diet_plan_4, **diet_plan_5,
    #                        **diet_plan_6, **diet_plan_7, **diet_plan_8, **diet_plan_9)

    #line10
    cursor = g.conn.execute("SELECT * FROM diet_plan WHERE diet_plan_id=10")
    dietplan10 = []
    for result in cursor:
        dietplan10.append(result['diet_plan_id'])  # can also be accessed using result[0]
        dietplan10.append(result['diet_plan_name'])
        dietplan10.append(result['breakfast'])
        dietplan10.append(result['lunch'])
        dietplan10.append(result['dinner'])
        dietplan10.append(result['expected_calorie_input'])
    cursor.close()

    diet_plan_10 = dict( dietplan10 = dietplan10)

    return render_template('dietplanpage.html', **diet_plan_1, **diet_plan_2, **diet_plan_3, **diet_plan_4, **diet_plan_5,
                           **diet_plan_6, **diet_plan_7, **diet_plan_8, **diet_plan_9, **diet_plan_10)



@app.route('/fitnessplanpage')
def fitnessplanpage():
    # print(request.args)

    # could use dict, but bug
    #line1
    cursor = g.conn.execute("SELECT * FROM fitness_plan WHERE fitness_plan_id=1")
    fitnessplan1 = []
    for result in cursor:
        fitnessplan1.append(result['fitness_plan_id'])  # can also be accessed using result[0]
        fitnessplan1.append(result['fitness_plan_name'])
        fitnessplan1.append(result['days_in_week'])
        fitnessplan1.append(result['training_day'])
        fitnessplan1.append(result['training_time'])
        fitnessplan1.append(result['parts'])
        fitnessplan1.append(result['expected_calorie_consumption'])
        fitnessplan1.append(result['music'])
    cursor.close()
    # print(fitnessplan1)
    fitness_plan_1 = dict( fitnessplan1 = fitnessplan1 )
    # print(fitness_plan_1)
    # return render_template('fitnessplanpage.html', **fitness_plan_1)

    # #line2
    cursor = g.conn.execute("SELECT * FROM fitness_plan WHERE fitness_plan_id=2")
    fitnessplan2 = []
    for result in cursor:
        fitnessplan2.append(result['fitness_plan_id'])  # can also be accessed using result[0]
        fitnessplan2.append(result['fitness_plan_name'])
        fitnessplan2.append(result['days_in_week'])
        fitnessplan2.append(result['training_day'])
        fitnessplan2.append(result['training_time'])
        fitnessplan2.append(result['parts'])
        fitnessplan2.append(result['expected_calorie_consumption'])
        fitnessplan2.append(result['music'])
    cursor.close()
    # print(fitnessplan1)
    fitness_plan_2 = dict( fitnessplan2 = fitnessplan2 )
    # print(fitness_plan_1)
    # return render_template('fitnessplanpage.html', **fitness_plan_1,)
    #
    # #line3
    cursor = g.conn.execute("SELECT * FROM fitness_plan WHERE fitness_plan_id=3")
    fitnessplan3 = []
    for result in cursor:
        fitnessplan3.append(result['fitness_plan_id'])  # can also be accessed using result[0]
        fitnessplan3.append(result['fitness_plan_name'])
        fitnessplan3.append(result['days_in_week'])
        fitnessplan3.append(result['training_day'])
        fitnessplan3.append(result['training_time'])
        fitnessplan3.append(result['parts'])
        fitnessplan3.append(result['expected_calorie_consumption'])
        fitnessplan3.append(result['music'])
    cursor.close()
    # print(fitnessplan1)
    fitness_plan_3 = dict( fitnessplan3 = fitnessplan3 )
    # print(fitness_plan_1)
    # return render_template('fitnessplanpage.html', **fitness_plan_1,)
    #
    # #line4
    cursor = g.conn.execute("SELECT * FROM fitness_plan WHERE fitness_plan_id=4")
    fitnessplan4 = []
    for result in cursor:
        fitnessplan4.append(result['fitness_plan_id'])  # can also be accessed using result[0]
        fitnessplan4.append(result['fitness_plan_name'])
        fitnessplan4.append(result['days_in_week'])
        fitnessplan4.append(result['training_day'])
        fitnessplan4.append(result['training_time'])
        fitnessplan4.append(result['parts'])
        fitnessplan4.append(result['expected_calorie_consumption'])
        fitnessplan4.append(result['music'])
    cursor.close()
    # print(fitnessplan1)
    fitness_plan_4 = dict( fitnessplan4 = fitnessplan4 )
    # print(fitness_plan_1)
    # return render_template('fitnessplanpage.html', **fitness_plan_1,)
    #
    # #line5
    cursor = g.conn.execute("SELECT * FROM fitness_plan WHERE fitness_plan_id=5")
    fitnessplan5 = []
    for result in cursor:
        fitnessplan5.append(result['fitness_plan_id'])  # can also be accessed using result[0]
        fitnessplan5.append(result['fitness_plan_name'])
        fitnessplan5.append(result['days_in_week'])
        fitnessplan5.append(result['training_day'])
        fitnessplan5.append(result['training_time'])
        fitnessplan5.append(result['parts'])
        fitnessplan5.append(result['expected_calorie_consumption'])
        fitnessplan5.append(result['music'])
    cursor.close()
    # print(fitnessplan1)
    fitness_plan_5 = dict( fitnessplan5 = fitnessplan5 )
    # print(fitness_plan_1)
    # return render_template('fitnessplanpage.html', **fitness_plan_1,)
    #
    # #line6
    cursor = g.conn.execute("SELECT * FROM fitness_plan WHERE fitness_plan_id=6")
    fitnessplan6 = []
    for result in cursor:
        fitnessplan6.append(result['fitness_plan_id'])  # can also be accessed using result[0]
        fitnessplan6.append(result['fitness_plan_name'])
        fitnessplan6.append(result['days_in_week'])
        fitnessplan6.append(result['training_day'])
        fitnessplan6.append(result['training_time'])
        fitnessplan6.append(result['parts'])
        fitnessplan6.append(result['expected_calorie_consumption'])
        fitnessplan6.append(result['music'])
    cursor.close()
    # print(fitnessplan1)
    fitness_plan_6 = dict( fitnessplan6 = fitnessplan6 )
    # print(fitness_plan_1)
    # return render_template('fitnessplanpage.html', **fitness_plan_1,)
    #
    # #line7
    cursor = g.conn.execute("SELECT * FROM fitness_plan WHERE fitness_plan_id=7")
    fitnessplan7 = []
    for result in cursor:
        fitnessplan7.append(result['fitness_plan_id'])  # can also be accessed using result[0]
        fitnessplan7.append(result['fitness_plan_name'])
        fitnessplan7.append(result['days_in_week'])
        fitnessplan7.append(result['training_day'])
        fitnessplan7.append(result['training_time'])
        fitnessplan7.append(result['parts'])
        fitnessplan7.append(result['expected_calorie_consumption'])
        fitnessplan7.append(result['music'])
    cursor.close()
    # print(fitnessplan1)
    fitness_plan_7 = dict( fitnessplan7 = fitnessplan7 )
    # print(fitness_plan_1)
    # return render_template('fitnessplanpage.html', **fitness_plan_1,)
    #
    # #line8
    cursor = g.conn.execute("SELECT * FROM fitness_plan WHERE fitness_plan_id=8")
    fitnessplan8 = []
    for result in cursor:
        fitnessplan8.append(result['fitness_plan_id'])  # can also be accessed using result[0]
        fitnessplan8.append(result['fitness_plan_name'])
        fitnessplan8.append(result['days_in_week'])
        fitnessplan8.append(result['training_day'])
        fitnessplan8.append(result['training_time'])
        fitnessplan8.append(result['parts'])
        fitnessplan8.append(result['expected_calorie_consumption'])
        fitnessplan8.append(result['music'])
    cursor.close()
    # print(fitnessplan1)
    fitness_plan_8 = dict( fitnessplan8 = fitnessplan8 )
    # print(fitness_plan_1)
    # return render_template('fitnessplanpage.html', **fitness_plan_1,)
    #
    # #line9
    cursor = g.conn.execute("SELECT * FROM fitness_plan WHERE fitness_plan_id=9")
    fitnessplan9 = []
    for result in cursor:
        fitnessplan9.append(result['fitness_plan_id'])  # can also be accessed using result[0]
        fitnessplan9.append(result['fitness_plan_name'])
        fitnessplan9.append(result['days_in_week'])
        fitnessplan9.append(result['training_day'])
        fitnessplan9.append(result['training_time'])
        fitnessplan9.append(result['parts'])
        fitnessplan9.append(result['expected_calorie_consumption'])
        fitnessplan9.append(result['music'])
    cursor.close()
    # print(fitnessplan1)
    fitness_plan_9 = dict( fitnessplan9 = fitnessplan9 )
    # print(fitness_plan_1)
    # return render_template('fitnessplanpage.html', **fitness_plan_1,)
    #
    # #line10
    cursor = g.conn.execute("SELECT * FROM fitness_plan WHERE fitness_plan_id=10")
    fitnessplan10 = []
    for result in cursor:
        fitnessplan10.append(result['fitness_plan_id'])  # can also be accessed using result[0]
        fitnessplan10.append(result['fitness_plan_name'])
        fitnessplan10.append(result['days_in_week'])
        fitnessplan10.append(result['training_day'])
        fitnessplan10.append(result['training_time'])
        fitnessplan10.append(result['parts'])
        fitnessplan10.append(result['expected_calorie_consumption'])
        fitnessplan10.append(result['music'])
    cursor.close()
    # print(fitnessplan1)
    fitness_plan_10 = dict( fitnessplan10 = fitnessplan10 )
    # print(fitness_plan_1)





    #line1
    cursor = g.conn.execute("SELECT * FROM coaches_provide WHERE coach_id=1")
    coachplan1 = []
    for result in cursor:
        coachplan1.append(result['coach_id'])  # can also be accessed using result[0]
        coachplan1.append(result['name'])
        coachplan1.append(result['height'])
        coachplan1.append(result['weight'])
        coachplan1.append(result['age'])

    cursor.close()
    coach_plan_1 = dict( coachplan1 = coachplan1 )
    # print(fitness_plan_1)
    # return render_template('fitnessplanpage.html', **fitness_plan_1, **fitness_plan_2, **fitness_plan_3, **fitness_plan_4, **fitness_plan_5,
    #                        **fitness_plan_6, **fitness_plan_7, **fitness_plan_8, **fitness_plan_9, **fitness_plan_10, **coach_plan_1)

    # # #line2
    cursor = g.conn.execute("SELECT * FROM coaches_provide WHERE coach_id=2")
    coachplan2 = []
    for result in cursor:
        coachplan2.append(result['coach_id'])  # can also be accessed using result[0]
        coachplan2.append(result['name'])
        coachplan2.append(result['height'])
        coachplan2.append(result['weight'])
        coachplan2.append(result['age'])

    cursor.close()
    coach_plan_2 = dict( coachplan2 = coachplan2 )
    # #
    # # #line3
    cursor = g.conn.execute("SELECT * FROM coaches_provide WHERE coach_id=3")
    coachplan3 = []
    for result in cursor:
        coachplan3.append(result['coach_id'])  # can also be accessed using result[0]
        coachplan3.append(result['name'])
        coachplan3.append(result['height'])
        coachplan3.append(result['weight'])
        coachplan3.append(result['age'])

    cursor.close()
    coach_plan_3 = dict( coachplan3 = coachplan3 )
    # #
    # # #line4
    cursor = g.conn.execute("SELECT * FROM coaches_provide WHERE coach_id=4")
    coachplan4 = []
    for result in cursor:
        coachplan4.append(result['coach_id'])  # can also be accessed using result[0]
        coachplan4.append(result['name'])
        coachplan4.append(result['height'])
        coachplan4.append(result['weight'])
        coachplan4.append(result['age'])

    cursor.close()
    coach_plan_4 = dict( coachplan4 = coachplan4 )
    # #
    # # #line5
    cursor = g.conn.execute("SELECT * FROM coaches_provide WHERE coach_id=5")
    coachplan5 = []
    for result in cursor:
        coachplan5.append(result['coach_id'])  # can also be accessed using result[0]
        coachplan5.append(result['name'])
        coachplan5.append(result['height'])
        coachplan5.append(result['weight'])
        coachplan5.append(result['age'])

    cursor.close()
    coach_plan_5 = dict( coachplan5 = coachplan5 )
    # #
    # # #line6
    cursor = g.conn.execute("SELECT * FROM coaches_provide WHERE coach_id=6")
    coachplan6 = []
    for result in cursor:
        coachplan6.append(result['coach_id'])  # can also be accessed using result[0]
        coachplan6.append(result['name'])
        coachplan6.append(result['height'])
        coachplan6.append(result['weight'])
        coachplan6.append(result['age'])

    cursor.close()
    coach_plan_6 = dict( coachplan6 = coachplan6 )
    # #
    # # #line7
    cursor = g.conn.execute("SELECT * FROM coaches_provide WHERE coach_id=7")
    coachplan7 = []
    for result in cursor:
        coachplan7.append(result['coach_id'])  # can also be accessed using result[0]
        coachplan7.append(result['name'])
        coachplan7.append(result['height'])
        coachplan7.append(result['weight'])
        coachplan7.append(result['age'])

    cursor.close()
    coach_plan_7 = dict( coachplan7 = coachplan7 )
    # #
    # # #line8
    cursor = g.conn.execute("SELECT * FROM coaches_provide WHERE coach_id=8")
    coachplan8 = []
    for result in cursor:
        coachplan8.append(result['coach_id'])  # can also be accessed using result[0]
        coachplan8.append(result['name'])
        coachplan8.append(result['height'])
        coachplan8.append(result['weight'])
        coachplan8.append(result['age'])

    cursor.close()
    coach_plan_8 = dict( coachplan8 = coachplan8 )
    # #
    # # #line9
    cursor = g.conn.execute("SELECT * FROM coaches_provide WHERE coach_id=9")
    coachplan9 = []
    for result in cursor:
        coachplan9.append(result['coach_id'])  # can also be accessed using result[0]
        coachplan9.append(result['name'])
        coachplan9.append(result['height'])
        coachplan9.append(result['weight'])
        coachplan9.append(result['age'])

    cursor.close()
    coach_plan_9 = dict( coachplan9 = coachplan9 )
    # #
    # # #line10
    cursor = g.conn.execute("SELECT * FROM coaches_provide WHERE coach_id=10")
    coachplan10 = []
    for result in cursor:
        coachplan10.append(result['coach_id'])  # can also be accessed using result[0]
        coachplan10.append(result['name'])
        coachplan10.append(result['height'])
        coachplan10.append(result['weight'])
        coachplan10.append(result['age'])

    cursor.close()
    coach_plan_10 = dict( coachplan10 = coachplan10 )
    #
    return render_template('fitnessplanpage.html', **fitness_plan_1, **fitness_plan_2, **fitness_plan_3, **fitness_plan_4, **fitness_plan_5,
                           **fitness_plan_6, **fitness_plan_7, **fitness_plan_8, **fitness_plan_9, **fitness_plan_10,
                           **coach_plan_1, **coach_plan_2, **coach_plan_3, **coach_plan_4, **coach_plan_5,
                           **coach_plan_6, **coach_plan_7, **coach_plan_8, **coach_plan_9, **coach_plan_10)





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