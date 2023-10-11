from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user, add_student,log_review, do_vote

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()

    # create users/staff
    bob = create_user('bob','123', 'bobpass')
    joe = create_user('joe', '124', 'joepass')
    jeff = create_user('jeff', '125', 'jeffpass')

    # create a student
    student_1 = add_student(816, "Josh")
    student_2 = add_student(817, "Paul")

    # log reviews
    review1 = log_review(bob.staff_id, student_1.student_id, "good", True)

    review2 = log_review(bob.staff_id, student_1.student_id, "gooder", True)
    review6 = log_review(bob.staff_id, student_1.student_id, "badd", False)

    review3 = log_review(bob.staff_id, student_2.student_id, "good", True)
    review4 = log_review(joe.staff_id, student_2.student_id, "Bad", False)
    review5 = log_review(bob.staff_id, student_2.student_id, "gooder", True)

    # do some votes
    # bob votes positive on review 1
    do_vote(bob.staff_id, review1.id, 1)
    # joe votes positive on review 1
    do_vote(joe.staff_id, review1.id, 1)
    # jeff votes negative on review 1
    do_vote(jeff.staff_id, review1.id, -1)

    do_vote(bob.staff_id, review2.id, 1)
    do_vote(joe.staff_id, review2.id, 1)

    do_vote(bob.staff_id, review6.id, 1)

    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})