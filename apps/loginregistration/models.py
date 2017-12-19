from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def regis_validator(self, post):
        first_name = post['first_name']
        last_name = post['last_name']
        email = post['email'].lower()
        password = post['password']
        cpassword = post['cpassword']
        errors=[]

        if not self:
            errors.append("all fields are required.")
        else:
            if not EMAIL_REGEX.match(email):
                errors.append("invalid email.")
            else:
                if len(User.objects.filter(email=email)) > 0 :
                    errors.append('email is used already')

            if not first_name.isalpha() or not last_name.isalpha():
                errors.append("characters only for first name and last name")

            if len(password) < 3 :
                errors.append('password need to have at least 8 characters')
            elif password != cpassword:
                errors.append('password is not match, please try again')

        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw((password.encode()), bcrypt.gensalt(5))

            new_user = self.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hashed
            )
            return new_user                

        return errors

    def login_validator(self, post):
        email = post['email'].lower()
        password = post['password']

        try:
            user = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return user
        except:
            pass

        return False

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()