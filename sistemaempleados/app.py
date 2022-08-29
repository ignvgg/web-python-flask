from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)

# Database Connection (localhost, XAMPP outside environment)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_BD'] = 'sistema'
mysql.init_app(app)

# Index page, 'main menu'. Shows current state of employees database.

@app.route('/')
def index():
	sql = "SELECT * FROM `sistema`.`empleados`;"
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(sql)
	empleados=cursor.fetchall()
	conn.commit()
	return render_template('empleados/index.html', empleados=empleados)

# Delete function called within index with SQL query, refresh index.

@app.route('/destroy/<int:id>')
def destroy(id):
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("DELETE FROM `sistema`.`empleados` WHERE id=%s", (id))
	conn.commit()
	return redirect('/')

# Create employee method

@app.route('/create', methods=['GET', 'POST'])
def create():

	return render_template('empleados/create.html')

# After succsessfully creating an employee (form completion), insert into database.

@app.route('/store', methods=['GET', 'POST'])
def storage():

	_nombre = request.form['txtNombre']
	_correo = request.form['txtCorreo']
	_foto = request.files['txtFoto']

	now = datetime.now()
	tiempo = now.strftime('%Y%H%M%S')
	if _foto.filename!='':
		nuevoNombreFoto = tiempo + _foto.filename
		_foto.save('uploads/' + nuevoNombreFoto)

	sql = "INSERT INTO `sistema`.`empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"

	datos = (_nombre,_correo,nuevoNombreFoto)
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(sql, datos)
	conn.commit()

	return redirect('/')

# Function that permits editing an existing employee

@app.route('/edit/<int:id>')
def edit(id):

	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM `sistema`.`empleados` WHERE id=%s", (id))
	empleados=cursor.fetchall()
	conn.commit()

	return render_template('empleados/edit.html', empleados=empleados)

# Update function after edit template runs and confirms a commit to the database

@app.route('/update', methods=['GET', 'POST'])
def update():

	_nombre=request.form['txtNombre']
	_correo=request.form['txtCorreo']
	_foto=request.files['txtFoto']
	id=request.form['txtID']

	sql = "UPDATE `sistema`.`empleados` SET `nombre`=%s, `correo`=%s WHERE id=%s;"
	datos=(_nombre,_correo,id)

	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute(sql,datos)
	conn.commit()
	
	return redirect('/')


if __name__ == '__main__':
	app.run(debug = True)