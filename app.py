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
    receitas = dados["receitas"]
    ingredientes = dados["ingredientes"]

    print("\n--- CADASTRAR NOVA RECEITA ---")
    while True:
        nome = input('Nome da receita: ').strip()
        if nome:
            break
        print("Erro: Nome da receita é obrigatório!")

    ingredientes_da_receita = []

    if not ingredientes:
        print("Aviso: Não há ingredientes cadastrados. Cadastre-os primeiro no menu de ingredientes.")
    else:
        while True:
            print("\nIngredientes disponíveis:")
            for ing in ingredientes:
                print(f"ID: {ing['id']} | Nome: {ing['nome']}")

            id_ing = input(
                "\nID do ingrediente para adicionar (ou '0' para finalizar): ")
            if id_ing == '0':
                break

            try:
                id_ing = int(id_ing)
                ing_encontrado = None
                for ing in ingredientes:
                    if ing["id"] == id_ing:
                        ing_encontrado = ing
                        break

                if ing_encontrado:
                    while True:
                        try:
                            qtd = int(input(
                                f"Quantidade de {ing_encontrado['nome']} ({ing_encontrado['unidade_medida']}): "))
                            if qtd > 0:
                                ingredientes_da_receita.append({
                                    "id_ingrediente": id_ing,
                                    "quantidade": qtd
                                })
                                print("Ingrediente adicionado!")
                                break
                            else:
                                print("Erro: A quantidade deve ser maior que zero.")
                        except ValueError:
                            print("Erro: A quantidade deve ser um número inteiro.")
                else:
                    print("Erro: ID de ingrediente não encontrado na lista!")

            except ValueError:
                print("Erro: Digite um número de ID válido.")

    while True:
        modo_preparo = input('Modo de preparo: ').strip()
        if modo_preparo:
            break
        print("Erro: Modo de preparo é obrigatório!")

    while True:
        try:
            preco = float(input('Preço de venda: '))
            if preco >= 0:
                preco = round(preco, 2)
                break
            else:
                print("Erro: Preço não pode ser negativo!")
        except ValueError:
            print("Erro: Preço deve ser um número válido!")

    novo_id = 1
    if receitas:
        novo_id = len(receitas) + 1
    receita = {
        "id": novo_id,
        "nome": nome,
        "ingredientes": ingredientes_da_receita,
        "modo_preparo": modo_preparo,
        "preco_venda": preco
    }

    receitas.append(receita)
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

        custo_total = 0
        for item in receita["ingredientes"]:
            for ing in lista_ingrediente:
                if ing["id"] == item["id_ingrediente"]:
                    custo_total += ing["custo_unitario"] * item["quantidade"]
                    break

        print(
            f'ID: {receita["id"]} | Nome: {receita["nome"]} | Preço: R${receita["preco_venda"]}')
        print('Ingredientes:')
        if not receita["ingredientes"]:
            print("(Sem ingredientes listados)")
        else:
            for item in receita["ingredientes"]:
                ing_nome = ""
                ing_unid = ""

                for ing in lista_ingrediente:
                    if ing["id"] == item["id_ingrediente"]:
                        ing_nome = ing["nome"]
                        ing_unid = ing["unidade_medida"]
                        break
                print(
                    f"  - {item['quantidade']} {ing_unid} de {ing_nome}")

        print(f'Preparo: {receita["modo_preparo"]}')
        lucro = receita["preco_venda"] - custo_total
        print(f'Custo Total: R${custo_total:.2f} | Lucro: R${lucro:.2f}')
        print('-' * 40)


def ler_receita_id():
    dados = carregar()
    receitas = dados["receitas"]
    ingredientes = dados["ingredientes"]
    try:
        id_busca = int(input('Digite o ID da receita: '))
    except ValueError:
        print("Erro: ID deve ser um número inteiro!")
        return

    for receita in receitas:
        if receita["id"] == id_busca:

            custo_total = 0
            for item in receita["ingredientes"]:
                for ing in ingredientes:
                    if ing["id"] == item["id_ingrediente"]:
                        custo_total += ing["custo_unitario"] * \
                            item["quantidade"]
                        break

            print(
                f'ID: {receita["id"]} | Nome: {receita["nome"]} | Preço: R${receita["preco_venda"]}')
            print('Ingredientes:')
            if not receita["ingredientes"]:
                print("(Sem ingredientes listados)")
            else:
                for item in receita["ingredientes"]:
                    ing_nome = ""
                    ing_unid = ""

                    for ing in ingredientes:
                        if ing["id"] == item["id_ingrediente"]:
                            ing_nome = ing["nome"]
                            ing_unid = ing["unidade_medida"]
                            break
                    print(
                        f"  - {item['quantidade']} {ing_unid} de {ing_nome}")

            print(f'Preparo: {receita["modo_preparo"]}')
            lucro = receita["preco_venda"] - custo_total
            print(f'Custo Total: R${custo_total:.2f} | Lucro: R${lucro:.2f}')
            return

    print('Erro: ID não encontrado.')


