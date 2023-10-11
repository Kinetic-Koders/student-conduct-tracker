from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    jwt_required,
    add_student,
    get_all_students_json,
    get_student
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['username'],data['staff_id'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})

# MY VIEWS, HAVE TO TEST WITH POSTMAN - use gitpod workspace instead of github codespace

# MIGHT HAVE TO CHANGE RETURN MSGS
# MIGHT HAVE TO MOVE TO INDEX VIEWS

# DO:   get all reviews json route
#       voting
#       authorization? login, logoff etc.

# add students route
@user_views.route('/api/users/add_student', methods=['POST'])
def add_student_endpoint():
    data = request.jsonify
    add_student(data['student_id'], data['name'])
    return jsonify({'message:'f"student {data['name']} added"})

#  log review route
@user_views.route('/api/users/log_review', methods=['POST'])
def log_review_endpoint():
    data = request.jsonify
    log_review(data['staff_id'], data['student_id'], data['description'], data['positive'])
    return jsonify({'message:' "review created!"})

#log a review
# @users_views.route('/api/users/review/<staff_id>/<student_id>/<description>/<positive>', methods=['POST'])
# #  login required
# def log_review_endpoint(staff_id, student_id, description, positive):
#     review = log_review(staff_id, student_id, description, positive)
#     return jsonify({'message:' "review created"})

# get all studentsjson route
@user_views.route('/api/users/students', methods=['GET'])
def get_all_students_endpoint():
    students = get_all_students_json()
    return jsonify(students)

# get a student by id
@user_views.route('/api/users/student/<int:student_id>', methods=['GET'])
# login required
def get_student_by_id(student_id):
    student = get_student(student_id)
    return jsonify(student.get_json())




@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'],data['staff_id'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')