# CLAUDE.md — Sistema de Login

## O que é este projeto

Sistema de autenticação (cadastro + login) em Python com padrão MVC.
Duas interfaces: CLI (`view.py`) e Web (`app.py` + `templates/index.html`).

## Stack

- Python 3.x, SQLAlchemy 2.x, SQLite, Flask 3.x, HTML/CSS/JS vanilla
- Hash de senhas: `hashlib.sha256`

## Arquivos principais

| Arquivo | Responsabilidade |
|---|---|
| `model.py` | ORM: classe `Pessoa`, `engine` e `Session` (singleton) |
| `controller.py` | Regras de negócio: `ControllerCadastro`, `ControllerLogin`, `Resultado` (IntEnum), `_hash_senha()` |
| `view.py` | Interface CLI com menu loop |
| `app.py` | Flask: rotas `GET /`, `POST /cadastrar`, `POST /login` |
| `templates/index.html` | SPA frontend com glassmorphism dark theme |

## Decisões de design importantes

- `engine` e `Session` criados **uma única vez** em `model.py` e importados pelo controller — não recriar por chamada.
- Retornos do controller usam `IntEnum Resultado` — nunca magic numbers.
- Validação de inputs ocorre **antes** da consulta ao banco em `cadastrar()`.
- Consultas usam `.first()` (não `.all()`) — evita carregar todas as linhas.
- Sessions sempre fechadas via `finally: session.close()`.
- `app.py` é apenas uma casca Flask — toda lógica fica no controller.

## Como rodar

```bash
pip install -r requirements.txt
python app.py        # web: http://127.0.0.1:5000
python view.py       # CLI
```

## O que NÃO fazer

- Não recriar o `engine` dentro de funções — usar o importado de `model.py`.
- Não usar `.all()` onde `.first()` basta.
- Não comparar resultados do controller com inteiros literais — usar `Resultado.SUCESSO` etc.
- Não armazenar senhas em texto puro — sempre passar por `_hash_senha()`.
- Não adicionar lógica de negócio em `app.py` — pertence ao controller.
