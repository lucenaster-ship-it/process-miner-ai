import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# Título e descrição
st.title("🧩 Process Miner AI")
st.write("""
**Gere documentação, POPs e protótipos de processos automaticamente com IA.**  
Envie capturas de telas e descreva cada etapa — o app monta conexões, regras de negócio e um fluxo sistêmico.
""")

# Configuração da API Key (usando secrets no Streamlit Cloud)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.warning("⚠️ Configure sua chave GEMINI_API_KEY nos secrets do Streamlit Cloud.")
    st.stop()

# Upload das imagens das telas
uploaded_files = st.file_uploader(
    "📸 Envie as imagens das telas do sistema",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

# Campo para descrição textual
descricao = st.text_area("🧾 Descreva as telas e o processo", placeholder="Explique cada tela, regras de negócio, e a sequência lógica...")

# Botão para gerar a análise
if st.button("🚀 Gerar documentação e protótipo"):
    if not uploaded_files and not descricao:
        st.warning("Envie pelo menos uma imagem ou descrição.")
        st.stop()

    st.info("Gerando documentação com IA... Aguarde alguns instantes...")

    # Prepara conteúdo
    imagens_base64 = []
    for file in uploaded_files:
        image = Image.open(file)
        imagens_base64.append(file.name)

    prompt = f"""
    Você é um analista de processos. 
    Com base nas telas enviadas e nas descrições a seguir, gere:
    1. Um resumo do processo;
    2. Regras de negócio identificadas;
    3. Fluxo sistêmico entre as telas;
    4. Sugestão de POP (Procedimento Operacional Padrão);
    5. Sugestão de protótipo funcional.
    
    Descrição:
    {descricao}
    Imagens: {', '.join(imagens_base64)}
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    resposta = model.generate_content(prompt)

    st.subheader("📘 Documentação Gerada")
    st.write(resposta.text)
