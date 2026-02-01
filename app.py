
import streamlit as st
import requests

API_URL = "http://localhost:8000"

def get_token():
    return st.session_state.get("token", None)

def set_token(token):
    st.session_state["token"] = token

def login_form():
    st.subheader("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        resp = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
        if resp.status_code == 200:
            token = resp.json()["access_token"]
            set_token(token)
            st.success("Login realizado!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos")

def register_form():
    st.subheader("Cadastro de Usuário")
    username = st.text_input("Usuário novo")
    email = st.text_input("E-mail novo")
    password = st.text_input("Senha nova", type="password")
    if st.button("Cadastrar"):
        data = {"username": username, "email": email, "password": password}
        resp = requests.post(f"{API_URL}/register", json=data)
        if resp.status_code == 200:
            st.success("Usuário cadastrado! Faça login.")
        else:
            st.error("Erro ao cadastrar usuário")

def auth_menu():
    menu = ["Login", "Cadastrar"]
    escolha = st.sidebar.selectbox("Acesso", menu)
    if escolha == "Login":
        login_form()
    else:
        register_form()


def main_menu():
    menu = ["Listar Clientes", "Adicionar Cliente", "Gerenciar Contatos", "Sair"]
    escolha = st.sidebar.selectbox("Menu", menu)
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    if escolha == "Listar Clientes":
        st.header("Lista de Clientes")
        resp = requests.get(f"{API_URL}/clientes/", headers=headers)
        if resp.status_code == 200:
            clientes = resp.json()
            for c in clientes:
                st.write(f"**{c['nome']}** | {c['email']} | {c['telefone']} | {c['status']}")
                if st.button(f"Editar {c['id']}"):
                    st.session_state['edit_id'] = c['id']
                if st.button(f"Excluir {c['id']}"):
                    requests.delete(f"{API_URL}/clientes/{c['id']}", headers=headers)
                    st.experimental_rerun()
        else:
            st.error("Erro ao buscar clientes")

        if 'edit_id' in st.session_state:
            cliente_id = st.session_state['edit_id']
            resp = requests.get(f"{API_URL}/clientes/{cliente_id}", headers=headers)
            if resp.status_code == 200:
                c = resp.json()
                st.subheader("Editar Cliente")
                nome = st.text_input("Nome", c['nome'])
                email = st.text_input("Email", c['email'])
                telefone = st.text_input("Telefone", c['telefone'])
                endereco = st.text_input("Endereço", c['endereco'])
                status = st.selectbox("Status", ["ativo", "inativo"], index=0 if c['status']=="ativo" else 1)
                if st.button("Salvar Alterações"):
                    data = {"nome": nome, "email": email, "telefone": telefone, "endereco": endereco, "status": status}
                    requests.put(f"{API_URL}/clientes/{cliente_id}", json=data, headers=headers)
                    del st.session_state['edit_id']
                    st.experimental_rerun()
    elif escolha == "Adicionar Cliente":
        st.header("Adicionar Cliente")
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        telefone = st.text_input("Telefone")
        endereco = st.text_input("Endereço")
        status = st.selectbox("Status", ["ativo", "inativo"])
        if st.button("Adicionar"):
            data = {"nome": nome, "email": email, "telefone": telefone, "endereco": endereco, "status": status}
            resp = requests.post(f"{API_URL}/clientes/", json=data, headers=headers)
            if resp.status_code == 200:
                st.success("Cliente adicionado com sucesso!")
                st.experimental_rerun()
            else:
                st.error("Erro ao adicionar cliente")
    elif escolha == "Gerenciar Contatos":
        st.header("Gerenciar Contatos")
        # Selecionar cliente para gerenciar contatos
        resp = requests.get(f"{API_URL}/clientes/", headers=headers)
        if resp.status_code == 200:
            clientes = resp.json()
            cliente_nomes = [f"{c['id']} - {c['nome']}" for c in clientes]
            cliente_idx = st.selectbox("Selecione o cliente", range(len(clientes)), format_func=lambda i: cliente_nomes[i] if clientes else "")
            if clientes:
                cliente_id = clientes[cliente_idx]['id']
                # Listar contatos
                resp_contatos = requests.get(f"{API_URL}/contatos/{cliente_id}", headers=headers)
                if resp_contatos.status_code == 200:
                    contatos = resp_contatos.json()
                    st.subheader("Contatos cadastrados")
                    for contato in contatos:
                        st.write(f"{contato['nome']} | {contato['telefone']}")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"Editar Contato {contato['id']}"):
                                st.session_state['edit_contato_id'] = contato['id']
                        with col2:
                            if st.button(f"Excluir Contato {contato['id']}"):
                                requests.delete(f"{API_URL}/contatos/{contato['id']}", headers=headers)
                                st.experimental_rerun()
                    # Editar contato
                    if 'edit_contato_id' in st.session_state:
                        contato_id = st.session_state['edit_contato_id']
                        contato = next((c for c in contatos if c['id'] == contato_id), None)
                        if contato:
                            st.subheader("Editar Contato")
                            nome = st.text_input("Nome do Contato", contato['nome'])
                            telefone = st.text_input("Telefone do Contato", contato['telefone'])
                            if st.button("Salvar Alterações do Contato"):
                                data = {"nome": nome, "telefone": telefone}
                                requests.put(f"{API_URL}/contatos/{contato_id}", json=data, headers=headers)
                                del st.session_state['edit_contato_id']
                                st.experimental_rerun()
                # Adicionar novo contato
                st.subheader("Adicionar Novo Contato")
                nome = st.text_input("Nome do Novo Contato")
                telefone = st.text_input("Telefone do Novo Contato")
                if st.button("Adicionar Contato"):
                    data = {"nome": nome, "telefone": telefone, "cliente_id": cliente_id}
                    resp = requests.post(f"{API_URL}/contatos/", json=data, headers=headers)
                    if resp.status_code == 200:
                        st.success("Contato adicionado com sucesso!")
                        st.experimental_rerun()
                    else:
                        st.error("Erro ao adicionar contato")
        else:
            st.error("Erro ao buscar clientes para contatos")
    elif escolha == "Sair":
        st.session_state.pop("token", None)
        st.success("Logout realizado!")
        st.experimental_rerun()

def main():
    st.title("ERP de Gerenciamento de Clientes - SaaS")
    if get_token() is None:
        auth_menu()
    else:
        main_menu()

if __name__ == "__main__":
    main()
