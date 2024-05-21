from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Aravind9740/123'
app.config['MYSQL_DB'] = 'task_management'

mysql = MySQL(app)

# Routes
@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        address = request.form['address']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, mobile, password, address) VALUES (%s, %s, %s, %s, %s)", (name, email, mobile, password, address))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            return redirect(url_for('dashboard'))
        else:
            return jsonify({'message': 'Login failed. Invalid credentials'})
    
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Fetch all users from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM users")
    users = cur.fetchall()
    cur.close()

    # Task statuses
    task_statuses = ['Pending', 'Completed']

    return render_template('dashboard.html', users=users, task_statuses=task_statuses)

@app.route('/tasks')
def tasks():
    # Fetch all tasks from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()

    return render_template('tasks.html', tasks=tasks)

@app.route('/view-tasks')
def view_tasks():
    # Fetch all tasks from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()

    return render_template('view_tasks.html', tasks=tasks)
    
@app.route('/api/login', methods=['POST'])
def api_login():
    cur = mysql.connection.cursor()
    email = request.form['email']
    password = request.form['password']
    cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cur.fetchone()
    cur.close()
    if user:
        return jsonify({'message': 'Login successful', 'user': user})
    else:
        return jsonify({'message': 'Login failed. Invalid credentials'})

@app.route('/api/register', methods=['POST'])
def api_register():
    cur = mysql.connection.cursor()
    name = request.form['name']
    email = request.form['email']
    mobile = request.form['mobile']
    password = request.form['password']
    address = request.form['address']
    cur.execute("INSERT INTO users (name, email, mobile, password, address) VALUES (%s, %s, %s, %s, %s)", (name, email, mobile, password, address))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Register successful', 'name': name, 'email': email, 'mobile': mobile, 'address': address})

@app.route('/api/add-task', methods=['POST'])
def api_add_task():
    task_name = request.form['taskName']
    task_date = request.form['taskDate']
    task_time = request.form['taskTime']
    task_assigned_to = request.form['taskAssignedTo']
    task_status = request.form['taskStatus']

    task_datetime = datetime.strptime(task_date + ' ' + task_time, '%Y-%m-%d %H:%M')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks (task_name, task_date, task_time, task_assigned_to, task_status) VALUES (%s, %s, %s, %s, %s)", (task_name, task_date, task_time, task_assigned_to, task_status))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Task added successfully'})

    # Optionally, you could redirect to the dashboard after adding a task:
    # return redirect(url_for('dashboard'))

    

@app.route('/api/tasks')
def api_get_tasks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    task_list = []
    for task in tasks:
        task_item = {
            'id': task[0],
            'task_name': task[1],
            'task_date': task[2].strftime('%Y-%m-%d'),  # Assuming task[2] is a date object
            'task_time': str(task[3]),  
            'task_assigned_to': task[4],
            'task_status': task[5]
        }
        print(task_item)
        task_list.append(task_item)
    return render_template('tasks.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)

