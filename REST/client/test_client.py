import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def test_crud_operations():
    # CREATE - Criar alguns itens
    print("\n=== Testando CREATE ===")
    create_response1 = requests.post(f'{BASE_URL}/item', 
                                   json={'name': 'Item 1','email':'joao@gmail.com','password':'teste'})
    print(f"Criando Item 1: {create_response1.json()}")
    
    create_response2 = requests.post(f'{BASE_URL}/item', 
                                   json={'name': 'Item 2','email':'giga@funga','password':'123'})
    print(f"Criando Item 2: {create_response2.json()}")

    # READ - Listar todos os itens
    print("\n=== Testando READ (todos) ===")
    read_all_response = requests.get(f'{BASE_URL}/items')
    print(f"Lista de itens: {read_all_response.json()}")

if __name__ == "__main__":
    try:
        test_crud_operations()
    except requests.exceptions.ConnectionError:
        print("Erro: Não foi possível conectar ao servidor. Certifique-se que ele está rodando na porta 5000.")
