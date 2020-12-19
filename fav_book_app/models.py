from django.db import models
import bcrypt
import datetime
from django.utils.dateparse import parse_date
import re
# Create your models here.


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['first_name']) < 2:
            errors["first_name"] = "first_name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "last_name should be at least 2 characters"
        if len(postData['pw']) < 8:
            errors["password"] = "password should be at least 8 characters"
        if postData['pw'] != postData['pw_cn']:
            errors["pw"] = "password should match"
        if postData['birth_date'] > str(datetime.date.today()):
            errors["desc"] = "The birth date should be in the past!"
        if User.objects.filter(email=postData['email']):
            errors['not_unique'] = 'This Email is already registered'
        if (datetime.date.today() - parse_date(postData['birth_date'])).days < 4745:
            errors['COPPA'] = 'This Application is not suitable for kids'
        return errors
    def login_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(User.objects.filter(email=postData['email'])) == 0:
            errors['not_registered'] = "You need to Register"
        if len(postData['pw']) < 8:
            errors["password"] = "password should be at least 8 characters"
        return errors


    def add_book_validator(self, postData):
        errors = {}
        if len(postData['title']) == 0:
            errors['title'] = "title is required"
        if len(postData['desc']) < 5:
            errors['desc'] = "Description should be at least five characters"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(null=True)
    uploaded_by = models.ForeignKey(User, related_name="book_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


def registration(new_user):
    hash_pw = bcrypt.hashpw(new_user['pw'].encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(first_name=new_user['first_name'], last_name=new_user['last_name'],
                               email=new_user['email'], birth_date=new_user['birth_date'], password=hash_pw)
    return user.id


def log_in(log_in_data):
    user = User.objects.filter(email=log_in_data['email'])
    if bcrypt.checkpw(log_in_data['pw'].encode(), user[0].password.encode()):
        context= {
            'flag': True,
            'this_user': user[0]
        }
        return context
    else:
        context = {
            'flag': False
        }
        return context


def success(user_id):
    context = {
        'this_user': User.objects.get(id=user_id),
        'all_books': Book.objects.all()
    }
    return context


def uploaded(user_id):
    books_list = []
    user = User.objects.get(id=user_id)
    for book in user.book_uploaded.all():
        books_list.append(book.id)
    return books_list


def get_user(user_id):
    return User.objects.get(id=user_id)


def get_book(book_id):
    return Book.objects.get(id=book_id)


def display(book_id, user_id):
    context = {
        'book': Book.objects.get(id=book_id),
        'this_user': User.objects.get(id=user_id)
    }
    return context


def add_fav(book_id, user_id):
    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=user_id)
    this_user.liked_books.add(this_book)
    return


def unfavorite(book_id, user_id):
    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=user_id)
    this_user.liked_books.remove(this_book)


def add_book(user_id, book_info):
    added_book = Book.objects.create(title=book_info['title'], desc=book_info['desc'], uploaded_by=User.objects.get(id=user_id))
    this_user = get_user(user_id)
    this_user.liked_books.add(added_book)
    return added_book.id


def update(postData, book_id):
    this_book = get_book(book_id)
    this_book.title = postData['title']
    this_book.desc = postData['desc']
    this_book.save()
    return


def destroy(book_id):
    this_book = get_book(book_id)
    this_book.delete()
    return
