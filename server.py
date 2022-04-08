import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


DATABASEURI = "postgresql://yw3692:6367@35.211.155.104/proj1part2"

# This line creates a database engine that knows how to connect to the URI above.
engine = create_engine(DATABASEURI)

num = 1   #global varible -- used as customer-id, get from login
user_name = ''

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
    print("\nregister")

    # get address_id and customer_id
    cursor = g.conn.execute("SELECT address_id FROM address")
    address_ids = []
    for result in cursor:
        address_ids.append(result['address_id'])  # can also be accessed using result[0]
    cursor.close()
    # print(address_ids[-1])
    address_id = address_ids[-1] + 1
    customer_id = address_id
    print(address_id)
    # print(address_id, customer_id, type(address_ids), type(customer_id))

    # get email as unique qualification(key)
    cursor = g.conn.execute("SELECT email FROM customers_live_in")
    emails = []
    for result in cursor:
        emails.append(result['email'])  # can also be accessed using result[0]
    cursor.close()


    #get data from web
    first_name = request.form['first name']
    last_name = request.form['last name']
    email = request.form['email']
    if not '@' in email:
        emailerror = 'Please enter an valid email'
        return render_template('registerpage.html', emailerror = emailerror)
    age = request.form['age']
    if age.isdigit() == False:
        ageerror = 'Please enter with a valid format'
        return render_template('registerpage.html', ageerror=ageerror)
    street = request.form['street']
    apartment = request.form['apartment']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zip code']
    if zip_code.isdigit() == False:
        zipcodeerror = 'Please enter with a valid format'
        return render_template('registerpage.html', zipcodeerror=zipcodeerror)
    password = request.form['password']
    print(type(password))

    print(password)


    if email in emails:
        print(email)
        print(emails)
        return render_template('registererror.html')
    else:
        g.conn.execute(
            """INSERT INTO address (address_id,apartment,street,city,state,zip_code) VALUES (%s,%s,%s,%s,%s,%s);""",
            (address_id, apartment, street, city, state, zip_code))
        g.conn.execute(
            """INSERT INTO customers_live_in (customer_id,address_id,email,password,first_name,last_name,age) VALUES
            (%s,%s,%s,%s,%s,%s,%s);""", (customer_id, address_id, email, password, first_name, last_name, age))

        return redirect('/registersuccess')


@app.route('/registersuccess')
def register_successfully():
    return render_template('registersuccess.html')


@app.route('/loginpage')
def loginpage():
    return render_template('loginpage.html')



@app.route('/login', methods=['POST'])
def login():
    global num
    global user_name
    print(request.args)
    print("\nlogin")

    # get email and password from login form
    email = request.form['email']
    password = request.form['password']
    print(email,password)


    # print(user)

    #get email&password from datebase
    cursor = g.conn.execute("SELECT email,password,first_name,last_name,customer_id FROM customers_live_in")
    customers = {}
    username = {}
    decide = {}
    for result in cursor:

        # email:password key:value  customers--use to login
        customers[result['email']] = result['password']
        # email:name key:value    username--use to present username in dashboard
        useremail = result['email']
        username[useremail] = result['first_name'] + str(' ') + result['last_name']
        # email:customer_id key:value    decide--use to present customer-id for selection
        decide[result['email']] = result['customer_id']

    cursor.close()
    print(customers)
    print(username)

    # judge
    if email in customers.keys():
        if password == customers[email]:
            num = decide[email]    #get customer_id
            print(num)
            print(type(num))
            for k,v in username.items():
                if k == email:
                    name = v
                    user_name = name  #global variable -- used when access to mainpage
                else:
                    continue
            print(name)

            return redirect('/mainpage')
        else:
            return render_template('passworderror.html')
    else:
        return render_template('emailerror.html')


@app.route('/logoutpage', methods=['POST'])
def logout():
    return redirect('loginpage')



