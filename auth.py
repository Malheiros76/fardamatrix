# auth.py

import bcrypt
import streamlit as st

def hash_senha(senha: str) -> bytes:
    """Gera hash da senha usando bcrypt"""
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

def verificar_senha(senha_plain: str, senha_hash: bytes) -> bool:
    """Compara senha digitada com hash armazenado"""
    if isinstance(senha_hash, str):
        senha_hash = senha_hash.encode('utf-8')
    return bcrypt.checkpw(senha_plain.encode(), senha_hash)

def autenticar(usuario: str, senha: str, usuarios_col) -> bool:
    """Autentica usuário e define sessão"""
    user = usuarios_col.find_one({"usuario": usuario})
    if user and verificar_senha(senha, user["senha"]):
        st.session_state['usuario_logado'] = usuario
        st.session_state['nivel_usuario'] = user.get("nivel", "user")
        st.session_state['logado'] = True
        return True
    return False
