from __init__ import *
from models import *



if __name__ == '__main__':
	create_tables()
	app.run(debug=True)