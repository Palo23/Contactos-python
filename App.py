from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MYSQL Connection
app.config["MYSQL_UNIX_SOCKET"] = "/opt/lampp/var/mysql/mysql.sock"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "flaskcontacts"

mysql = MySQL(app)

#Session
app.secret_key = "myabby"


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contactos = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        telefono = request.form['telefono']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (nombre, telefono, email) VALUES (%s, %s, %s);', 
        (fullname, telefono, email))
        mysql.connection.commit()
        flash("Contacto agregado exitosamente")
        return redirect(url_for('Index'))

@app.route('/edit/<id>') 
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit.html', contacto = data[0])

@app.route('/update_contact', methods=['POST'])
def update_contact():
    if request.method == 'POST':
        id = request.form['id']
        fullname = request.form['fullname']
        telefono = request.form['telefono']
        email = request.form['email']
    cur = mysql.connection.cursor()
    cur.execute('UPDATE contacts SET nombre=%s, telefono=%s, email=%s WHERE ID=%s', 
    (fullname, telefono, email, id))
    mysql.connection.commit()
    flash('Contacto actualizado correctamente')
    return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto eliminado')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)