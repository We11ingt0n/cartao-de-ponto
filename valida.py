from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# Tela de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        # Validação simples (você pode trocar por banco de dados ou planilha)
        if usuario == 'admin' and senha == '1234':
            return redirect(url_for('ponto'))
        else:
            return render_template('login.html', erro='Usuário ou senha inválidos')
    return render_template('login.html')

# Tela principal protegida
@app.route('/ponto', methods=['GET'])
def ponto():
    return render_template('index.html')
