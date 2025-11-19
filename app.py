import streamlit as st
import plotly.graph_objects as go
import time # Importar a biblioteca de tempo

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="NeuroCareer - Análise de Perfil",
    page_icon="🧠",
    layout="centered"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px; /* Mais arredondado */
        height: 3.5em; /* Um pouco maior */
        background-color: #4CAF50; /* Verde padrão */
        color: white;
        border: none;
        font-size: 16px;
        font-weight: bold;
        transition: background-color 0.2s;
        margin-bottom: 8px; /* Espaçamento entre botões */
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    
    .question-card {
        background-color: #f0f2f6;
        padding: 25px;
        border-radius: 10px;
        border-left: 6px solid #4CAF50;
        margin-bottom: 25px;
        color: #1e1e1e !important;
    }
    
    .question-card h3 {
        color: #2c3e50 !important;
        margin-top: 0;
    }
    
    .question-card p {
        font-size: 18px !important;
        line-height: 1.6;
        font-weight: 500;
    }

    /* Estilo para o timer e contador de etapas */
    .footer-info {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #333;
        color: white;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 18px;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.2);
        z-index: 1000;
    }
    .timer {
        color: #FFD700; /* Amarelo para o tempo */
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DADOS DAS PERGUNTAS ---

questions = [
    {
        "type": "image",
        "title": "Teste Projetivo Visual 1",
        "text": "Observe esta mancha de tinta (Rorschach). O que seus olhos focam primeiro?",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Rorschach_blot_01.jpg/600px-Rorschach_blot_01.jpg", 
        "options": [
            {"txt": "A simetria técnica e a forma de 'morcego' ou insígnia.", "cat": "A"},
            {"txt": "Vejo dois anjos ou pessoas dançando ao centro.", "cat": "C"},
            {"txt": "Vejo uma máscara misteriosa ou algo fantasioso.", "cat": "I"},
            {"txt": "Vejo apenas uma mancha de tinta preta, sem significado.", "cat": "E"}
        ]
    },
    {
        "type": "text",
        "title": "Gestão de Crise",
        "text": "Sua empresa perdeu um prazo crítico hoje. Qual sua reação instintiva imediata?",
        "image": None,
        "options": [
            {"txt": "Paro tudo para analisar onde o processo falhou (causa-raiz).", "cat": "A"},
            {"txt": "Converso com a equipe para manter o moral alto e acalmar os ânimos.", "cat": "C"},
            {"txt": "Improviso uma solução criativa rápida para entregar algo funcional.", "cat": "I"},
            {"txt": "Foco 100% em terminar a tarefa agora, custe o que custar.", "cat": "E"}
        ]
    },
    {
        "type": "image",
        "title": "Percepção de Ambiente",
        "text": "Olhe para esta arquitetura moderna. O que mais te agrada nela?",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Valencia_City_of_Arts_and_Sciences.jpg/600px-Valencia_City_of_Arts_and_Sciences.jpg",
        "options": [
            {"txt": "A engenharia estrutural e a repetição dos padrões.", "cat": "A"},
            {"txt": "Imagino como as pessoas se sentem passeando por ali.", "cat": "C"},
            {"txt": "O design futurista que quebra regras tradicionais.", "cat": "I"},
            {"txt": "A funcionalidade do espaço e o tamanho da obra.", "cat": "E"}
        ]
    },
    {
        "type": "text",
        "title": "Liderança de Projetos",
        "text": "Você assumiu um novo projeto. Qual é seu primeiro passo?",
        "image": None,
        "options": [
            {"txt": "Crio um cronograma detalhado, planilha de custos e KPIs.", "cat": "A"},
            {"txt": "Faço uma reunião de brainstorming para ouvir todas as ideias.", "cat": "C"},
            {"txt": "Visualizo o resultado final inovador e crio o conceito.", "cat": "I"},
            {"txt": "Defino as metas imediatas e começo a executar já.", "cat": "E"}
        ]
    },
    {
        "type": "image",
        "title": "Associação Abstrata",
        "text": "Esta imagem representa conexões. Como você prefere se conectar ao mundo?",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Neural_network.png/600px-Neural_network.png",
        "options": [
            {"txt": "Através da lógica: entendendo como os sistemas funcionam.", "cat": "A"},
            {"txt": "Através da emoção: conversas profundas e networking.", "cat": "C"},
            {"txt": "Através da arte: música, visual ou novas ideias.", "cat": "I"},
            {"txt": "Através da ação: realizando coisas tangíveis e úteis.", "cat": "E"}
        ]
    },
    {
        "type": "text",
        "title": "Motivação Profunda",
        "text": "O que faz você sentir que teve um dia de trabalho produtivo?",
        "image": None,
        "options": [
            {"txt": "Quando resolvi um problema complexo ou organizei o caos.", "cat": "A"},
            {"txt": "Quando ajudei alguém, ensinei ou fechei uma parceria.", "cat": "C"},
            {"txt": "Quando tive uma ideia brilhante ou criei algo do zero.", "cat": "I"},
            {"txt": "Quando risquei todos os itens da minha lista de tarefas.", "cat": "E"}
        ]
    }
]

# --- LÓGICA DE ESTADO ---
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.scores = {'A': 0, 'C': 0, 'I': 0, 'E': 0}
    st.session_state.finished = False
    st.session_state.start_time = None # Tempo de início do teste
    st.session_state.time_taken = 0 # Tempo final

# --- FUNÇÕES ---

def reset_test():
    st.session_state.current_q = 0
    st.session_state.scores = {'A': 0, 'C': 0, 'I': 0, 'E': 0}
    st.session_state.finished = False
    st.session_state.start_time = None
    st.session_state.time_taken = 0
    st.rerun()

def process_answer(category):
    st.session_state.scores[category] += 1
    if st.session_state.current_q < len(questions) - 1:
        st.session_state.current_q += 1
    else:
        st.session_state.finished = True
        st.session_state.time_taken = time.time() - st.session_state.start_time
    st.rerun()

def calculate_speed_score(time_taken, total_questions):
    # A pontuação de velocidade é inversamente proporcional ao tempo.
    # Quanto menos tempo, maior a pontuação.
    # Max time = 180s (3 min)
    # Min time = ~10s (