def atualizar_receita():
    dados = carregar()
    receitas = dados["receitas"]
    ingredientes = dados["ingredientes"]
    try:
        id_busca = int(input('ID da receita a editar: '))
    except ValueError:
        print("Erro: ID inválido!")
        return

    for receita in receitas:
        if receita["id"] == id_busca:
            print(f"\n--- Editando: {receita['nome']} ---")

            novo_nome = input(
                f'Novo nome (Atual: {receita["nome"]}): ').strip()
            novo_preparo = input(
                f'Novo preparo (Atual: {receita["modo_preparo"]}): ').strip()
            novo_preco = input(
                f'Novo preço (Atual: R${receita["preco_venda"]}): ').strip()

            if novo_nome:
                receita["nome"] = novo_nome
            if novo_preparo:
                receita["modo_preparo"] = novo_preparo
            if novo_preco:
                while True:
                    try:
                        preco_float = float(novo_preco)
                        if preco_float >= 0:
                            receita["preco_venda"] = round(preco_float, 2)
                            break
                        else:
                            print("Erro: Preço não pode ser negativo!")
                            novo_preco = input(
                                f'Novo preço (Atual: R${receita["preco_venda"]}): ').strip()
                    except ValueError:
                        print("Erro: Preço deve ser um número válido!")
                        novo_preco = input(
                            f'Novo preço (Atual: R${receita["preco_venda"]}): ').strip()

            while True:
                print("\nIngredientes atuais desta receita:")
                if not receita["ingredientes"]:
                    print("  (Lista vazia)")
                else:
                    for item in receita["ingredientes"]:
                        nome_ing = "Desconhecido"
                        unidade_ing = ""
                        for ing_mestre in ingredientes:
                            if ing_mestre["id"] == item["id_ingrediente"]:
                                nome_ing = ing_mestre["nome"]
                                unidade_ing = ing_mestre["unidade_medida"]
                                break
                        print(
                            f"  - {nome_ing}: {item['quantidade']} {unidade_ing}")

                print("\nOpções de ingredientes:")
                print(
                    "1 - Adicionar | 2 - Remover | 3 - Limpar tudo | 0 - Salvar e Sair")
                op_ing = input("Escolha: ")

                if op_ing == '1':
                    print("\nDisponíveis no sistema:")
                    for ing in ingredientes:
                        print(
                            f"ID: {ing['id']} | {ing['nome']} ({ing['unidade_medida']})")

                    try:
                        id_novo = int(
                            input("ID do ingrediente para adicionar: "))
                        ing_mestre_encontrado = None
                        for ing in ingredientes:
                            if ing["id"] == id_novo:
                                ing_mestre_encontrado = ing
                                break

                        if ing_mestre_encontrado:
                            unid = ing_mestre_encontrado['unidade_medida']
                            try:
                                qtd = int(
                                    input(f"Quantidade de {ing_mestre_encontrado['nome']} em ({unid}): "))
                                if qtd <= 0:
                                    print(
                                        "Erro: A quantidade deve ser maior que zero.")
                                else:
                                    receita["ingredientes"].append({
                                        "id_ingrediente": id_novo,
                                        "quantidade": qtd
                                    })
                                    print("Adicionado!")
                            except ValueError:
                                print(
                                    "Erro: A quantidade deve ser um número inteiro.")
                        else:
                            print("Erro: Ingrediente não encontrado no sistema.")
                    except ValueError:
                        print("Erro: Digite apenas números.")

                elif op_ing == '2':
                    try:
                        id_remov = int(
                            input("ID do ingrediente para REMOVER desta receita: "))
                        removido = False
                        for i in range(len(receita["ingredientes"])):
                            if receita["ingredientes"][i]["id_ingrediente"] == id_remov:
                                receita["ingredientes"].pop(i)
                                removido = True
                                print("Removido!")
                                break
                        if not removido:
                            print("ID não está na lista desta receita.")
                    except ValueError:
                        print("Erro: ID inválido.")

                elif op_ing == '3':
                    receita["ingredientes"] = []
                    print("Lista limpa!")

                elif op_ing == '0':
                    break

            salvar(dados)
            print('\nAlterações salvas com sucesso!')
            return

    print('Erro: Receita não encontrada.')


