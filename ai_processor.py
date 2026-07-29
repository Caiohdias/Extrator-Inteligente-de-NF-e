import os
import time
from pathlib import Path
from pydantic import BaseModel
from typing import List
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Carrega a chave do .env
load_dotenv()

# Definimos exatamente o formato que queremos receber
class ItemNota(BaseModel):
    descricao: str
    quantidade: float
    valor_unitario: float
    valor_total_item: float # NOVO CAMPO ADICIONADO AQUI

class NotaFiscal(BaseModel):
    numero: str
    emitente: str
    cnpj: str
    data_emissao: str
    valor_total: float
    itens: List[ItemNota]

def processar_nota_com_ia(caminho_arquivo):
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    # Prompt focado em análise visual
    prompt = """
    Você é um especialista em extração de dados de notas fiscais escaneadas (DANFE/NF-e).
    Analise a imagem deste PDF visualmente e extraia os dados solicitados.
    
    Regras:
    1. Ignore avisos como "documento sem valor fiscal" ou marca d'água.
    2. Identifique os itens da nota fiscal na tabela principal.
    3. Extraia o valor total de cada item multiplicando a quantidade pelo valor unitário, ou copiando o valor da coluna "Preço total" / "Valor Total" se existir.
    4. Converta valores monetários para números de Python (ex: 230,00 vira 230.0).
    5. Se não encontrar algo de forma nítida, retorne vazio ou 0.
    """

    # Lemos o arquivo PDF diretamente do seu computador em formato "bruto" (bytes)
    print(f"📄 Carregando arquivo PDF: '{caminho_arquivo}'...")
    pdf_bytes = Path(caminho_arquivo).read_bytes()
    
    # Empacotamos o PDF no formato que a API do Gemini exige
    documento_pdf = types.Part.from_bytes(data=pdf_bytes, mime_type='application/pdf')

    for tentativa in range(3):
        try:
            print(f"👁️ A IA está 'olhando' o PDF visualmente (Tentativa {tentativa + 1})...")
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                # Enviamos o texto (prompt) e o arquivo PDF (documento_pdf) juntos!
                contents=[prompt, documento_pdf],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=NotaFiscal,
                    temperature=0.0 # Zero criatividade, foco total na precisão
                ),
            )
            return response.parsed 
        
        except Exception as e:
            print(f"⚠️ Erro: {e}. Tentando novamente em 5s...")
            time.sleep(5)
            
    raise Exception("❌ Não foi possível processar a nota após 3 tentativas.")