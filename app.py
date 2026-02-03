import json

def data_creat(dados):
    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(dados, json_file, indent=4, ensure_ascii=False)

def data_read():
    with open('data.json', 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


menu = '''
==== SISTEMA DE RESTAURANTE ====

1 - Gerenciar Alimentos
2 - Gerenciar Ingredientes
3 - Listar Cardápio
0 - Sair
'''

menu_alimentos = '''
==== GERENCIAR ALIMENTOS ====

1 - Cadastrar alimento
2 - Listar alimentos
3 - Editar alimento
4 - Remover alimento
0 - Voltar
'''

menu_ingredientes = '''
==== GERENCIAR INGREDIENTES ====

1 - Cadastrar ingrediente
2 - Listar ingredientes
3 - Editar ingrediente
4 - Remover ingrediente
0 - Voltar
'''

while True:
    print(menu)
    escolha = input('Escolha uma opção: ')

    if escolha == '1':
        while True:
            print(menu_alimentos)
            opcao_alimento = input('Escolha uma opção: ')

            if opcao_alimento == '0':
                break
            else:
                print('Escolha uma opção disponível!\n')

    elif escolha == '2':
        while True:
            print(menu_ingredientes)
            opcao_ingrediente = input('Escolha uma opção: ')

            if opcao_ingrediente == '0':
                break
            else:
                print('Escolha uma opção disponível!\n')

    elif escolha == '3':
        print('Listagem do cardápio ainda não implementada.\n')

    elif escolha == '0':
        print('Saindo do sistema...')
        break

    else:
        print('Escolha uma opção disponível!\n')
