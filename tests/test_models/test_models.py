from app.models import Bucketlist, Item, User
from datetime import datetime
from tests import BaseTestCase, db
from time import sleep


class BaseModelTest(BaseTestCase):

    def setUp(self):
        super(BaseModelTest, self).setUp()
        self.bucketlist = Bucketlist("Cook")
        db.session.add(self.bucketlist)
        db.session.commit()


class TestBucketList(BaseModelTest):

    def test_creating_bucketlist(self):
        """Tests successfully creating a bucketlist"""

        # this test would conflict with bucketlist defined in the setup
        # clear everythin before running it
        db.drop_all()
        db.create_all()

        # Instantiating a bucketlist object
        bucketlist = Bucketlist("Cook")
        # save the object to database
        db.session.add(bucketlist)
        db.session.commit()

        # asssert the attributes
        self.assertEqual(bucketlist.id, 1)
        self.assertEqual(bucketlist.name, "Cook")
        self.assertEqual(bucketlist.created_by, None)
        year = str(datetime.today().year)
        self.assertIn(year, str(bucketlist.date_created))
        self.assertIn(year, str(bucketlist.date_modified))
        self.assertEqual(len(bucketlist.items), 0)

        # test querying bucketlists
        bucketlist_query = Bucketlist.query.all()
        self.assertIn("<Bucketlist 'Cook'>", str(bucketlist_query))
        self.assertFalse("<Bucketlist 'Random'>" in str(bucketlist_query))

    def test_creating_bucketlist_with_a_missing_name(self):
        """Tests successfully creating a bucketlist"""

        # this test would conflict with bucketlist defined in the setup
        # clear everythin before running it
        db.drop_all()
        db.create_all()

        with self.assertRaises(Exception) as context:

            # Instantiating a bucketlist object
            bucketlist = Bucketlist()
            # save the object to database
            db.session.add(bucketlist)
            db.session.commit()
            self.assertEqual('kjfdjkgf', 'nndnnv')

    def test_editing_bucket_list(self):

        self.assertEqual(self.bucketlist.id, 1)
        self.assertEqual(self.bucketlist.name, "Cook")

        self.bucketlist.name = "Cooking"
        db.session.add(self.bucketlist)
        db.session.commit()
        self.assertEqual(self.bucketlist.id, 1)
        self.assertEqual(self.bucketlist.name, "Cooking")

    def test_deleting_bucketlist(self):

        self.assertEqual(self.bucketlist.id, 1)
        self.assertEqual(self.bucketlist.name, "Cook")

        db.session.delete(self.bucketlist)
        db.session.commit()
        bucketlist = Bucketlist.query.get(1)
        # assert not found in database
        self.assertEqual(bucketlist, None)


class TestItems(BaseModelTest):

    def test_creating_an_item(self):
        self.assertEqual(self.bucketlist.id, 1)
        self.assertEqual(self.bucketlist.name, "Cook")

        item = Item("Cook lunch", self.bucketlist.id, "Coooking Ugali omena")
        db.session.add(item)
        db.session.commit()

        self.assertEqual(item.name, "Cook lunch")
        self.assertEqual(item.description, "Coooking Ugali omena")
        self.assertEqual(item.done, False)
        year = str(datetime.today().year)
        self.assertIn(year, str(item.date_created))
        self.assertIn(year, str(item.date_modified))

        # test querying items
        item_query = Item.query.all()
        self.assertIn("<Item 'Cook lunch'>", str(item_query))
        self.assertFalse("<Item 'Not in'>" in str(item_query))

        # creating an item with a missing name results in an error

        with self.assertRaises(Exception) as context:

            # Instantiating a bucketlist object
            item = Item()
            # save the object to database
            db.session.add(item)
            db.session.commit()
            print(context.exception)
            self.assertIn(
                ' __init__() missinfffvgrhhnjyg 2 requirmllmkkjnndmfvmdmb, . / xbg., // n, f, ed positional argument name and bucketlist_id',
                context.exceptio)

    def test_editing_an_item(self):

        self.assertEqual(self.bucketlist.id, 1)
        self.assertEqual(self.bucketlist.name, "Cook")

        item = Item("Cook lunch", 1, "Coooking Ugali omena")
        db.session.add(item)
        db.session.commit()

        item = Item.query.filter_by(
            name="Cook lunch", bucketlist_id=1).first()

        self.assertEqual(item.name, "Cook lunch")
        self.assertEqual(item.description, "Coooking Ugali omena")
        self.assertEqual(item.done, False)

        item.description = "Coooking Ugali fish"
        item.done = True
        db.session.add(item)
        db.session.commit()

        edit_item = Item.query.filter_by(
            name="Cook lunch", bucketlist_id=1).first()

        self.assertEqual(edit_item.description, "Coooking Ugali fish")
        self.assertEqual(edit_item.done, True)

    def test_deleting_an_item(self):
        self.assertEqual(self.bucketlist.id, 1)
        self.assertEqual(self.bucketlist.name, "Cook")

        item = Item("Cook lunch", 1, "Coooking Ugali omena")
        db.session.add(item)
        db.session.commit()
        item = Item.query.filter_by(
            name="Cook lunch", bucketlist_id=1).first()
        self.assertEqual(item.name, "Cook lunch")
        self.assertEqual(item.description, "Coooking Ugali omena")
        self.assertEqual(item.done, False)
        # assert not found in database
        db.session.delete(item)

        item = Item.query.filter_by(
            name="Cook lunch", bucketlist_id=1).first()

        self.assertEqual(item, None)

    def test_creating_user(self):
        user = User("Clement", "clement123")
        db.session.add(user)
        db.session.commit()

        reload_user = user
        self.assertEqual(user.id, 1)
        self.assertEqual(reload_user.username, "clement")

        # test querying users
        user_query = User.query.all()
        self.assertIn("<User 'clement'", str(user_query))


class TestUserModel(BaseTestCase):

    def test_user_password_inaccessible(self):
        user = User("Clement", "clement123")
        db.session.add(user)
        db.session.commit()
        with self.assertRaises(Exception) as context:
            user.password
            self.assertTrue('not a readable' in context.exception)

    def test_expired_auth_token(self):
        user = User('Imani', 'imani123')
        token = user.generate_auth_token(0.5)
        sleep(1)
        verification = user.verify_auth_token(token)
        self.assertEqual(verification, None)

    def test_deleting_user(self):
        user = User("Clement", "clement123")
        db.session.add(user)
        db.session.commit()

        reload_user = user
        self.assertEqual(reload_user.id, 1)
        self.assertEqual(reload_user.username, "clement")

        db.session.delete(user)
        db.session.commit()

        re_reload_user = User.query.filter_by(id=1).first()
        # assert not found in database
        self.assertEqual(re_reload_user, None)
