from API import app
from models import *



if __name__ == '__main__':
	Tables.create_tables()
	app.run(debug=True)