# 🍽️ Sistema de Gerenciamento de Restaurante

## 📋 Tema da Aplicação

Sistema de Gerenciamento de Restaurante para controlar **Receitas** e **Ingredientes** com cálculo automático de lucro.

---

## 🎯 O Que o Sistema Faz

O sistema permite gerenciar um restaurante através de **2 módulos principais**:

### A. Módulo de Receitas
- ✅ Cadastrar receitas com nome, modo de preparo e preço de venda
- ✅ Associar ingredientes às receitas com quantidades específicas
- ✅ Listar todas as receitas cadastradas com cálculo automático de **lucro**
- ✅ Visualizar uma receita específica por ID com análise completa
- ✅ Editar nome, preparo, preço e ingredientes de receitas existentes
- ✅ Remover receitas do sistema
- ✅ **Calcular automaticamente lucro** = preço venda - custo dos ingredientes

### B. Módulo de Ingredientes
- ✅ Cadastrar ingredientes com nome, unidade de medida e custo unitário
- ✅ Listar todos os ingredientes disponíveis
- ✅ Visualizar um ingrediente específico por ID
- ✅ Editar nome, unidade e custo de ingredientes
- ✅ Remover ingredientes (com proteção para ingredientes em uso)

---

## Como o CRUD Foi Aplicado

### A. CREATE (Criar)
- **criar_receita()**: Novo registro de receita com ID automático
- **cadastrar_ingrediente()**: Novo registro de ingrediente com ID automático
- **Validações**: campos obrigatórios, valores numéricos válidos, sem negativos

### B. READ (Ler)
- **listar_receitas()**: Exibe todas as receitas com cálculo automático de lucro
- **listar_ingredientes()**: Exibe todos os ingredientes
- **ler_receita_id()**: Busca e exibe uma receita específica por ID com análise de custos
- **ler_ingredientes_id()**: Busca e exibe um ingrediente específico por ID
- **Tratamento**: mensagem de erro se ID não existir

### C. UPDATE (Atualizar)
- **atualizar_receita()**: Modifica nome, modo de preparo, preço e ingredientes
- **editar_ingrediente()**: Modifica nome, unidade e custo
- **Validações**: rejeita valores negativos, mantém anteriores se inválidos

### D. DELETE (Deletar)
- **deletar_receita()**: Remove uma receita pelo ID
- **deletar_ingrediente()**: Remove ingrediente (protege se estiver em uso)
- **Tratamento**: avisa se ID não encontrado

---

## Estrutura de Dados

### Banco de Dados JSON (data.json)

```json
{
    "receitas": [
        {
            "id": 1,
            "nome": "Pão com Queijo",
            "ingredientes": [
                {"id_ingrediente": 1, "quantidade": 500},
                {"id_ingrediente": 2, "quantidade": 200}
            ],
            "modo_preparo": "Misture farinha, água e sal...",
            "preco_venda": 25.00
        }
    ],
    "ingredientes": [
        {
            "id": 1,
            "nome": "Pão",
            "unidade_medida": "g",
            "custo_unitario": 0.05
        },
        {
            "id": 2,
            "nome": "Queijo",
            "unidade_medida": "g",
            "custo_unitario": 0.15
        }
    ]
}
```

---

## ⚙️ Funcionalidades de Erro

- ✅ **Validação de ID**: Rejeita IDs não encontrados
- ✅ **Validação numérica**: Trata valores negativos e não numéricos
- ✅ **Campos obrigatórios**: Verifica se nome e descrição estão vazios
- ✅ **Proteção de dados**: Impede remover ingredientes em uso em receitas
- ✅ **Armazenamento**: Salva automaticamente em JSON após cada operação
- ✅ **Loops de validação**: Utiliza `while True` com `break` para entrada segura

---

### Visualizar Lucro

Ao listar receitas ou consultar por ID, o sistema mostra automaticamente:
- **Custo Total**: Soma de (custo_unitario × quantidade) para cada ingrediente
- **Lucro**: Preço de venda - Custo total

Exemplo:
```
Receita: Pão com Queijo
Preço de Venda: R$ 25.00
Custo Total: R$ 10.00
Lucro: R$ 15.00
```

---

## Validações Implementadas

### Entrada de Dados
- Não aceita campos vazios
- Não aceita valores negativos
- Aceita apenas unidades: `g`, `ml`, `un`
- Rejeita IDs duplicados ou inválidos

### Operações
- Só delete ingrediente se não estiver em nenhuma receita
- Mantém dados anteriores se atualização falhar
- Avisa quando ID não é encontrado

---

## Tecnologias Utilizadas

- **Python**: Linguagem de programação
- **JSON**: Armazenamento de dados
- **Módulos padrão**: `json`, `os`