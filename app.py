import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

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
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .big-font { font-size: 20px !important; }
    .question-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE CONHECIMENTO (PSICOLOGIA & RH) ---

# Perfis Baseados no Holland Codes (RIASEC) + DISC
# A = Analítico (Lógica, Dados, Processos)
# C = Comunicador (Pessoas, Persuasão, Empatia)
# I = Inovador (Criatividade, Visão, Mudança)
# E = Executor (Ação, Resultados, Praticidade)

questions = [
    {
        "type": "image",
        "title": "Teste Projetivo Visual 1",
        "text": "Observe esta imagem abstrata (Mancha de Rorschach simulada). O que captura sua atenção primeiro?",
        "image": "https://images.unsplash.com/photo-1565697592121-21cb05b19278?q=80&w=600&auto=format&fit=crop", # Imagem abstrata de tinta
        "options": [
            {"txt": "A simetria e a estrutura das formas.", "cat": "A"},
            {"txt": "Vejo rostos ou interações humanas na mancha.", "cat": "C"},
            {"txt": "Sinto uma emoção ou uma explosão de criatividade.", "cat": "I"},
            {"txt": "Vejo o movimento e a direção da tinta.", "cat": "E"}
        ]
    },
    {
        "type": "text",
        "title": "Gestão de Crise",
        "text": "Sua empresa perdeu um prazo crítico hoje. Qual sua reação instintiva imediata?",
        "image": None,
        "options": [
            {"txt": "Paro tudo para analisar onde o processo falhou para não repetir.", "cat": "A"},
            {"txt": "Converso com a equipe para manter o moral alto e alinhar expectativas.", "cat": "C"},
            {"txt": "Improviso uma solução alternativa rápida para entregar algo.", "cat": "I"},
            {"txt": "Foco 100% em terminar a tarefa, custe o que custar, depois converso.", "cat": "E"}
        ]
    },
    {
        "type": "image",
        "title": "Percepção de Ambiente",
        "text": "Olhe para esta imagem de arquitetura. O que mais te agrada nela?",
        "image": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=600&auto=format&fit=crop", # Prédio moderno geométrico
        "options": [
            {"txt": "A precisão matemática das linhas e ângulos.", "cat": "A"},
            {"txt": "Imagino as pessoas vivendo e trabalhando lá dentro.", "cat": "C"},
            {"txt": "O design futurista e a visão do arquiteto.", "cat": "I"},
            {"txt": "A solidez da construção e a funcionalidade.", "cat": "E"}
        ]
    },
    {
        "type": "text",
        "title": "Dinâmica de Trabalho",
        "text": "Você foi encarregado de liderar um novo projeto. Qual é seu primeiro passo?",
        "image": None,
        "options": [
            {"txt": "Crio um cronograma detalhado e defino KPIs.", "cat": "A"},
            {"txt": "Faço uma reunião de brainstorming para ouvir a todos.", "cat": "C"},
            {"txt": "Visualizo o resultado final e crio um conceito inovador.", "cat": "I"},
            {"txt": "Defino as metas de curto prazo e começo a executar já.", "cat": "E"}
        ]
    },
    {
        "type": "image",
        "title": "Associação Livre",
        "text": "Esta imagem remete a conexões. Como você prefere se conectar ao mundo?",
        "image": "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=600&auto=format&fit=crop", # Gradiente de cores abstrato
        "options": [
            {"txt": "Através da compreensão lógica de como as coisas funcionam.", "cat": "A"},
            {"txt": "Através de conversas profundas e networking.", "cat": "C"},
            {"txt": "Através da arte, música ou ideias novas.", "cat": "I"},
            {"txt": "Através de realizações tangíveis e trabalho prático.", "cat": "E"}
        ]
    },
    {
        "type": "text",
        "title": "Motivação Profunda",
        "text": "O que faz você sentir que teve um dia de trabalho produtivo?",
        "image": None,
        "options": [
            {"txt": "Quando resolvi um problema complexo ou organizei algo caótico.", "cat": "A"},
            {"txt": "Quando ajudei alguém ou convenci um cliente importante.", "cat": "C"},
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

# --- FUNÇÕES ---

def reset_test():
    st.session_state.current_q = 0
    st.session_state.scores = {'A': 0, 'C': 0, 'I': 0, 'E': 0}
    st.session_state.finished = False
    st.rerun()

def process_answer(category):
    st.session_state.scores[category] += 1
    if st.session_state.current_q < len(questions) - 1:
        st.session_state.current_q += 1
    else:
        st.session_state.finished = True
    st.rerun()

# --- TELA PRINCIPAL ---

if not st.session_state.finished:
    # HEADER
    st.title("🧠 NeuroCareer: Mapeamento Profissional")
    st.markdown("Responda com honestidade. Algumas questões usam **psicologia projetiva** (imagens), não há resposta certa ou errada.")
    
    # BARRA DE PROGRESSO
    progress = (st.session_state.current_q) / len(questions)
    st.progress(progress)

    # EXIBIÇÃO DA PERGUNTA
    q = questions[st.session_state.current_q]
    
    with st.container():
        st.markdown(f"<div class='question-card'><h3>Questão {st.session_state.current_q + 1}: {q['title']}</h3><p class='big-font'>{q['text']}</p></div>", unsafe_allow_html=True)
        
        if q['type'] == 'image' and q['image']:
            st.image(q['image'], use_container_width=True)
            st.caption("Observe a imagem e selecione a opção que melhor descreve sua percepção.")

        # OPÇÕES (4 Respostas)
        col1, col2 = st.columns(2)
        with col1:
            if st.button(q['options'][0]['txt']): process_answer(q['options'][0]['cat'])
            if st.button(q['options'][1]['txt']): process_answer(q['options'][1]['cat'])
        with col2:
            if st.button(q['options'][2]['txt']): process_answer(q['options'][2]['cat'])
            if st.button(q['options'][3]['txt']): process_answer(q['options'][3]['cat'])

else:
    # --- TELA DE RESULTADOS ---
    st.balloons()
    st.title("📊 Seu Mapeamento Profissional")
    
    # Calcular Perfil Dominante
    scores = st.session_state.scores
    total = sum(scores.values())
    dominant_code = max(scores, key=scores.get)
    
    profiles = {
        'A': {'name': 'O ANALISTA ESTRATEGISTA', 'desc': 'Você é movido por lógica, dados e eficiência.', 'color': '#3498db'},
        'C': {'name': 'O DIPLOMATA COMUNICADOR', 'desc': 'Você é movido por conexões humanas e influência.', 'color': '#e91e63'},
        'I': {'name': 'O VISIONÁRIO INOVADOR', 'desc': 'Você é movido por ideias, criação e futuro.', 'color': '#9b59b6'},
        'E': {'name': 'O EXECUTOR PRAGMÁTICO', 'desc': 'Você é movido por ação, resultados e velocidade.', 'color': '#e67e22'}
    }
    
    dominant = profiles[dominant_code]
    
    # Exibir Perfil Principal
    st.markdown(f"""
        <div style="padding: 20px; background-color: {dominant['color']}; color: white; border-radius: 10px; text-align: center;">
            <h2>Seu Arquétipo: {dominant['name']}</h2>
            <p class='big-font'>{dominant['desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    # --- GRÁFICO DE RADAR (SPIDER CHART) ---
    st.subheader("Raio-X das Competências")
    
    categories = ['Analítico', 'Comunicador', 'Inovador', 'Executor']
    values = [scores['A'], scores['C'], scores['I'], scores['E']]
    
    fig = go.Figure(data=go.Scatterpolar(
      r=values,
      theta=categories,
      fill='toself',
      line_color=dominant['color']
    ))
    fig.update_layout(
      polar=dict(radialaxis=dict(visible=True, range=[0, max(values)+1])),
      showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- ANÁLISE SWOT & CARREIRA ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Plano de Carreira Sugerido")
        if dominant_code == 'A':
            st.success("**Áreas Ideais:** Ciência de Dados, Engenharia, Finanças, TI, Direito Tributário.")
            st.info("**Foco de Desenvolvimento:** Tente não perder tempo demais buscando a perfeição.")
        elif dominant_code == 'C':
            st.success("**Áreas Ideais:** RH, Vendas, Marketing, Psicologia, Gestão de Comunidades.")
            st.info("**Foco de Desenvolvimento:** Aprenda a dizer 'não' e focar em métricas frias quando necessário.")
        elif dominant_code == 'I':
            st.success("**Áreas Ideais:** Design, Arquitetura, Empreendedorismo, P&D, Publicidade.")
            st.info("**Foco de Desenvolvimento:** Melhore sua capacidade de finalizar o que começa (acabativa).")
        elif dominant_code == 'E':
            st.success("**Áreas Ideais:** Gestão de Projetos, Logística, Operações, Cirurgia, Esportes.")
            st.info("**Foco de Desenvolvimento:** Trabalhe a paciência e a escuta ativa com a equipe.")

    with col2:
        st.subheader("🛡️ Análise SWOT Pessoal")
        st.markdown("Baseado nas suas escolhas situacionais:")
        
        # Lógica Dinâmica SWOT
        strengths = []
        weaknesses = []
        
        if scores['A'] >= 2: strengths.append("Pensamento Crítico"); strengths.append("Organização")
        else: weaknesses.append("Atenção aos detalhes")
        
        if scores['C'] >= 2: strengths.append("Empatia"); strengths.append("Persuasão")
        else: weaknesses.append("Comunicação Interpessoal")
        
        if scores['I'] >= 2: strengths.append("Criatividade"); strengths.append("Adaptabilidade")
        else: weaknesses.append("Resistência à mudança")
        
        if scores['E'] >= 2: strengths.append("Foco em Resultado"); strengths.append("Agilidade")
        else: weaknesses.append("Procrastinação")
        
        st.write(f"**Forças (Interno):** {', '.join(strengths)}")
        st.write(f"**Fraquezas (Interno):** {', '.join(weaknesses)}")
        st.write(f"**Oportunidades (Externo):** Mercado busca profissionais {dominant['name'].split()[-1].lower()}s para liderança.")
        st.write(f"**Ameaças (Externo):** Ambientes burocráticos podem desmotivar seu perfil.")

    if st.button("Refazer Teste"):
        reset_test()