from flask import Flask, request, jsonify, render_template
from controller import ControllerCadastro, ControllerLogin, Resultado

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.get_json()
    resultado = ControllerCadastro.cadastrar(
        data.get('nome', ''),
        data.get('email', ''),
        data.get('senha', '')
    )
    mensagens = {
        Resultado.SUCESSO:            ('Cadastro realizado com sucesso!', True),
        Resultado.NOME_INVALIDO:      ('Nome deve ter entre 3 e 50 caracteres.', False),
        Resultado.EMAIL_INVALIDO:     ('Email não pode ter mais de 200 caracteres.', False),
        Resultado.SENHA_INVALIDA:     ('Senha deve ter entre 6 e 100 caracteres.', False),
        Resultado.EMAIL_JA_CADASTRADO:('Este email já está cadastrado.', False),
        Resultado.ERRO_INTERNO:       ('Erro interno. Tente novamente.', False),
    }
    mensagem, ok = mensagens.get(resultado, ('Erro desconhecido.', False))
    return jsonify({'ok': ok, 'mensagem': mensagem})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    resultado = ControllerLogin.login(
        data.get('email', ''),
        data.get('senha', '')
    )
    if resultado:
        return jsonify({'ok': True, 'mensagem': f"Bem-vindo! (ID: {resultado['id']})"})
    return jsonify({'ok': False, 'mensagem': 'Email ou senha inválidos.'})

if __name__ == '__main__':
    app.run(debug=True)