@app.route('/mainpage', methods=['GET','POST'])
def mainpage():
    print(request.args)
    if request.method == 'GET':
        show_selection1 = []
        adminid = []
        cursor = g.conn.execute("SELECT customer_id,admin_id,fitness_plan_id,diet_plan_id FROM plans_consist_of")
        for row in cursor:
            showselection1 = {}
            if row['customer_id'] == num:
                showselection1['fitness_plan_id'] = row['fitness_plan_id']
                showselection1['diet_plan_id'] = row['diet_plan_id']
                show_selection1.append(showselection1)
                adminid.append(row['admin_id'])
        cursor.close()
        context1 = dict(data1 = show_selection1)
        print('mainpage')
        print(show_selection1)
        print(adminid)
        context1 = dict(data1 = show_selection1)


        show_selection2 = []
        cursor = g.conn.execute("SELECT * FROM administration")
        for row1 in cursor:
            showselection2 = {}
            if row1['admin_id'] in adminid:
                showselection2['plan_duration'] = row1['plan_duration']
                showselection2['coach_id'] = row1['coach_id']
                show_selection2.append(showselection2)
        cursor.close()
        print(show_selection2)
        context2 = dict(data2 = show_selection2)

        return render_template("mainpage.html", **context1, **context2, name=user_name)

    if request.method == 'POST':

        show_selection1 = []
        adminid = []
        cursor = g.conn.execute("SELECT customer_id,admin_id,fitness_plan_id,diet_plan_id FROM plans_consist_of")
        for row in cursor:
            showselection1 = {}
            if row['customer_id'] == num:
                showselection1['fitness_plan_id'] = row['fitness_plan_id']
                showselection1['diet_plan_id'] = row['diet_plan_id']
                show_selection1.append(showselection1)
                adminid.append(row['admin_id'])
        cursor.close()
        context1 = dict(data1=show_selection1)
        print('mainpage')
        print(show_selection1)
        print(adminid)
        context1 = dict(data1=show_selection1)

        show_selection2 = []
        cursor = g.conn.execute("SELECT * FROM administration")
        for row1 in cursor:
            showselection2 = {}
            if row1['admin_id'] in adminid:
                showselection2['plan_duration'] = row1['plan_duration']
                showselection2['coach_id'] = row1['coach_id']
                show_selection2.append(showselection2)
        cursor.close()
        print(show_selection2)
        context2 = dict(data2=show_selection2)


        calorie_input = request.form['calorie_input']
        calorie_consumption = request.form['calorie_consumption']
        calorie_input = int(calorie_input)
        calorie_consumption = int(calorie_consumption)
        # print(calorie_input)
        # print(type(calorie_input))
        if calorie_input < 1800:
            context = 'Don’t forget eating more meat and eggs :P'
        elif calorie_input > 3500:
            context = 'You eat too much!'
        elif calorie_consumption > 800:
            context = 'You trained a lot today, remember to have a good rest :)'
        elif calorie_consumption < 200:
            context = 'Remember to exercise!'
        else:
            context = 'Well done! Keep working!'


        return render_template("mainpage.html", **context1, **context2, name=user_name, context=context)



@app.route('/planselection', methods=['POST'])
def planselection():
    print(request.args)
    print("\nselect")
    customer_id = num
    print(num)
    print('customer_id is: ')
    print(customer_id)

    # get email and password from login form
    chosen_diet_plan_id = request.form['diet_plan_id']
    # if chosen_diet_plan_id.isdigit() == False:
    #     planiderror = 'Please enter with a valid format'
    #     return render_template('registerpage.html', planiderror=planiderror)
    chosen_fitness_plan_id = request.form['fitness_plan_id']
    chosen_plan_duration = request.form['plan_duration']
    chosen_coach_id = request.form['coach_id']


    # --------------- get plan_id and admin_id ------------------
    cursor = g.conn.execute("SELECT admin_id FROM administration")
    admin_ids = []
    for result in cursor:
        admin_ids.append(result['admin_id'])  # can also be accessed using result[0]
    cursor.close()
    print('\n')
    print(admin_ids[-1])

    admin_id = admin_ids[-1] + 1
    plan_id = admin_id
    print(plan_id, admin_id)
    # --------------- get plan_id and admin_id ------------------


    g.conn.execute(
        """INSERT INTO administration (admin_id,plan_duration,coach_id) VALUES (%s,%s,%s);""",
        (admin_id, chosen_plan_duration, chosen_coach_id))
    g.conn.execute(
        """INSERT INTO plans_consist_of (plan_id,admin_id,customer_id,fitness_plan_id,diet_plan_id) VALUES
        (%s,%s,%s,%s,%s);""", (plan_id, admin_id, customer_id, chosen_fitness_plan_id, chosen_diet_plan_id))


    # print(chosen_diet_plan_id, chosen_fitness_plan_id, chosen_plan_duration,chosen_coach_id)
    return redirect('/mainpage')


