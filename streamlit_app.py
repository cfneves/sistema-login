import streamlit as st
from controller import ControllerCadastro, ControllerLogin, Resultado

# ── Helpers de alerta ────────────────────────────────────────────────────────
def alerta_err(msg: str) -> None:
    st.markdown(f'<div class="alerta-err">{msg}</div>', unsafe_allow_html=True)

def alerta_ok(msg: str) -> None:
    st.markdown(f'<div class="alerta-ok">{msg}</div>', unsafe_allow_html=True)

_CAMPOS_OBRIGATORIOS = "Preencha todos os campos."

_MSGS_CADASTRO: dict[Resultado, tuple[str, bool]] = {
    Resultado.SUCESSO:             ("Cadastro realizado com sucesso! Faça login.", True),
    Resultado.NOME_INVALIDO:       ("Nome deve ter entre 3 e 50 caracteres.",     False),
    Resultado.EMAIL_INVALIDO:      ("Email não pode ter mais de 200 caracteres.", False),
    Resultado.SENHA_INVALIDA:      ("Senha deve ter entre 6 e 100 caracteres.",   False),
    Resultado.EMAIL_JA_CADASTRADO: ("Este email já está cadastrado.",              False),
    Resultado.ERRO_INTERNO:        ("Erro interno. Tente novamente.",              False),
}

def _mostrar_resultado_cadastro(resultado: Resultado) -> None:
    msg, sucesso = _MSGS_CADASTRO.get(resultado, ("Erro desconhecido.", False))
    alerta_ok(msg) if sucesso else alerta_err(msg)

# ── Página ──────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Sistema de Login", page_icon="🔐", layout="centered")

# ── CSS — glassmorphism dark idêntico ao index.html ─────────────────────────
st.markdown("""
<style>
  /* fundo gradiente */
  .stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  }

  /* esconde elementos padrão do Streamlit */
  #MainMenu, header, footer { visibility: hidden; }
  .block-container { padding-top: 3rem; padding-bottom: 2rem; }

  /* card central */
  .card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 36px 32px 28px;
    max-width: 420px;
    margin: 0 auto;
    box-shadow: 0 25px 60px rgba(0,0,0,0.4);
  }

  /* logo */
  .logo { text-align: center; margin-bottom: 24px; }
  .logo-icon {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, #e94560, #0f3460);
    border-radius: 16px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    margin-bottom: 10px;
  }
  .logo h1 { color: #fff; font-size: 1.4rem; font-weight: 700; margin: 0; }
  .logo p  { color: rgba(255,255,255,0.45); font-size: 0.85rem; margin: 4px 0 0; }

  /* inputs */
  .stTextInput > div > div > input,
  .stTextInput > div > div > input:focus {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #fff !important;
    padding: 12px 14px !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: #e94560 !important;
    background: rgba(255,255,255,0.1) !important;
    box-shadow: none !important;
  }
  .stTextInput label { color: rgba(255,255,255,0.6) !important; font-size: 0.78rem !important;
    font-weight: 600 !important; text-transform: uppercase; letter-spacing: .06em; }

  /* botão primário */
  .stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #e94560, #c0392b) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 13px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    margin-top: 6px;
    transition: opacity .2s;
  }
  .stButton > button:hover { opacity: .9 !important; }

  /* abas */
  .stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 4px;
    gap: 0;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: rgba(255,255,255,0.5) !important;
    font-weight: 600;
    padding: 9px 20px;
    border: none !important;
  }
  .stTabs [aria-selected="true"] {
    background: #e94560 !important;
    color: #fff !important;
    box-shadow: 0 4px 14px rgba(233,69,96,0.4);
  }
  .stTabs [data-baseweb="tab-highlight"] { display: none; }
  .stTabs [data-baseweb="tab-border"]    { display: none; }

  /* alertas */
  .alerta-ok  { background: rgba(46,213,115,.15); color: #2ed573;
    border: 1px solid rgba(46,213,115,.3); border-radius: 10px;
    padding: 11px 14px; font-size: .88rem; font-weight: 500; margin-top: 10px; }
  .alerta-err { background: rgba(233,69,96,.15); color: #e94560;
    border: 1px solid rgba(233,69,96,.3);  border-radius: 10px;
    padding: 11px 14px; font-size: .88rem; font-weight: 500; margin-top: 10px; }

  /* tela de boas-vindas */
  .welcome { text-align: center; padding: 10px 0; }
  .welcome h2 { color: #fff; font-size: 1.3rem; margin-bottom: 8px; }
  .welcome p  { color: rgba(255,255,255,.5); font-size: .88rem; margin-bottom: 20px; }

  /* botão sair (outline) */
  div[data-testid="stButton"].sair > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: rgba(255,255,255,0.7) !important;
    font-weight: 500 !important;
  }
  div[data-testid="stButton"].sair > button:hover {
    border-color: #e94560 !important;
    color: #e94560 !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Estado da sessão ─────────────────────────────────────────────────────────
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario_id" not in st.session_state:
    st.session_state.usuario_id = None

# ── Card wrapper ─────────────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)

# Logo
st.markdown("""
<div class="logo">
  <div class="logo-icon">🔐</div>
  <h1>Sistema de Login</h1>
  <p>Acesse ou crie sua conta</p>
</div>
""", unsafe_allow_html=True)

# ── Tela logado ───────────────────────────────────────────────────────────────
if st.session_state.logado:
    st.markdown(f"""
    <div class="welcome">
      <div style="font-size:3rem;margin-bottom:12px">🎉</div>
      <h2>Bem-vindo de volta!</h2>
      <p>Autenticado com sucesso &nbsp;·&nbsp; ID: {st.session_state.usuario_id}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Sair", key="btn_sair"):
        st.session_state.logado = False
        st.session_state.usuario_id = None
        st.rerun()

# ── Tela de autenticação ──────────────────────────────────────────────────────
else:
    tab_login, tab_cadastro = st.tabs(["Entrar", "Cadastrar"])

    # ── Login ──────────────────────────────────────────────────────────────
    with tab_login:
        email_l = st.text_input("Email", placeholder="seu@email.com", key="login_email")
        senha_l = st.text_input("Senha", placeholder="••••••••", type="password", key="login_senha")

        if st.button("Entrar", key="btn_login"):
            if not email_l or not senha_l:
                alerta_err(_CAMPOS_OBRIGATORIOS)
            else:
                resultado = ControllerLogin.login(email_l, senha_l)
                if resultado:
                    st.session_state.logado = True
                    st.session_state.usuario_id = resultado['id']
                    st.rerun()
                else:
                    alerta_err("Email ou senha inválidos.")

    # ── Cadastro ───────────────────────────────────────────────────────────
    with tab_cadastro:
        nome_c  = st.text_input("Nome",  placeholder="Seu nome completo", key="cad_nome")
        email_c = st.text_input("Email", placeholder="seu@email.com",     key="cad_email")
        senha_c = st.text_input("Senha", placeholder="Mínimo 6 caracteres",
                                type="password", key="cad_senha")

        if st.button("Criar conta", key="btn_cadastro"):
            if not nome_c or not email_c or not senha_c:
                alerta_err(_CAMPOS_OBRIGATORIOS)
            else:
                resultado = ControllerCadastro.cadastrar(nome_c, email_c, senha_c)
                _mostrar_resultado_cadastro(resultado)

st.markdown('</div>', unsafe_allow_html=True)
