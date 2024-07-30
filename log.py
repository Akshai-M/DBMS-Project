from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
import mysql.connector
import logging
from datetime import datetime
from mysql.connector import IntegrityError

 
app = Flask(__name__)

# Add a new route for handling search functionality


def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='username',
        password='password',
        database='databasename'
    )
def get_training_progress(employee_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM training_progress WHERE employee_id = %s', (employee_id,))
    progress = cursor.fetchall()
    conn.close()
    return progress

user_credentials = {'username': 'user', 'password': 'user123'}
admin_credentials = {'username': 'admin', 'password': 'admin123'}
# Route to display departments
@app.route('/department')
def departments():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM departments ORDER BY department_id ASC')
    departments = cursor.fetchall()
    conn.close()
    return render_template('department.html', departments=departments)
# Route to display employees
@app.route('/employee')
def employees():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees ORDER BY employee_id ASC')
    employees = cursor.fetchall()
    conn.close()
    return render_template('employee.html', employees=employees)

# Route to display courses
@app.route('/course')
def courses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Courses ORDER BY course_id ASC')
    courses = cursor.fetchall()
    conn.close()
    return render_template('course.html', courses=courses)

# Route to display instructors
@app.route('/instructors')
def instructors():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM instructors ORDER BY instructor_id ASC')
    instructors = cursor.fetchall()
    conn.close()
    return render_template('instructors.html', instructors=instructors)

# Route to display training progress
@app.route('/training_progress')
def training_progress():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM training_progress ORDER BY employee_id ASC')
    progress = cursor.fetchall()
    logging.debug("Fetched data from database: %s", progress)  # Add this line for logging
    conn.close()
    return render_template('training_progress.html', progress=progress)

@app.route('/delete_department/<department_id>', methods=['POST'])
def delete_department(department_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Delete department from the database
    cursor.execute('DELETE FROM departments WHERE department_id = %s', (department_id,))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('departments'))

# Route to delete employee
@app.route('/delete_employee/<employee_id>', methods=['POST'])
def delete_employee(employee_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Delete employee from the database
    cursor.execute('DELETE FROM employees WHERE employee_id = %s', (employee_id,))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('employees'))

# Route to delete course
@app.route('/delete_course/<course_id>', methods=['POST'])
def delete_course(course_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Delete course from the database
    cursor.execute('DELETE FROM Courses WHERE course_id = %s', (course_id,))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('courses'))

# Route to delete instructor
@app.route('/delete_instructor/<instructor_id>', methods=['POST'])
def delete_instructor(instructor_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Delete instructor from the database
    cursor.execute('DELETE FROM instructors WHERE instructor_id = %s', (instructor_id,))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('instructors'))

# Route to delete training progress
@app.route('/delete_training_progress/<progress_id>', methods=['POST'])
def delete_training_progress(progress_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Delete training progress from the database
    cursor.execute('DELETE FROM training_progress WHERE employee_id = %s', (progress_id,))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('training_progress'))

# Route to create a new department
@app.route('/create_department', methods=['GET', 'POST'])
def create_department():
    if request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        department_id = request.form['department_id']
        department_name = request.form['department_name']
        try:
            # Execute SQL INSERT statement
            cursor.execute('INSERT INTO departments (department_id, department_name) VALUES (%s, %s)', (department_id, department_name))
            conn.commit()
            conn.close()
            return redirect(url_for('departments'))  # Redirect to the departments route after successful insertion
        except Exception as e:
            conn.rollback()  # Rollback the transaction if an error occurs
            conn.close()
            # Handle the error (e.g., display an error message or redirect to an error page)
            return "An error occurred while creating the department: " + str(e)
    else:
        return render_template('create_department.html')


# Route to create a new employee
@app.route('/create_employee', methods=['GET', 'POST'])
def create_employee():
    if request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        employee_id = request.form['employee_id']
        Emp_name = request.form['Emp_name']
        location = request.form['location']
        department_id = request.form['department_id']
        try:
            cursor.execute('INSERT INTO employees (employee_id, Emp_name, location, department_id) VALUES (%s, %s, %s, %s)', (employee_id, Emp_name, location, department_id))
            conn.commit()
            conn.close()
            return redirect(url_for('employees'))
        except Exception as e:
            conn.rollback()  # Rollback the transaction if an error occurs
            conn.close()
            # Handle the error (e.g., display an error message or redirect to an error page)
            return "An error occurred while creating the Employee: " + str(e)
        
    else:
        return render_template('create_employee.html')

# Route to create a new course
  # Import IntegrityError for handling uniqueness constraint violation

@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        course_id = request.form['course_id']  # Retrieve course ID from the form
        title = request.form['title']
        description = request.form['C_description']
        instructor_id = request.form['instructor_id']
        duration_days = request.form['duration_days']
        
        try:
            cursor.execute('INSERT INTO Courses (course_id, title, C_description, instructor_id, duration_days) VALUES (%s, %s, %s, %s, %s)', (course_id, title, description, instructor_id, duration_days))
            conn.commit()
            conn.close()
            return redirect(url_for('courses'))
        except IntegrityError as e:  # Catch IntegrityError for uniqueness constraint violation
            conn.rollback()
            conn.close()
            return "Error: Course ID already exists. Please choose a different Course ID."
        except Exception as e:
            conn.rollback()
            conn.close()
            return "An error occurred while creating the Course: " + str(e)
    else:
        return render_template('create_course.html')




# Route to create a new instructor
@app.route('/create_instructor', methods=['GET', 'POST'])
def create_instructor():
    if request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        instructor_id = request.form['instructor_id']
        instructor_name = request.form['instructor_name']
        department_id = request.form['department_id']
        try:
            cursor.execute('INSERT INTO instructors (instructor_id, instructor_name, department_id) VALUES (%s, %s, %s)', (instructor_id, instructor_name, department_id))
            conn.commit()
            conn.close()
            return redirect(url_for('instructors'))
        except Exception as e:
            conn.rollback()  # Rollback the transaction if an error occurs
            conn.close()
            # Handle the error (e.g., display an error message or redirect to an error page)
            return "An error occurred while creating the Instructor: " + str(e)
    else:
        return render_template('create_instructor.html')

# Route to create a new training progress
@app.route('/create_training_progress', methods=['GET', 'POST'])
def create_training_progress():
    if request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        employee_id = request.form['employee_id']
        course_id = request.form['course_id']
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        
        # Fetch duration_days from the courses table
        cursor.execute('SELECT duration_days FROM courses WHERE course_id = %s', (course_id,))
        duration_days = cursor.fetchone()[0]
        
        # Calculate progress percentage based on duration and start/end dates
        total_days = (end_date - start_date).days
        progress_percentage = min(100, (total_days / duration_days) * 100)
        
        try:
            cursor.execute('INSERT INTO training_progress (employee_id, course_id, start_date, end_date, progress_percentage) VALUES (%s, %s, %s, %s, %s)', (employee_id, course_id, start_date, end_date, progress_percentage))
            conn.commit()
            conn.close()
            return redirect(url_for('training_progress'))
        except Exception as e:
            conn.rollback()  # Rollback the transaction if an error occurs
            conn.close()
            # Handle the error (e.g., display an error message or redirect to an error page)
            return "An error occurred while creating the Training: " + str(e)
    else:
        return render_template('create_training_progress.html')

def validate_user(username, password):
    # Check if the entered username and password match the credentials
    if username == user_credentials['username'] and password == user_credentials['password']:
        return 'user'
    elif username == admin_credentials['username'] and password == admin_credentials['password']:
        return 'admin'
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate the username and password
        role = validate_user(username, password)

        if role == 'user':
            # Redirect to enter_employee_id route
            return redirect(url_for('enter_employee_id', username=username, role=role))

        elif role == 'admin':
            return render_template('index.html')

        else:
            error_message = "Invalid username or password. Please try again."
            return render_template('login.html', error_message=error_message)

    return render_template('login.html')

# Route for admin dashboard
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('department.html')  # Assuming 'index.html' is your admin dashboard template

# Route for entering employee ID
@app.route('/enter_employee_id', methods=['GET', 'POST'])
def enter_employee_id():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        progress = get_training_progress(employee_id)

        if progress is not None:
            username = request.args.get('username')
            role = request.args.get('role')
            return render_template('dashboard.html', username=username, employee_id=employee_id, role=role, progress=progress)
        else:
            error_message = "No training progress found for this employee."
            return render_template('login.html', error_message=error_message)

    return render_template('enter_employee_id.html')

if __name__ == "__main__":
    app.run(debug=True)
