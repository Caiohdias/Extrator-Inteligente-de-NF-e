import sqlite3
from ai_processor import processar_nota_com_ia

def salvar_no_banco(dados):
    """
    Recebe o objeto NotaFiscal (do Pydantic) e insere no SQLite.
    Agora acessamos os campos com ponto (.) em vez de .get()
    """
    print("💾 Conectando ao Banco de Dados...")
    conexao = sqlite3.connect("notas_fiscais.db")
    cursor = conexao.cursor()
    
    try:
        # 1. SALVAR A NOTA FISCAL
        cursor.execute("""
            INSERT INTO notas_fiscais (numero, emitente, cnpj, data_emissao, valor_total)
            VALUES (?, ?, ?, ?, ?)
        """, (
            dados.numero,
            dados.emitente,
            dados.cnpj,
            dados.data_emissao,
            dados.valor_total
        ))
        
        id_nota_inserida = cursor.lastrowid
        
        # 2. SALVAR OS ITENS
        for item in dados.itens:
            cursor.execute("""
                INSERT INTO itens_nota (id_nota, descricao, quantidade, valor_unitario, valor_total_item)
                VALUES (?, ?, ?, ?, ?)
            """, (
                id_nota_inserida,
                item.descricao,
                item.quantidade,
                item.valor_unitario,
                item.valor_total_item # NOVO CAMPO ADICIONADO AQUI
            ))
            
        conexao.commit()
        print("🎉 Nota e itens salvos com sucesso!")
        
    except Exception as e:
        conexao.rollback()
        print(f"❌ Erro ao salvar no banco de dados: {e}")
    finally:
        conexao.close()

if __name__ == "__main__":
    arquivo_alvo = "nota_exemplo.pdf"
    
    print("\n" + "="*50)
    print("🚀 INICIANDO O PIPELINE MULTIMODAL...")
    print("="*50)
    
    try:
        # Passo Único: Enviar o arquivo direto para a IA analisar visualmente
        dados_processados = processar_nota_com_ia(arquivo_alvo)
        
        # Salvar no banco
        salvar_no_banco(dados_processados)
        
        print("🏆 PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        
    except Exception as e:
        print(f"❌ Pipeline interrompido por erro: {e}")