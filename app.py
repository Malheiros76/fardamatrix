from auth import autenticar
from db import get_db

# bancos de  dados
db = get_db()
usuarios_col = db["usuarios"]
cadastro_col = db["cadastro"]
produtos_col = db["produtos"]
movimentacao_col = db["movimentacao"]
alunos_col = db["alunos"]
movimentacao_aluno_col = db["movimentacao_aluno"]

# Autenticação

if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.subheader("Login do Sistema")
    with st.form("login"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.form_submit_button("Entrar"):
            if autenticar(usuario.strip(), senha.strip(), usuarios_col):
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")
