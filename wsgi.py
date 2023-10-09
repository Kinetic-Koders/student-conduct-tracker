import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app


# from App.controllers import ( create_user, get_all_users_json, get_all_users )
from App.controllers import *

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()

    # create users/staff
    bob = create_user('bob','123', 'bobpass')
    joe = create_user('joe', '124', 'joepass')
    jeff = create_user('jeff', '125', 'jeffpass')

    # staff2 = get_user(1)
    # print(staff.get_json())

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
    do_vote(jeff.staff_id, review1.id, -1)

    do_vote(bob.staff_id, review2.id, 1)
    do_vote(joe.staff_id, review2.id, 1)

    do_vote(bob.staff_id, review6.id, 1)
    

    # bob changes to negative on review 1
    # do_vote(bob.staff_id, review1.id, -1)
    
    # joe votes the same value again which unvotes
    # do_vote(joe.staff_id, review1.id, 1)

    # print(get_karma_by_id(816))

    # try to print all reviews for a particular student_id


    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("staff_id", default="321")
@click.argument("password", default="robpass")
def create_user_command(username, staff_id,  password):
    create_user(username, staff_id, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

@user_cli.command("vote", help="Votes on a particular review")
@click.argument("staff_id", default="123")
@click.argument("review_id", default="1")
@click.argument("value", default="1")
def user_vote(staff_id, review_id, value):
    new_vote = do_vote(staff_id, review_id, value)
    
    print(new_vote.get_json())

app.cli.add_command(user_cli) # add the group to the cli


# student command
student_cli = AppGroup('student', help="student object commands")

# @student_cli("create", help="creates a student")

@student_cli.command("list", help="Lists students in the database")
@click.argument("format", default="string")
def list_students_command(format):
    if format == 'string':
        print(get_all_students())
    else:
        print(get_all_students_json())

# @student_cli.command("get", help="Get all information about a specific student")

app.cli.add_command(student_cli)

# review commands
review_cli = AppGroup('review', help="review object commands")

@review_cli.command("list", help="Lists reviews in the database")
@click.argument("format", default="string")
def list_reviews_command(format):
    if format == 'string':
        print(get_all_reviews())
    else:
        print(get_all_reviews_json())

@review_cli.command("student", help="List all reviews for a particular student")
@click.argument("student_id", default="816")
def list_student_reviews(student_id):
    print(get_all_student_reviews_json(student_id))

app.cli.add_command(review_cli)

# vote commands
vote_cli = AppGroup('vote', help="vote object commands")

@vote_cli.command("list", help="List all votes in the databse")
@click.argument("format", default="string")
def list_votes(format):
    if format == "string":
        print(get_all_votes())
    else:
        print(get_all_votes_json())


app.cli.add_command(vote_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)