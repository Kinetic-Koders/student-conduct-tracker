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

    # staff2 = get_user(1)
    # print(staff.get_json())

    # create a student
    student_josh = add_student(816, "Josh")

    # log 2 reviews
    log_review(bob.staff_id, student_josh.student_id, "good", True)
    log_review(bob.staff_id, student_josh.student_id, "gooder", True)

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

app.cli.add_command(review_cli)

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