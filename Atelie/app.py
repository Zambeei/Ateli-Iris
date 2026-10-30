from flask import Flask, render_template, request, redirect, url_for, abort
import mysql.connector

app = Flask(__name__)

# Configuração da Base de Dados MySQL
def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",          
        password="senai105",          
        database="atelie_iris"     
    )

@app.route('/')
def inicio():
    return render_template('forms.html')

@app.route('/salvar_cliente', methods=['POST'])
def salvar_cliente():
   
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor()
        conexao.close()
    except Exception as e:
        print(f"Erro ao salvar cliente no banco: {e}")
        
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():

    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM pedidos")
    lista_pedidos = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return render_template('pedidos.html', pedidos=lista_pedidos)


@app.route('/debutante')
def debutante():
    return render_template('debutante.html')

@app.route('/noiva')
def noiva():
    return render_template('noiva.html')

@app.route('/festa')
def festa():
    return render_template('festa.html')

if __name__ == '__main__':
    app.run(debug=True)