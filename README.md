# 📄 Extrator Inteligente de NF-e (AI Invoice Extractor)

Este projeto é um pipeline de engenharia de dados em Python que automatiza a extração de informações de Notas Fiscais (DANFE/NF-e). Utilizando **IA Multimodal**, o sistema "lê" visualmente os documentos, estrutura os dados em formato JSON e os persiste em um banco de dados relacional **SQL (SQLite)**.

## 🎯 O Problema
A entrada manual de dados fiscais é um processo lento, caro e sujeito a erros. Ferramentas tradicionais de OCR muitas vezes falham ao interpretar tabelas complexas ou documentos com ruídos visuais. 

## 🚀 A Solução
O sistema utiliza o modelo **Gemini 3.5 Flash** para análise visual, permitindo que a IA identifique itens, valores e datas em documentos digitalizados, ignorando elementos visuais sem valor fiscal e garantindo uma extração de dados estruturada e tipada via **Pydantic**.

## ⚙️ Arquitetura do Projeto
1. **Ingestão:** O script carrega o arquivo PDF em formato binário.
2. **Processamento (IA Multimodal):** Envio da imagem à API do Gemini para conversão de dados não estruturados (PDF) em objetos JSON estruturados.
3. **Persistência Relacional:** Inserção relacional (1:N) no banco de dados local `SQLite3`, garantindo integridade referencial entre cabeçalhos de notas e seus respectivos itens.
4. **Interface:** Visualização intuitiva dos dados processados, métricas e histórico através de um dashboard em **Streamlit**.

## ✨ Destaques Técnicos
*   **IA Multimodal:** Processamento visual que supera limitações do OCR tradicional.
*   **Dados Tipados:** Uso de esquemas rigorosos (Pydantic) para garantir a qualidade dos dados extraídos.
*   **Resiliência:** Lógica de *Retry* automática em caso de falhas na rede ou limites de API.
*   **Persistência Relacional:** Modelagem SQL que permite consultas complexas e análise de dados históricos.

## 🛠️ Tecnologias Utilizadas
*   **Linguagem:** Python
*   **Interface Web:** Streamlit
*   **Banco de Dados:** SQLite3
*   **Processamento de Dados:** Pandas
*   **IA:** Google Gemini (Generative AI SDK)
*   **Estruturação:** Pydantic

## 📦 Como rodar o projeto

1. **Clone o repositório:**
   
```bash
   git clone [https://github.com/Caiohdias/Extrator-Inteligente-de-NF-e.git](https://github.com/Caiohdias/Extrator-Inteligente-de-NF-e.git)
   cd Extrator-Inteligente-de-NF-e