# @app.route('/judgecalorie', methods=['POST'])
# def judgecalorie():
#     print(request.args)
#     print('judgecalorie')
#
#     calorie_input = request.form['calorie_input']
#     calorie_consumption = request.form['calorie_consumption']
#     calorie_input = int(calorie_input)
#     calorie_consumption = int(calorie_consumption)
#     # print(calorie_input)
#     # print(type(calorie_input))
#     if calorie_input < 1800:
#         context = 'Don’t forget eating more meat and eggs :P'
#     elif calorie_input > 3500:
#         context = 'You eat too much!'
#     elif calorie_consumption > 800:
#         context = 'You trained a lot today, remember to have a good rest :)'
#     elif calorie_consumption < 200:
#         context = 'Remember to exercise!'
#     else:
#         context = 'Well done! Keep working!'
#
#     return render_template('mainpage.html', context=context)


@app.route('/dietplanpage')
def dietplanpage():
    print(request.args)
    dietplan = []
    # diet_plan = {}       # 必须放在循环里初始化列表
    cursor = g.conn.execute("SELECT * FROM diet_plan")
    for row in cursor:
        diet_plan = {}     #一定要放这里！！！！  不然最后append结束后列表所有元素都一样，都是一个字典
        n = 0
        diet_plan['diet_plan_id'] = row['diet_plan_id']
        diet_plan['diet_plan_name'] = row['diet_plan_name']
        diet_plan['breakfast'] = row['breakfast']
        diet_plan['lunch'] = row['lunch']
        diet_plan['dinner'] = row['dinner']
        diet_plan['expected_calorie_input'] = row['expected_calorie_input']
        # print(row['diet_plan_id'],row['diet_plan_name'],row['breakfast'])
        # print(type(row['diet_plan_id']),type(row['diet_plan_name']),type(row['breakfast']))
        # print(diet_plan)
        dietplan.append(diet_plan)
    #     print(dietplan)
    # print('\n')
    # print(dietplan)
    cursor.close()
    context = dict(data=dietplan)
    # print(context)
    return render_template('dietplanpage.html', **context)



@app.route('/fitnessplanpage')
def fitnessplanpage():
    print(request.args)
    fitnessplan = []
    # fitness_plan = {}       # 必须放在循环里初始化列表
    cursor = g.conn.execute("SELECT * FROM fitness_plan")
    for row in cursor:
        fitness_plan = {}     #一定要放这里！！！！  不然最后append结束后列表所有元素都一样，都是一个字典
        fitness_plan['fitness_plan_id'] = row['fitness_plan_id']
        fitness_plan['fitness_plan_name'] = row['fitness_plan_name']
        fitness_plan['days_in_week'] = row['days_in_week']
        fitness_plan['training_day'] = row['training_day']
        fitness_plan['training_time'] = row['training_time']
        fitness_plan['parts'] = row['parts']
        fitness_plan['expected_calorie_consumption'] = row['expected_calorie_consumption']
        fitness_plan['music'] = row['music']
        fitnessplan.append(fitness_plan)

    context = dict(data=fitnessplan)
    cursor.close()


    coachplan = []
    # fitness_plan = {}       # 必须放在循环里初始化列表
    cursor = g.conn.execute("SELECT * FROM coaches_provide")
    for row in cursor:
        coach_plan = {}     #一定要放这里！！！！  不然最后append结束后列表所有元素都一样，都是一个字典
        coach_plan['coach_id'] = row['coach_id']
        coach_plan['name'] = row['name']
        coach_plan['height'] = row['height']
        coach_plan['weight'] = row['weight']
        coach_plan['age'] = row['age']
        coach_plan['fitness_plan_id'] = row['fitness_plan_id']
        coachplan.append(coach_plan)

    context1 = dict(data1=coachplan)
    cursor.close()

    return render_template('fitnessplanpage.html', **context, **context1)



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