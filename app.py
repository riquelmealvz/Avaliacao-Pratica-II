from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def start_db():
    conn = sqlite3.connect('alunos.db')
    cursor = conn.cursor()
    with open('schema.sql', 'r') as f:
        sql_script = f.read()
        cursor.executescript(sql_script)
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('alunos.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    alunos = conn.execute('SELECT * FROM aluno').fetchall()
    conn.close()
    return render_template('index.html', alunos=alunos)

@app.route('/cadastro', methods=('GET', 'POST'))
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        curso = request.form['curso']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO aluno (nome, idade, curso) VALUES (?, ?, ?)',(nome, curso, idade))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('cadastro.html')

if __name__ == '__main__':
    start_db()
    app.run(debug=True)