def deletar_receita():
    dados = carregar()
    receitas = dados["receitas"]
    try:
        id_busca = int(input('ID da receita a remover: '))
    except ValueError:
        print("Erro: ID inválido!")
        return

    for receita in receitas:
        if receita["id"] == id_busca:
            receitas.remove(receita)
            salvar(dados)
            print('Receita removida com sucesso!')
            return

    print('Erro: ID não encontrado.')


def cadastrar_ingrediente():
    dados = carregar()
    ingredientes = dados["ingredientes"]

    while True:
        nome = input('Nome do ingrediente: ').strip()
        if nome:
            break
        print('Erro: Nome do ingrediente é obrigatório!')

    while True:
        unidade = input('Unidade de medida (g, ml, un): ').strip().lower()
        if unidade in ['g', 'ml', 'un']:
            break
        print('Erro: Unidade deve ser g, ml ou un!')

    while True:
        try:
            custo = float(input('Custo unitário: '))
            if custo >= 0:
                custo = round(custo, 3)
                break
            else:
                print('Erro: Custo não pode ser negativo!')
        except ValueError:
            print('Erro: Custo deve ser um número válido.')

    novo_id = 1
    if ingredientes:
        novo_id = len(ingredientes) + 1

    ingrediente = {
        "id": novo_id,
        "nome": nome,
        "unidade_medida": unidade,
        "custo_unitario": custo
    }

    ingredientes.append(ingrediente)
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
            f'Custo: R${ing["custo_unitario"]}'
        )


def ler_ingredientes_id():
    dados = carregar()
    ingredientes = dados["ingredientes"]

    try:
        id_busca = int(input('Digite o ID do ingrediente: '))
    except ValueError:
        print("Erro: ID deve ser um número inteiro!")
        return

    for ing in ingredientes:
        if ing["id"] == id_busca:
            print('Ingrediente:')
            print(
                f'ID: {ing["id"]} | Nome: {ing["nome"]} | Unidade de medida: {ing["unidade_medida"]} | Custo unitario: R${ing["custo_unitario"]}')
            return

    print('Erro: ID não encontrado.')


def editar_ingrediente():
    dados = carregar()
    ingredientes = dados["ingredientes"]
    try:
        id_busca = int(input('ID do ingrediente a editar: '))
    except ValueError:
        print('Erro: ID inválido.')
        return

    for ing in ingredientes:
        if ing["id"] == id_busca:
            print(f"Editando: {ing['nome']}")
            nome = input('Novo nome (vazio para manter): ').strip()
            unid = input('Nova unidade (vazio para manter): ').strip().lower()
            custo = input('Novo custo (vazio para manter): ').strip()

            if nome:
                ing["nome"] = nome
            if unid:
                while True:
                    if unid in ['g', 'ml', 'un']:
                        ing["unidade_medida"] = unid
                        break
                    else:
                        print('Erro: Unidade deve ser g, ml ou un!')
                        unid = input(
                            'Nova unidade (vazio para manter): ').strip().lower()
                        if not unid:
                            break
            if custo:
                while True:
                    try:
                        custo_float = float(custo)
                        if custo_float >= 0:
                            ing["custo_unitario"] = round(custo_float, 3)
                            break
                        else:
                            print("Erro: Custo não pode ser negativo!")
                            custo = input(
                                'Novo custo (vazio para manter): ').strip()
                            if not custo:
                                break
                    except ValueError:
                        print("Erro: Custo deve ser um número válido!")
                        custo = input(
                            'Novo custo (vazio para manter): ').strip()
                        if not custo:
                            break

            salvar(dados)
            print('Ingrediente atualizado com sucesso!')
            return
    print('Erro: ingrediente não encontrado.')


def deletar_ingrediente():
    dados = carregar()
    receitas = dados["receitas"]
    ingredientes = dados["ingredientes"]

    try:
        id_busca = int(input('Digite o ID do ingrediente a remover: '))
    except ValueError:
        print('Erro: ID inválido.')
        return

    for receita in receitas:
        for item in receita["ingredientes"]:
            if item["id_ingrediente"] == id_busca:
                print('Erro: ingrediente está sendo usado em uma receita.')
                return

    for ing in ingredientes:
        if ing["id"] == id_busca:
            ingredientes.remove(ing)
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
==== GERENCIAR RECEITAS ====

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
            elif op == '3':
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
