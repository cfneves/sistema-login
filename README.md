# Sistema de Login

Sistema de autenticação com cadastro e login de usuários, desenvolvido em Python seguindo o padrão arquitetural **MVC**. Possui duas interfaces: CLI (terminal) e Web (Flask + HTML/CSS/JS).

---

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.x |
| Banco de dados | SQLite via SQLAlchemy 2.x |
| Backend web | Flask 3.x |
| Frontend | HTML5 + CSS3 + JavaScript (vanilla) |
| Hash de senhas | SHA-256 (`hashlib`) |

---

## Estrutura do projeto

```
.
├── model.py          # Camada Model — ORM SQLAlchemy, tabela Pessoa
├── controller.py     # Camada Controller — regras de negócio, validação, hash
├── view.py           # Interface CLI — menu interativo no terminal
├── app.py            # Servidor Flask — API REST + serve o frontend web
├── templates/
│   └── index.html    # Interface Web — SPA com design glassmorphism
└── requirements.txt
```

---

## Arquitetura MVC

```
┌─────────────┐     ┌──────────────────┐     ┌───────────────┐
│   VIEW      │────▶│   CONTROLLER     │────▶│    MODEL      │
│             │     │                  │     │               │
│ view.py     │     │ ControllerCadastro│    │ Pessoa (ORM)  │
│ index.html  │     │ ControllerLogin  │     │ SQLite DB     │
│ app.py      │     │ Resultado (Enum) │     │               │
└─────────────┘     └──────────────────┘     └───────────────┘
```

- **Model** (`model.py`) — define a entidade `Pessoa` e a conexão com o banco. O `engine` e `Session` são criados uma única vez (singleton).
- **Controller** (`controller.py`) — toda a lógica de negócio: validação de dados, hash de senhas, consultas ao banco. Retorna o `IntEnum Resultado` em vez de magic numbers.
- **View CLI** (`view.py`) — loop de menu no terminal que consome o controller.
- **View Web** (`app.py` + `index.html`) — servidor Flask que expõe o controller como API REST; o frontend é uma SPA em HTML/JS puro.

---

## Como executar

### Pré-requisitos

```bash
pip install -r requirements.txt
```

### Interface CLI (terminal)

```bash
python view.py
```

Menu interativo:
```
========== [MENU] ==========
Digite 1 para cadastrar
Digite 2 para Logar
Digite 3 para sair
```

### Interface Web

```bash
python app.py
```

Acesse **http://127.0.0.1:5000** no navegador.

---

## API REST (Flask)

### `POST /cadastrar`

**Body JSON:**
```json
{ "nome": "João Silva", "email": "joao@email.com", "senha": "minhasenha" }
```

**Resposta (sucesso):**
```json
{ "ok": true, "mensagem": "Cadastro realizado com sucesso!" }
```

**Resposta (erro):**
```json
{ "ok": false, "mensagem": "Email já cadastrado." }
```

### `POST /login`

**Body JSON:**
```json
{ "email": "joao@email.com", "senha": "minhasenha" }
```

**Resposta (sucesso):**
```json
{ "ok": true, "mensagem": "Bem-vindo! (ID: 1)" }
```

---

## Regras de validação

| Campo | Regra |
|---|---|
| Nome | 3 a 50 caracteres |
| Email | até 200 caracteres, único no banco |
| Senha | 6 a 100 caracteres |

Senhas são armazenadas como hash **SHA-256** — nunca em texto puro.

---

## Banco de dados

SQLite local (`projeto2.db`), criado automaticamente na primeira execução.

```sql
CREATE TABLE Pessoa (
    id    INTEGER PRIMARY KEY,
    nome  VARCHAR(50),
    email VARCHAR(200),
    senha VARCHAR(100)   -- SHA-256 hash
);
```

---

## Códigos de retorno (`Resultado`)

```python
class Resultado(IntEnum):
    SUCESSO             = 1
    NOME_INVALIDO       = 2
    EMAIL_INVALIDO      = 3
    SENHA_INVALIDA      = 4
    EMAIL_JA_CADASTRADO = 5
    ERRO_INTERNO        = 6
```
