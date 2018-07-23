import psycopg2

connection = psycopg2.connect("dbname='diary' user='postgres' host='localhost' password='cocopine1' port='5432'")
cur = connection.cursor()

#creates table in the database
def create_tables():
	with connection.cursor() as cursor:
	    cursor.execute ("CREATE TABLE IF NOT EXISTS entries (entryID serial PRIMARY KEY,username varchar(200) NOT NULL, title varchar(50) NOT NULL,comment text NOT NULL,comment_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")
	    cursor.execute ("CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, fname varchar(100), lname varchar(100),username varchar(100) NOT NULL,email varchar(100) NOT NULL,password varchar(100) NOT NULL,registration_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")
	connection.commit()