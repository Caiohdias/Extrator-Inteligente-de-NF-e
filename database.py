import sqlite3

def inicializar_banco():
    conexao = sqlite3.connect("notas_fiscais.db")
    cursor = conexao.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    #Tabela 1: Guarda os dados do cabeçalho da Nota Fiscal
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas_fiscais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL,
            emitente TEXT NOT NULL,
            cnpj TEXT NOT NULL,
            data_emissao TEXT,
            valor_total REAL
        );
    """)

    #Tabela 2: Guarda os produtos e faz um vínculo (id_nota) com a tabela notas_fiscais
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_nota (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_nota INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            quantidade REAL NOT NULL,
            valor_unitario REAL NOT NULL,
            valor_total_item REAL NOT NULL, -- NOVO CAMPO ADICIONADO AQUI
            FOREIGN KEY (id_nota) REFERENCES notas_fiscais (id) ON DELETE CASCADE
        );
    """)

    conexao.commit()
    conexao.close()
    print("✅ Banco de dados 'notas_fiscais.db' e tabelas criados com sucesso!")

if __name__ == "__main__":
    inicializar_banco()
