from flask import Flask, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "123"

ordens = []

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['senha'] == '123':
            session['logado'] = True
            return redirect('/')
    return '''
    <h2>Login</h2>
    <form method="post">
    Usuário:<input name="user"><br><br>
    Senha:<input type="password" name="senha"><br><br>
    <button>Entrar</button>
    </form>
    '''

@app.before_request
def proteger():
    if request.endpoint != 'login' and not session.get('logado'):
        return redirect('/login')

@app.route('/')
def home():
    html = ""
    for o in ordens:
        html += f"<div style='padding:10px;border:1px solid #ccc;margin:5px'>{o}</div>"
    return f'''
    <h2>Ordens de Serviço</h2>
    {html}
    <br>
    <a href="/nova">➕ Nova OS</a>
    '''

@app.route('/nova', methods=['GET','POST'])
def nova():
    if request.method == 'POST':
        cliente = request.form['cliente']
        servico = request.form['servico']
        ordens.append(f"Cliente: {cliente} | Serviço: {servico}")
        return redirect('/')
    return '''
    <h2>Nova Ordem de Serviço</h2>
    <form method="post">
    Cliente:<br><input name="cliente"><br><br>
    Serviço:<br><input name="servico"><br><br>
    <button>Salvar</button>
    </form>
    '''

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
