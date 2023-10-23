import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    add_student,
    get_student,
    get_all_students_json,
    log_review,
    get_review,
    get_all_reviews_json,
    check_voted,
    do_vote,
    get_all_votes_json
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "123", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "123", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None,"staff_id":"123", "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", "123", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", "123", password)
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "123", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "321", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "staff_id":123, "username":"bob"}, {"id":2, "staff_id":321, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

    # insert other tests here
    #todo: 
    # add student & get all students json
    # log review & get all reviews json
    # vote & get all votes json

    # add student test
    def test_add_student(self):
        add_student(816, "Josh")
        student = get_student(816)
        assert student.name == "Josh"

    # get all students json test
    def test_get_all_students_json(self):
        # add in another student to get back a list
        add_student(817, "Paul")

        students_json = get_all_students_json()
        self.assertListEqual([{"id":1, "student_id":816, "name":"Josh", "karma":0}, {"id":2, "student_id":817, "name":"Paul", "karma":0}],students_json)

    # log review test
    def test_log_review(self):
        # log a positive review
        review1 = log_review(123, 816, "Good boy", True)
        # log a negative review
        review2 = log_review(321, 816, "Bad boy", False)

        # review1 = get_review(1)
        # review2 = get_review(2)

        assert review1.description == "Good boy" and review2.description == "Bad boy"
    
    # get all reviews json
    # z added so when ran in alphabetical order it runs after logging reviews
    def test_zget_all_reviews_json(self):

        reviews_json = get_all_reviews_json()

        # print(reviews_json)
        
        self.assertListEqual([{"id":1, "description":"Good boy", "staff_id":123, "student_id":816, "positive":True}, {"id":2, "description":"Bad boy", "staff_id":321, "student_id":816, "positive":False}], reviews_json)

    # vote tests
    def test_vote(self):
        # do 2 positive votes on review 1
        vote1 = do_vote(123, 1, 1)

        # do_vote(321, 1, 1)

        # vote1 = get_vote(1)
        # vote2 = get_vote(2)

        # self.assertListEqual([{'id':1,'staff_id':123,'review_id':1,'self.value':1}])
        assert vote1.id == 1

        # self.assertListEqual([{'id':1,'staff_id':123,'review_id':1,'self.value':1}], get_all_votes_json())
    # get all votes json test
    # z added in name so when ran in order it runs after actually adding votes
    def test_zget_all_votes_json(self):

        votes_json = get_all_votes_json()
        self.assertListEqual([{'id':1,'staff_id':123,'review_id':1,'self.value':1}], votes_json)

