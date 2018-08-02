import os
import psycopg2

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host='localhost', password=DB_PASS, port='5432')
cur = connection.cursor()

class Tables():
	#creates table in the database

	def create_tables():
		with connection.cursor() as cursor:
			cursor.execute ("CREATE TABLE IF NOT EXISTS entries (entryID serial PRIMARY KEY,\
				username varchar(200) NOT NULL, title varchar(50) NOT NULL,\
				comment text NOT NULL,comment_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")
			cursor.execute ("CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY,\
			 	fname varchar(100), lname varchar(100),username varchar(100) NOT NULL,\
			 	email varchar(100) NOT NULL,password varchar(100) NOT NULL,\
			 	registration_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")
		connection.commit()