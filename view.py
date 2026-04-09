from controller import ControllerCadastro, ControllerLogin, Resultado

while True:
    print("========== [MENU] ==========")
    try:
        decidir = int(input('Digite 1 para cadastrar\nDigite 2 para Logar\nDigite 3 para sair\n'))
    except ValueError:
        print("Opção inválida. Digite um número.")
        continue

    if decidir == 1:
        nome = input('Digite seu nome: ')
        email = input('Digite seu email: ')
        senha = input('Digite sua senha: ')
        resultado = ControllerCadastro.cadastrar(nome, email, senha)

        if resultado == Resultado.NOME_INVALIDO:
            print("Tamanho do nome digitado inválido")
        elif resultado == Resultado.EMAIL_INVALIDO:
            print("Email maior que 200 caracteres")
        elif resultado == Resultado.SENHA_INVALIDA:
            print("Tamanho da senha inválido")
        elif resultado == Resultado.EMAIL_JA_CADASTRADO:
            print("Email já cadastrado")
        elif resultado == Resultado.ERRO_INTERNO:
            print("Erro interno do sistema")
        elif resultado == Resultado.SUCESSO:
            print("Cadastro realizado com sucesso")

    elif decidir == 2:
        email = input('Digite seu email: ')
        senha = input('Digite sua senha: ')
        resultado = ControllerLogin.login(email, senha)
        if not resultado:
            print("Email ou senha inválidos")
        else:
            print(resultado)

    else:
        break
