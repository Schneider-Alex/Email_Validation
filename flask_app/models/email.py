from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import email
from flask import flash
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# model the class after the friend table from our database
class Email:
    def __init__( self , data ):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @staticmethod
    def validate_email( email ):
        is_valid = True
        query = """SELECT * FROM emails WHERE email =  %(email)s"""
        results = connectToMySQL('email_schema').query_db(query, email)
        if len(results) >= 1:
            flash("email address already in use!")
            is_valid = False
        elif not EMAIL_REGEX.match(email['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM emails;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('email_schema').query_db(query)
        # Create an empty list to append our instances of friends
        emails = []
        # Iterate over the db results and create instances of friends with cls.
        for email in results:
            emails.append( cls(email)) 
        return emails
    
    @classmethod
    def save(cls, data ):
        query = """INSERT INTO emails (email, created_at,updated_at ) 
        VALUES (%(email)s, NOW() , NOW());"""
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('email_schema').query_db( query, data )
    
    
    