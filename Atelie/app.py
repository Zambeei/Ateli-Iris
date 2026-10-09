import os

import mysql.connector
from mysql.connector import IntegrityError
from flask import Flask , abort, redirect, render_template, request, url_for



# Cria a aplicação Flask.
# Os arquivos HTML devem estar na pasta templates.
app = Flask(__name__)


def conectar_mysql():
    """
    Cria uma conexão com o banco de dados MySQL.
    """

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "senai105"),
        database="atelie_iris",
    )

@app.route("/")
def inicio():
    """
    Redireciona a página inicial index.html
    """

    return render_template("/index.html")


@app.route("/noiva") 
def noiva():
    return render_template("/noiva.html")


@app.route("/festa")
def festa():
    return render_template("/festa.html")


@app.route("/formulario")
def formulario():
    return render_template("/forms.html")



@app.route("/debutante")
def debutante():
    return render_template("/debutante.html")


@app.route("/pedidos")
def listar_pedidos():
    conexao = conectar_mysql()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT 
                pedidos.id AS pedido_id,
                cliente.nome AS nome_cliente,
                pedidos.data_pedido,
                pedidos.valor_total,
                pedidos.status
            FROM pedidos
            INNER JOIN cliente ON pedidos.cliente_id = cliente.cliente_id
            """
        )
        pedidos = cursor.fetchall()
    finally:
        cursor.close()
        conexao.close()

    return render_template("pedidos.html", pedidos=pedidos)


"""

    conexao = conectar_mysql()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT aluno_id, nome, email, telefone "
            "FROM alunos "
            "ORDER BY aluno_id DESC"
        )

        alunos = cursor.fetchall()

    finally:
        cursor.close()
        conexao.close()

    return render_template("alunos.html", alunos=alunos)


@app.route("/alunos/novo", methods=["GET", "POST"])
def cadastrar_aluno():
    
    GET: mostra o formulário.

    POST: recebe os dados, valida e grava um novo aluno no MySQL.
    

    # Quando a página é acessada pela primeira vez.
    if request.method == "GET":
        return render_template(
            "formulario.html",
            erro=None,
            valores={},
        )

    # Recupera os dados enviados pelo formulário HTML.
    # O nome usado aqui precisa ser igual ao atributo name do input.
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    telefone = request.form.get("telefone", "").strip()

    # Guarda os valores para reapresentá-los caso ocorra algum erro.
    valores = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
    }

    # Validação dos campos obrigatórios.
    if not nome or not email:
        return (
            render_template(
                "formulario.html",
                erro="Preencha o nome e o email.",
                valores=valores,
            ),
            400,
        )

    # Validação simples do email.
    if "@" not in email:
        return (
            render_template(
                "formulario.html",
                erro="Confira o formato do email.",
                valores=valores,
            ),
            400,
        )

    # Validação do tamanho dos campos conforme a estrutura do banco.
    if len(nome) > 100:
        return (
            render_template(
                "formulario.html",
                erro="O nome pode ter no máximo 100 caracteres.",
                valores=valores,
            ),
            400,
        )

    if len(email) > 120:
        return (
            render_template(
                "formulario.html",
                erro="O email pode ter no máximo 120 caracteres.",
                valores=valores,
            ),
            400,
        )

    if len(telefone) > 20:
        return (
            render_template(
                "formulario.html",
                erro="O telefone pode ter no máximo 20 caracteres.",
                valores=valores,
            ),
            400,
        )

    conexao = conectar_mysql()
    cursor = conexao.cursor()

    try:
        # Os marcadores %s recebem os valores da tupla abaixo.
        # Os dados não devem ser concatenados diretamente no SQL.
        cursor.execute(
            
            INSERT INTO alunos (nome, email, telefone)
            VALUES (%s, %s, %s)
            ,
            (
                nome,
                email,
                telefone or None,
            ),
        )

        # Recupera o ID gerado automaticamente pelo banco.
        novo_id = cursor.lastrowid

        # Confirma o INSERT no banco de dados.
        conexao.commit()

    except IntegrityError as erro_mysql:
        # Desfaz a operação caso ocorra algum erro.
        conexao.rollback()

        # Erro 1062 significa valor duplicado.
        # Neste banco, o email possui UNIQUE.
        if erro_mysql.errno == 1062:
            return (
                render_template(
                    "formulario.html",
                    erro="Este email já está cadastrado.",
                    valores=valores,
                ),
                409,
            )

        # Reenvia outros erros para que apareçam no terminal.
        raise

    finally:
        cursor.close()
        conexao.close()

    # Depois do cadastro, abre a página do aluno criado.
    return redirect(
        url_for(
            "detalhar_aluno",
            aluno_id=novo_id,
        )
    )


@app.route("/alunos/<int:aluno_id>")
def detalhar_aluno(aluno_id):
    
    Busca um aluno específico pelo ID.
    

    conexao = conectar_mysql()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute(
            
            SELECT aluno_id, nome, email, telefone
            FROM alunos
            WHERE aluno_id = %s
            "",
            (aluno_id,),
        )

        aluno = cursor.fetchone()

    finally:
        cursor.close()
        conexao.close()

    # Se nenhum aluno for encontrado, retorna erro 404.
    if aluno is None:
        abort(404)

    return render_template(
        "aluno_cadastrado.html",
        aluno=aluno,
    )
"""

# Inicia o servidor somente quando executamos:
# python app.py
if __name__ == "__main__":
    app.run(debug=True)