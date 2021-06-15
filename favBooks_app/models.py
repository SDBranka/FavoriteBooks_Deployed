from django.db import models
import re
import bcrypt

# Create your models here.

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

        if len(postData['first_name']) < 2 or not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "Please enter a valid first name"
        if len(postData['last_name']) < 2 or not NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "Please enter a valid last name"
        if len(postData['email']) < 2 or not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Please enter a valid email"
        email_in_db = self.filter(email = postData['email'])        #ensure no duplicate email exists
        if email_in_db:
            errors["email"] = "This email already exists in the database"
        if len(postData['password']) < 8:
            errors["password"] = "Please enter a valid password"
        if not postData['password'] == postData['confirm_pw']:
            errors['confirm_pw'] = "Your passwords do not match"
        return errors

    def login_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['lemail']) < 2 or not EMAIL_REGEX.match(postData['lemail']):
            errors["email"] = "Please enter a valid email"
        if len(postData['lpassword']) < 8:
            errors["password"] = "Please enter a valid password"

        email_in_db = self.filter(email = postData['lemail'])
        if not email_in_db:
            errors['email'] = "This email is not registered"
        else:
            user = User.objects.get(email=postData["lemail"])
            pw_to_hash = postData["lpassword"]
            if not bcrypt.checkpw(pw_to_hash.encode(), user.password.encode()):
                errors['email'] = "Incorrect password entered"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class BookManager(models.Manager):
    def add_book_validator(self, postData):
        errors = {}

        if len(postData['title']) < 1:
                errors['title'] = "Title should be at least 1 characters"
        title_in_db = self.filter(title = postData['title'])        #ensure no duplicate title exists
        if title_in_db:
            errors["title"] = "This title already exists in the database"
        if len(postData['desc']) < 5 :
            errors['desc'] = "Description should be more than 5 characters"        
        return errors

    def edit_book_validator(self, postData):
        errors = {}

        if len(postData['title']) < 1:
                errors['title'] = "Title should be at least 1 characters"
        if len(postData['desc']) < 5 :
            errors['desc'] = "Description should be more than 5 characters"        
        return errors


class Book(models.Model):
    uploaded_by = models.ForeignKey(
        User, 
        related_name = "books_uploaded",
        on_delete = models.CASCADE
    )
    favorited_by = models.ManyToManyField(
        User, 
        related_name="fav_books"
    )
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
