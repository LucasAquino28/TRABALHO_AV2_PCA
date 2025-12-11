import pandas as pd
import os

ARQUIVO = "alunos.csv"
COLUNAS = ["Matricula", "Nome", "Rua", "Numero", "Bairro", "Cidade", "UF", "Telefone", "Email"]

# -------------------------------------------------------------------

def carregar_dados():
    """Carrega o arquivo CSV ou cria um dataframe vazio."""
    if os.path.exists(ARQUIVO):
        df = pd.read_csv(ARQUIVO)

        
        for c in COLUNAS:
            if c not in df.columns:
                df[c] = ""

        
        df["Matricula"] = pd.to_numeric(df["Matricula"], errors="coerce").fillna(0).astype(int)

        return df
    else:
        return pd.DataFrame(columns=COLUNAS)

# -------------------------------------------------------------------

def salvar_dados(df):
    """Salva o dataframe no arquivo CSV."""
    df.to_csv(ARQUIVO, index=False)

# -------------------------------------------------------------------

def gerar_matricula(df):
    """Gera a próxima matrícula automaticamente."""
    if df.empty:
        return 1
    else:
        return int(df["Matricula"].max()) + 1

# -------------------------------------------------------------------

def inserir(df):
    print("\n=== INSERIR ALUNO ===")

    matricula = gerar_matricula(df)
    print("Matrícula gerada:", matricula)

    nome = input("Nome: ")
    rua = input("Rua: ")
    numero = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    uf = input("UF: ")
    telefone = input("Telefone: ")
    email = input("Email: ")

    aluno = {
        "Matricula": matricula,
        "Nome": nome,
        "Rua": rua,
        "Numero": numero,
        "Bairro": bairro,
        "Cidade": cidade,
        "UF": uf,
        "Telefone": telefone,
        "Email": email
    }

    
    df = pd.concat([df, pd.DataFrame([aluno])], ignore_index=True)

    salvar_dados(df)
    print("Aluno cadastrado com sucesso!\n")
    return df

# -------------------------------------------------------------------

def mostrar_aluno(aluno):
    print("\n--- DADOS DO ALUNO ---")
    for campo in COLUNAS:
        print(f"{campo}: {aluno[campo]}")
    print("-----------------------\n")

# -------------------------------------------------------------------

def editar(df, indice):
    aluno = df.loc[indice]
    mostrar_aluno(aluno)

    print("Qual campo deseja editar?")
    print("1 - Nome")
    print("2 - Rua")
    print("3 - Número")
    print("4 - Bairro")
    print("5 - Cidade")
    print("6 - UF")
    print("7 - Telefone")
    print("8 - Email")
    print("0 - Cancelar")

    opc = input("Opção: ")

    campos_editaveis = COLUNAS[1:]  

    if opc == "0":
        print("Edição cancelada.\n")
        return df

    if opc.isdigit() and 1 <= int(opc) <= 8:
        campo = campos_editaveis[int(opc) - 1]
        novo_valor = input(f"Novo valor para {campo}: ")
        df.at[indice, campo] = novo_valor
        salvar_dados(df)
        print("Dados atualizados!\n")
    else:
        print("Opção inválida.\n")

    return df

# -------------------------------------------------------------------

def remover(df, indice):
    aluno = df.loc[indice]
    mostrar_aluno(aluno)

    confirm = input("Tem certeza que deseja remover? (s/n): ").lower()

    if confirm == "s":
        df = df.drop(index=indice).reset_index(drop=True)
        salvar_dados(df)
        print("Aluno removido!\n")
    else:
        print("Remoção cancelada.\n")

    return df

# -------------------------------------------------------------------

def pesquisar(df):
    print("\n=== PESQUISAR ===")
    print("1 - Pesquisar por Matrícula")
    print("2 - Pesquisar por Nome")
    opc = input("Opção: ")

    if opc == "1":
        mat = input("Digite a matrícula: ")
        if mat.isdigit():
            mat = int(mat)
            resultado = df[df["Matricula"] == mat]
        else:
            print("Matrícula inválida.\n")
            return df

    elif opc == "2":
        nome = input("Digite o nome: ").lower()
        
        resultado = df[df["Nome"].str.lower().str.contains(nome, na=False)]
    else:
        print("Opção inválida.\n")
        return df

    if resultado.empty:
        print("Aluno não encontrado.\n")
        return df

    
    if len(resultado) > 1:
        print("Foram encontrados vários alunos:")
        for i, row in resultado.iterrows():
            print(f"{i} - {row['Nome']} (Matrícula {row['Matricula']})")

        escolha = input("Digite o índice desejado: ")

        if escolha.isdigit() and int(escolha) in resultado.index:
            indice = int(escolha)
        else:
            print("Índice inválido.\n")
            return df
    else:
        indice = resultado.index[0]

    aluno = df.loc[indice]
    mostrar_aluno(aluno)

    print("1 - Editar")
    print("2 - Remover")
    print("0 - Voltar")
    acao = input("Opção: ")

    if acao == "1":
        df = editar(df, indice)
    elif acao == "2":
        df = remover(df, indice)

    return df

# -------------------------------------------------------------------

def menu():
    df = carregar_dados()

    while True:
        print("=== MENU PRINCIPAL ===")
        print("1 - Inserir")
        print("2 - Pesquisar")
        print("3 - Sair")

        opc = input("Opção: ")

        if opc == "1":
            df = inserir(df)
        elif opc == "2":
            df = pesquisar(df)
        elif opc == "3":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida.\n")


menu()