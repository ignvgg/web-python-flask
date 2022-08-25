from flask import Flask
from flask import render_template
# from flaskext.mysql import MySQL

app = Flask(__name__)

# mysql = MySQL()
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_BD'] = 'sistema'
# mysql.init_app(app)

@app.route('/')

def index():
	return render_template('empleados/index.html')
	
# sql = ""
# conn = mysql.connect()
# cursor = conn.cursor()
# cursor.execute(sql)
# conn.commit()

if __name__ == '__main__':
	app.run(debug = True)