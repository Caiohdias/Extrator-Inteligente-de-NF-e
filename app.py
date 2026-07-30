import sqlite3
import pandas as pd
import streamlit as st
from database import inicializar_banco
from ai_processor import processar_nota_com_ia

# ... importações ...
inicializar_banco()

st.set_page_config(
    page_title="Extrator Inteligente de NF-e",
    page_icon="📄",
    layout="wide"
)
st.markdown("""
    <style>
    .stMetric {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=2) 
def carregar_dados_banco():
    conexao = sqlite3.connect("notas_fiscais.db")
    
    df_notas = pd.read_sql_query("SELECT * FROM notas_fiscais", conexao)
    
    query_itens = """
        SELECT 
            n.emitente as Empresa,
            i.descricao as Produto,
            i.quantidade as Quantidade,
            i.valor_unitario as 'Valor Unitário (R$)',
            i.valor_total_item as 'Total do Item (R$)'
        FROM itens_nota i
        JOIN notas_fiscais n ON i.id_nota = n.id
    """
    df_itens = pd.read_sql_query(query_itens, conexao)
    
    conexao.close()
    return df_notas, df_itens

st.title("📄 Extrator Inteligente de Notas Fiscais (IA + SQL)")
st.write("Automatize a leitura de DANFE/NF-e usando inteligência artificial multimodal e organize tudo em um banco de dados relacional.")

aba_processar, aba_dashboard = st.tabs(["🚀 Processar Nova Nota", "📊 Painel de controle e histórico"])

# ==========================================
# ABA 1: PROCESSAR NOVA NOTA
# ==========================================
with aba_processar:
    st.subheader("Faça o upload do documento fiscal (PDF)")
    
    arquivo_upload = st.file_uploader("Escolha um arquivo PDF", type=["pdf"])
    
    if arquivo_upload is not None:
        st.success(f"Arquivo **{arquivo_upload.name}** carregado com sucesso!")
        
        if st.button("🧠 Processar Nota com IA", type="primary"):
            with st.spinner("A IA está analisando visualmente o documento e extraindo os dados... Aguarde."):
                try:
                    caminho_temp = "temp_nota.pdf"
                    with open(caminho_temp, "wb") as f:
                        f.write(arquivo_upload.getbuffer())
                    
                    # 1. Processa com a IA Multimodal
                    dados_processados = processar_nota_com_ia(caminho_temp)
                    
                    # 2. Salva no Banco de Dados SQLite
                    conexao = sqlite3.connect("notas_fiscais.db")
                    cursor = conexao.cursor()
                    
                    cursor.execute("""
                        INSERT INTO notas_fiscais (numero, emitente, cnpj, data_emissao, valor_total)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        dados_processados.numero,
                        dados_processados.emitente,
                        dados_processados.cnpj,
                        dados_processados.data_emissao,
                        dados_processados.valor_total
                    ))
                    id_nota = cursor.lastrowid
                    
                    for item in dados_processados.itens:
                        cursor.execute("""
                            INSERT INTO itens_nota (id_nota, descricao, quantidade, valor_unitario, valor_total_item)
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            id_nota,
                            item.descricao,
                            item.quantidade,
                            item.valor_unitario,
                            item.valor_total_item
                        ))
                        
                    conexao.commit()
                    conexao.close()
                    
                    st.balloons()
                    st.success("🎉 Nota fiscal processada e salva no banco de dados com sucesso! Vá para a aba 'Painel de controle e histórico' para visualizar.")
                    
                except Exception as e:
                    st.error(f"❌ Ocorreu um erro durante o processamento: {e}")

# ==========================================
# ABA 2: DASHBOARD e HISTÓRICO
# ==========================================
with aba_dashboard:
    df_notas, df_itens = carregar_dados_banco()
    
    if df_notas.empty:
        st.info("📭 O banco de dados ainda está vazio. Processe alguma nota fiscal na aba ao lado para visualizar os dados aqui.")
    else:
        # --- SEÇÃO 1: MÉTRICAS PRINCIPAIS (KPIs) ---
        st.markdown("### 📈 Indicadores Gerais")
        col1, col2, col3 = st.columns(3)
        
        total_gasto = df_notas["valor_total"].sum()
        qtd_notas = len(df_notas)
        qtd_empresas = df_notas["emitente"].nunique()
        
        col1.metric("💰 Valor Total Processado", f"R$ {total_gasto:,.2f}")
        col2.metric("📄 Total de Notas Lidas", qtd_notas)
        col3.metric("🏢 Empresas Emitentes", qtd_empresas)
        
        st.divider()
        
        # --- SEÇÃO 2: GRÁFICO DE GASTOS POR EMPRESA ---
        st.markdown("### 📊 Gastos por Empresa Emitente")
        if not df_notas.empty:
            df_grafico = df_notas.groupby("emitente")["valor_total"].sum().reset_index()
            df_grafico.columns = ["Empresa", "Valor Total (R$)"]
            df_grafico = df_grafico.set_index("Empresa")
            st.bar_chart(df_grafico)
            
        st.divider()

        # --- SEÇÃO 3: ITENS SEPARADOS POR EMPRESA ---
        st.markdown("### 🛒 Detalhamento dos Itens por Empresa")
        
        empresas_cadastradas = df_itens["Empresa"].unique()
        
        for empresa in empresas_cadastradas:
            with st.expander(f"🏢 Empresa: {empresa}", expanded=True):
                df_filtro_empresa = df_itens[df_itens["Empresa"] == empresa].drop(columns=["Empresa"])
                st.dataframe(df_filtro_empresa, use_container_width=True)
        
        st.divider()
        
        # --- SEÇÃO 4: HISTÓRICO BRUTO DE NOTAS ---
        st.markdown("### 📋 Histórico de Cabeçalhos de Notas Fiscais")
        st.dataframe(df_notas, use_container_width=True)
