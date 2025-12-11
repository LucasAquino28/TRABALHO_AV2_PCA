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