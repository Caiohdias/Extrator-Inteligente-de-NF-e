import sqlite3

def visualizar_dados():
    """
    Conecta ao banco SQLite e exibe todas as notas e seus itens de forma clara.
    """
    print("\n🔍 BUSCANDO DADOS NO BANCO DE DADOS...\n")
    conexao = sqlite3.connect("notas_fiscais.db")
    cursor = conexao.cursor()
    
    try:
        # 1. Busca todas as notas fiscais
        cursor.execute("SELECT * FROM notas_fiscais")
        notas = cursor.fetchall()
        
        if not notas:
            print("📭 O banco de dados está vazio.")
            return

        for nota in notas:
            id_nota, numero, emitente, cnpj, data, valor = nota
            print(f"📄 NOTA FISCAL ID: {id_nota} | Nº: {numero}")
            print(f"🏢 Emitente: {emitente} (CNPJ: {cnpj})")
            print(f"📅 Data: {data} | 💰 Valor Total: R$ {valor:.2f}")
            print("-" * 50)
            
            # 2. Busca os itens relacionados a esta nota
            cursor.execute("SELECT descricao, quantidade, valor_unitario, valor_total_item FROM itens_nota WHERE id_nota = ?", (id_nota,))
            itens = cursor.fetchall()
            
            print("🛒 Itens da Nota:")
            for item in itens:
                desc, qtd, vlr_unit, vlr_total = item
                # Exibe o valor unitário e o valor total do item
                print(f"   • {desc} | Qtd: {qtd} | Unitário: R$ {vlr_unit:.2f} | Total Item: R$ {vlr_total:.2f}")
            print("\n" + "="*60 + "\n")
            
    except Exception as e:
        print(f"❌ Erro ao consultar o banco: {e}")
    finally:
        conexao.close()

if __name__ == "__main__":
    visualizar_dados()