import json
import os

ARQUIVO_JSON = 'data.json'


def carregar():
    if not os.path.exists(ARQUIVO_JSON):
        return {"receitas": [], "ingredientes": []}

    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as json_file:
        try:
            dados = json.load(json_file)
            if "receitas" not in dados:
                dados["receitas"] = []
            if "ingredientes" not in dados:
                dados["ingredientes"] = []
            return dados
        except (json.JSONDecodeError, ValueError):
            return {"receitas": [], "ingredientes": []}


def salvar(dados):
    with open(ARQUIVO_JSON, 'w', encoding='utf-8') as json_file:
        json.dump(dados, json_file, indent=4, ensure_ascii=False)


def criar_receita():
    dados = carregar()
    lista = dados["receitas"]

    print("\n--- CADASTRAR NOVA RECEITA ---")
    nome = input('Nome da receita: ').strip()

    ingredientes_da_receita = []

    if not dados["ingredientes"]:
        print("Aviso: Não há ingredientes cadastrados. Cadastre-os primeiro no menu de ingredientes.")
    else:
        while True:
            print("\nIngredientes disponíveis:")
            for ing in dados["ingredientes"]:
                print(f"ID: {ing['id']} | Nome: {ing['nome']}")

            id_ing = input(
                "\nID do ingrediente para adicionar (ou '0' para finalizar): ")
            if id_ing == '0':
                break

            try:
                id_ing = int(id_ing)
                ing_encontrado = None
                for ing in dados["ingredientes"]:
                    if ing["id"] == id_ing:
                        ing_encontrado = ing
                        break

                if ing_encontrado:
                    try:
                        qtd_texto = input(
                            f"Quantidade de {ing_encontrado['nome']} ({ing_encontrado['unidade_medida']}): ")
                        qtd = int(qtd_texto)

                        ingredientes_da_receita.append({
                            "id_ingrediente": id_ing,
                            "quantidade": qtd
                        })
                        print("Ingrediente adicionado com sucesso!")

                    except ValueError:
                        print("Erro: A quantidade deve ser um número inteiro.")
                else:
                    print("Erro: ID de ingrediente não encontrado.")
            except ValueError:
                print("Erro: Digite números válidos.")

    modo_preparo = input('Modo de preparo: ').strip()

    if not nome or not modo_preparo:
        print("Erro: Nome e Modo de Preparo são obrigatórios!")
        return

    try:
        preco = float(input('Preço de venda: '))
    except ValueError:
        print("Erro: Preço deve ser um número válido!")
        return

    novo_id = len(dados["receitas"]) + 1
    receita = {
        "id": novo_id,
        "nome": nome,
        "ingredientes": ingredientes_da_receita,
        "modo_preparo": modo_preparo,
        "preco_venda": preco
    }

    lista.append(receita)
    salvar(dados)
    print(f'Receita "{nome}" cadastrada com sucesso!')


def listar_receitas():
    dados = carregar()
    lista_receita = dados["receitas"]
    lista_ingrediente = dados["ingredientes"]

    if not lista_receita:
        print('\nNenhuma receita cadastrada.')
        return

    print("\n--- LISTA DE RECEITAS ---")
    for receita in lista_receita:
        print(
            f'ID: {receita["id"]} | Nome: {receita["nome"]} | Preço: R${receita["preco_venda"]}')
        print('Ingredientes:')
        if not receita["ingredientes"]:
            print("(Sem ingredientes listados)")
        else:
            for item in receita["ingredientes"]:
                ing_nome = ""
                ing_unid = 0

                for ing in lista_ingrediente:
                    if ing["id"] == item["id_ingrediente"]:
                        ing_nome = ing["nome"]
                        ing_unid = ing["unidade_medida"]
                        break
            print(f"  - {item['quantidade']} {ing_unid} de {ing_nome}")

        print(f'Preparo: {receita["modo_preparo"]}')
        print('-' * 40)


def ler_receita_id():
    dados = carregar()
    try:
        id_busca = int(input('Digite o ID da receita: '))
    except ValueError:
        print("Erro: ID deve ser um número inteiro!")
        return

    for receita in dados["receitas"]:
        if receita["id"] == id_busca:
            lista_ingrediente = dados["ingredientes"]
            print(f'ID: {receita["id"]} | Nome: {receita["nome"]} | Preço: R${receita["preco_venda"]}')
            print('Ingredientes:')
            if not receita["ingredientes"]:
                print("(Sem ingredientes listados)")
            else:
                for item in receita["ingredientes"]:
                    ing_nome = ""
                    ing_unid = 0

                    for ing in lista_ingrediente:
                        if ing["id"] == item["id_ingrediente"]:
                            ing_nome = ing["nome"]
                            ing_unid = ing["unidade_medida"]
                            break
                print(f"  - {item['quantidade']} {ing_unid} de {ing_nome}")

            print(f'Preparo: {receita["modo_preparo"]}')
            return

    print('Erro: ID não encontrado.')


def atualizar_receita():
    dados = carregar()
    try:
        id_busca = int(input('ID da receita a editar: '))
    except ValueError:
        print("Erro: ID inválido!")
        return

    for receita in dados["receitas"]:
        if receita["id"] == id_busca:
            print(f"Editando: {receita['nome']}")

            novo_nome = input('Novo nome (deixe vazio para manter): ').strip()
            novo_preparo = input(
                'Novo preparo (deixe vazio para manter): ').strip()
            novo_preco = input(
                'Novo preço (deixe vazio para manter): ').strip()

            if novo_nome:
                receita["nome"] = novo_nome
            if novo_preparo:
                receita["modo_preparo"] = novo_preparo
            if novo_preco:
                try:
                    receita["preco_venda"] = float(novo_preco)
                except ValueError:
                    print("Preço inválido! Mantendo o anterior.")

            salvar(dados)
            print('Receita atualizada com sucesso!')
            return

    print('Erro: ID não encontrado.')


