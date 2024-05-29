from flask import Flask, request, jsonify,make_response
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Aravind9740/123'
app.config['MYSQL_DB'] = 'Taks'

mysql = MySQL(app)

@app.route('/')
def welcome():
    return 'Welcome'

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            response = make_response(jsonify({'message': 'Login Successful'}))
            response.set_cookie('email', email, max_age=60 * 60 * 24 * 7)
            return response
        else:
            return jsonify({'message': 'Login failed. Invalid credentials'})

@app.route('/tasks')
def tasks():
    email = request.cookies.get('email') 
    if not email:
        return jsonify({'message': 'User not logged in'})

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE email=%s", (email,))
    user = cur.fetchone()
    userName = user[2]
    cur.close()

    if not user:
        return jsonify({'message': 'User not found'})
        
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM task WHERE username=%s", (userName,))
    tasks = cur.fetchall()
    cur.close()

    if not tasks:
        return jsonify({'message': 'No tasks found for this user'})

    return jsonify({'tasks': tasks})

    

@app.route('/add-task', methods=['POST'])
def api_add_task():
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        task_name = data.get('taskName')
        task_assigned_to = data.get('taskAssignedTo')
        task_status = data.get('taskStatus')

    if not task_name or not task_assigned_to or not task_status:
        return jsonify({'error': 'All fields are required'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO task (taskName, taskAssignedTo, taskStatus, username) VALUES (%s, %s, %s, %s)", 
                    (task_name, task_assigned_to, task_status, username))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Task added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete-task', methods=['DELETE'])
def delete_task():
    userName = None
    if request.is_json:
        data = request.get_json()
        userName = data.get('username')
    else:
        userName = request.args.get('username')
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM task WHERE username=%s", (userName,))
    task = cur.fetchone()
    
    if not task:
        cur.close()
        return jsonify({'message': 'Task not found for the given userName'}), 404
    
    cur.execute("DELETE FROM task WHERE username=%s", (userName,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Task deleted successfully'})



@app.route('/update-task', methods=['PUT'])
def update_task():
    if request.is_json:
        data = request.get_json()
        task_name = data.get('taskName')
        task_assigned_to = data.get('taskAssignedTo')
        task_status = data.get('taskStatus')
        userName = data.get('username')  

        cur = mysql.connection.cursor()
        cur.execute("UPDATE task SET taskName=%s, taskAssignedTo=%s, taskStatus=%s WHERE username=%s", 
                    (task_name, task_assigned_to, task_status, username))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Task updated successfully'})
    else:
        return jsonify({'message': 'Request must be JSON'}), 400


if __name__ == '__main__':
    app.run(debug=True)

