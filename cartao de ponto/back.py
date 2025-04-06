import csv
from datetime import datetime

import pandas as pd
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'chave_super_secreta'  # Protege a sessão

# Rota da tela de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        # Carrega a planilha
        try:
            df = pd.read_excel('usuarios.xlsx')
        except Exception as e:
            return f"Erro ao ler a planilha: {e}"

        # Valida usuário e senha
        filtro = (
            df['usuario'].astype(str).str.strip() == usuario.strip()
        ) & (
            df['senha'].astype(str).str.strip() == senha.strip()
        )

        usuario_valido = df[filtro]

        if not usuario_valido.empty:
            try:
                nome = usuario_valido.iloc[0]['nome_completo']
                session['nome_completo'] = nome
                return redirect(url_for('ponto'))
            except Exception as e:
                return f"Erro ao acessar nome completo: {e}"
        else:
            return render_template('login.html', erro='Usuário ou senha inválidos')

    return render_template('login.html')


# Rota da página principal (protegida)
@app.route('/ponto')
def ponto():
    if 'nome_completo' not in session:
        return redirect(url_for('login'))
    
    mensagem = session.pop('mensagem_sucesso', '')  # Remove após exibir
    return render_template('index.html', nome=session['nome_completo'], mensagem=mensagem)


# Rota para registrar o ponto
@app.route('/registrar', methods=['POST'])
def registrar():
    nome = request.form['nome']
    acao = request.form['acao']
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    with open('registro.csv', mode='a', newline='') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow([nome, acao, agora])
        
    session['mensagem_sucesso'] = f"Seu ponto: {acao} foi marcado com sucesso!"
    return redirect(url_for('ponto'))        


# Rota de logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

app = Flask(__name__)
    
    
