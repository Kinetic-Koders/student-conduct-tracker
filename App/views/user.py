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
    get_student,
    log_review,
    do_vote
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

#  done
@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

# done
# @user_views.route('/api/users', methods=['POST'])
# def create_user_endpoint():
#     data = request.json
#     create_user(data['username'],data['staff_id'], data['password'])
#     return jsonify({'message': f"user {data['username']} created"})

# route that return erros message if already created
@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    result = create_user(data['username'],data['staff_id'], data['password'])
    if result:
        return jsonify({'message': f"user {data['username']} created"}), 201
    return jsonify({'message': f"user {data['username']} or {data['staff_id']} already exists"}), 500



# add students route
# done
# @user_views.route('/api/users/add_student', methods=['POST'])
# def add_student_endpoint():
#     data = request.json
#     add_student(data['student_id'], data['name'])
#     return jsonify({'message':f"student {data['name']} added"})
#     # return jsonify({'message': f"user {data['username']} created"})

# route that returns error message if already created
@user_views.route('/api/users/add_student', methods=['POST'])
def add_student_endpoint():
    data = request.json
    result = add_student(data['student_id'], data['name'])
    if result:
        return jsonify({'message':f"student {data['name']} added"}), 201
    return jsonify({'message': f"student {data['username']} or {data['student_id']} already exists"}), 500

#  log review route
# done
@user_views.route('/api/users/log_review', methods=['POST'])
def log_review_endpoint():
    data = request.json
    log_review(data['staff_id'], data['student_id'], data['description'], data['positive'])
    return jsonify({'message': "review created!"})

# get all studentsjson route
# done
@user_views.route('/api/users/students', methods=['GET'])
def get_all_students_endpoint():
    students = get_all_students_json()
    return jsonify(students)

# get a student by id
# done
@user_views.route('/api/users/student/<int:student_id>', methods=['GET'])
# login required
def get_student_by_id(student_id):
    student = get_student(student_id)
    return jsonify(student.get_json())

# vote
@user_views.route('/api/users/vote', methods=["POST"])
def vote_endpoint():
    data = request.json
    do_vote(data['staff_id'], data['review_id'], data['value'])
    return jsonify({'message': "vote completed!"})



@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'],data['staff_id'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')