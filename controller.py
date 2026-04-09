from enum import IntEnum
import hashlib
from model import Pessoa, Session


class Resultado(IntEnum):
    SUCESSO = 1
    NOME_INVALIDO = 2
    EMAIL_INVALIDO = 3
    SENHA_INVALIDA = 4
    EMAIL_JA_CADASTRADO = 5
    ERRO_INTERNO = 6


def _hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


class ControllerCadastro():
    @classmethod
    def verifica_dados(cls, nome, email, senha):
        if len(nome) > 50 or len(nome) < 3:
            return Resultado.NOME_INVALIDO
        if len(email) > 200:
            return Resultado.EMAIL_INVALIDO
        if len(senha) > 100 or len(senha) < 6:
            return Resultado.SENHA_INVALIDA
        return Resultado.SUCESSO

    @classmethod
    def cadastrar(cls, nome, email, senha):
        dados_verificados = cls.verifica_dados(nome, email, senha)
        if dados_verificados != Resultado.SUCESSO:
            return dados_verificados

        session = Session()
        try:
            if session.query(Pessoa).filter(Pessoa.email == email).first() is not None:
                return Resultado.EMAIL_JA_CADASTRADO

            p1 = Pessoa(nome=nome, email=email, senha=_hash_senha(senha))
            session.add(p1)
            session.commit()
            return Resultado.SUCESSO

        except Exception:
            session.rollback()
            return Resultado.ERRO_INTERNO
        finally:
            session.close()


class ControllerLogin():
    @classmethod
    def login(cls, email, senha):
        session = Session()
        try:
            logado = session.query(Pessoa).filter(
                Pessoa.email == email,
                Pessoa.senha == _hash_senha(senha)
            ).first()
            if logado is not None:
                return {'logado': True, 'id': logado.id}
            return False
        finally:
            session.close()
