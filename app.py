
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'your_secret_key'  


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = ''  
app.config['MYSQL_DB'] = 'task'


mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email,phone,address) VALUES (%s, %s, %s ,%s)", (name, email,phone,address))
        mysql.connection.commit()
        flash('Student added successfully!')
        return redirect(url_for('index'))
    return render_template('add_user.html')

@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        cur.execute("UPDATE users SET name = %s, email = %s, phone = %s, address = %s  WHERE id = %s", (name, email, phone, address, id))
        mysql.connection.commit()
        flash('Student updated successfully!')
        return redirect(url_for('index'))
    
    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    flash('Student deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