def deletar_receita():
    dados = carregar()
    try:
        id_busca = int(input('ID da receita a remover: '))
    except ValueError:
        print("Erro: ID inválido!")
        return

    for receita in dados["receitas"]:
        if receita["id"] == id_busca:
            dados["receitas"].remove(receita)
            salvar(dados)
            print('Receita removida com sucesso!')
            return

    print('Erro: ID não encontrado.')


def cadastrar_ingrediente():
    dados = carregar()

    nome = input('Nome do ingrediente: ')
    unidade = input('Unidade de medida (g, ml, un): ')
    try:
        custo = float(input('Custo unitário: '))
    except ValueError:
        print('Erro: custo inválido.')
        return

    novo_id = 1
    if dados["ingredientes"]:
        novo_id = dados["ingredientes"][-1]["id"] + 1

    ingrediente = {
        "id": novo_id,
        "nome": nome,
        "unidade_medida": unidade,
        "custo_unitario": round(custo, 2)
    }

    dados["ingredientes"].append(ingrediente)
    salvar(dados)

    print('Ingrediente cadastrado com sucesso!\n')

def listar_ingredientes():
    dados = carregar()
    ingredientes = dados["ingredientes"]

    if not ingredientes:
        print('\nNenhum ingrediente cadastrado.')
        return

    print('\n--- LISTA DE INGREDIENTES ---')
    for ing in ingredientes:
        print(
            f'ID: {ing["id"]} | '
            f'Nome: {ing["nome"]} | '
            f'Unidade: {ing["unidade_medida"]} | '
            f'Custo: R${ing["custo_unitario"]:.2f}'
        )


def ler_ingredientes_id():
    dados = carregar()
    try:
        id_busca = int(input('Digite o ID do ingrediente: '))
    except ValueError:
        print("Erro: ID deve ser um número inteiro!")
        return

    for ing in dados["ingredientes"]:
        if ing["id"] == id_busca:
            print('Ingrediente:')
            print(f'ID: {ing["id"]} | Nome: {ing["nome"]} | Unidade de medida: {ing["unidade_medida"]} | Custo unitario: R${ing["custo_unitario"]}')
            if not ing["ingredientes"]:
                print("Sem ingrediente com esse ID listado!")

    print('Erro: ID não encontrado.')

def editar_ingrediente():
    dados = carregar()

    try:
        id_busca = int(input('Digite o ID do ingrediente a editar: '))
    except ValueError:
        print('Erro: ID inválido.')
        return

    for ing in dados["ingredientes"]:
        if ing["id"] == id_busca:
            ing["nome"] = input('Novo nome: ')
            ing["unidade_medida"] = input('Nova unidade de medida: ')
            try:
                ing["custo_unitario"] = round(
                    float(input('Novo custo unitário: ')), 2
                )
            except ValueError:
                print('Erro: custo inválido.')
                return

            salvar(dados)
            print('Ingrediente atualizado com sucesso!\n')
            return

    print('Erro: ingrediente não encontrado.')

def deletar_ingrediente():
    dados = carregar()

    try:
        id_busca = int(input('Digite o ID do ingrediente a remover: '))
    except ValueError:
        print('Erro: ID inválido.')
        return

    for receita in dados["receitas"]:
        for item in receita["ingredientes"]:
            if item["id_ingrediente"] == id_busca:
                print('Erro: ingrediente está sendo usado em uma receita.')
                return

    for ing in dados["ingredientes"]:
        if ing["id"] == id_busca:
            dados["ingredientes"].remove(ing)
            salvar(dados)
            print('Ingrediente removido com sucesso!\n')
            return

    print('Erro: ingrediente não encontrado.')


menu = '''
==== SISTEMA DE RESTAURANTE ====

1 - Gerenciar receitas
2 - Gerenciar Ingredientes
0 - Sair
'''

menu_receitas = '''
==== GERENCIAR receitaS ====

1 - Cadastrar receita
2 - Listar receitas
3 - Ver receita por id
4 - Editar receita
5 - Remover receita
0 - Voltar
'''

menu_ingredientes = '''
==== GERENCIAR INGREDIENTES ====

1 - Cadastrar ingrediente
2 - Listar ingredientes
3 - Ver ingrediente por id
4 - Editar ingrediente
5 - Remover ingrediente
0 - Voltar
'''

while True:
    print(menu)
    escolha = input('Escolha uma opção: ')

    if escolha == '1':
        while True:
            print(menu_receitas)
            op = input('Escolha uma opção: ')
            if op == '1':
                criar_receita()
            elif op == '2':
                listar_receitas()
            elif op == '3':
                ler_receita_id()
            elif op == '4':
                atualizar_receita()
            elif op == '5':
                deletar_receita()
            elif op == '0':
                break
            else:
                print('Escolha uma opção disponivel!')

    elif escolha == '2':
        while True:
            print(menu_ingredientes)
            op = input('Escolha uma opção: ')

            if op == '0':
                break
            elif op == '1':
                cadastrar_ingrediente()
            elif op == '2':
                listar_ingredientes()
            elif op =='3':
                ler_ingredientes_id()
            elif op == '4':
                editar_ingrediente()
            elif op == '5':
                deletar_ingrediente()
            else:
                print('Escolha uma opção disponível!\n')

    elif escolha == '0':
        print('Saindo do sistema...')
        break

    else:
        print('Escolha uma opção disponível!\n')
