import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

# Configuração do Flask
app = Flask(__name__)
app.secret_key = 'chave_super_secreta'

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ponto.db'  # banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    nome_completo = db.Column(db.String(200), nullable=False)

# Modelo de registro de ponto
class RegistroPonto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    acao = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)

# Criar as tabelas no banco de dados
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        # Validar usuário e senha no banco de dados
        usuario_valido = Usuario.query.filter_by(usuario=usuario.strip(), senha=senha.strip()).first()

        if usuario_valido:
            session['nome_completo'] = usuario_valido.nome_completo
            return redirect(url_for('ponto'))
        else:
            return render_template('login.html', erro='Usuário ou senha inválidos')

    return render_template('login.html')


@app.route('/ponto')
def ponto():
    if 'nome_completo' not in session:
        return redirect(url_for('login'))
    
    mensagem = session.pop('mensagem_sucesso', '')  # Remove após exibir
    return render_template('index.html', nome=session['nome_completo'], mensagem=mensagem)


@app.route('/registrar', methods=['POST'])
def registrar():
    nome = request.form['nome']
    acao = request.form['acao']
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    # Criar um novo registro de ponto no banco de dados
    novo_registro = RegistroPonto(nome=nome, acao=acao, timestamp=agora)
    db.session.add(novo_registro)
    db.session.commit()

    session['mensagem_sucesso'] = f"Seu ponto: {acao} foi marcado com sucesso!"
    return redirect(url_for('ponto'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='192.168.1.4', port=5000, debug=True)

