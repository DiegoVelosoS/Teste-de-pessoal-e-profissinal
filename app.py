import streamlit as st
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="NeuroCareer - Análise de Perfil",
    page_icon="🧠",
    layout="centered"
)

# --- ESTILOS CSS PERSONALIZADOS (CORRIGIDO) ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50; /* Verde padrão */
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    
    /* Correção do Cartão da Pergunta */
    .question-card {
        background-color: #f0f2f6;
        padding: 25px;
        border-radius: 10px;
        border-left: 6px solid #4CAF50;
        margin-bottom: 25px;
        color: #1e1e1e !important; /* Força texto escuro para leitura */
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
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DADOS DAS PERGUNTAS ---

questions = [
    {
        "type": "image",
        "title": "Teste Projetivo Visual 1",
        "text": "Observe esta mancha de tinta (Rorschach). O que seus olhos focam primeiro?",
        # Link estável da Wikimedia (Rorschach real)
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
        # Link estável de Arquitetura
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
        # Link estável de Rede Neural/Abstrato
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
        # Renderiza o cartão da pergunta com HTML seguro para aplicar o CSS
        st.markdown(f"""
            <div class='question-card'>
                <h3>Questão {st.session_state.current_q + 1}: {q['title']}</h3>
                <p>{q['text']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if q['type'] == 'image' and q['image']:
            # Tenta carregar a imagem, se falhar não quebra o app
            try:
                st.image(q['image'], use_container_width=True)
                st.caption("Observe a imagem e selecione a opção que melhor descreve sua percepção.")
            except:
                st.error("Erro ao carregar imagem. Prossiga pelo texto.")

        # OPÇÕES (Botões grandes)
        st.write("") # Espaçamento
        col1, col2 = st.columns(2)
        with col1:
            if st.button(q['options'][0]['txt'], key="opt1"): process_answer(q['options'][0]['cat'])
            st.write("") # Espaçamento vertical entre botões mobile
            if st.button(q['options'][1]['txt'], key="opt2"): process_answer(q['options'][1]['cat'])
        with col2:
            if st.button(q['options'][2]['txt'], key="opt3"): process_answer(q['options'][2]['cat'])
            st.write("")
            if st.button(q['options'][3]['txt'], key="opt4"): process_answer(q['options'][3]['cat'])

else:
    # --- TELA DE RESULTADOS ---
    st.balloons()
    st.title("📊 Seu Mapeamento Profissional")
    
    # Calcular Perfil Dominante
    scores = st.session_state.scores
    dominant_code = max(scores, key=scores.get)
    
    profiles = {
        'A': {'name': 'O ANALISTA ESTRATEGISTA', 'desc': 'Você é movido por lógica, dados e eficiência.', 'color': '#3498db'}, # Azul
        'C': {'name': 'O DIPLOMATA COMUNICADOR', 'desc': 'Você é movido por conexões humanas e influência.', 'color': '#e91e63'}, # Rosa
        'I': {'name': 'O VISIONÁRIO INOVADOR', 'desc': 'Você é movido por ideias, criação e futuro.', 'color': '#9b59b6'}, # Roxo
        'E': {'name': 'O EXECUTOR PRAGMÁTICO', 'desc': 'Você é movido por ação, resultados e velocidade.', 'color': '#e67e22'} # Laranja
    }
    
    dominant = profiles[dominant_code]
    
    # Exibir Perfil Principal com CSS inline para garantir visual
    st.markdown(f"""
        <div style="padding: 20px; background-color: {dominant['color']}; color: white; border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <h2 style="color: white; margin:0;">Seu Arquétipo: {dominant['name']}</h2>
            <p style="font-size: 18px; margin-top: 10px;">{dominant['desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    # --- GRÁFICO DE RADAR (SPIDER CHART) ---
    st.subheader("Raio-X das Competências")
    
    categories = ['Analítico (Lógica)', 'Comunicador (Pessoas)', 'Inovador (Ideias)', 'Executor (Ação)']
    values = [scores['A'], scores['C'], scores['I'], scores['E']]
    
    # Fecha o gráfico repetindo o primeiro valor
    values_plot = values + [values[0]]
    categories_plot = categories + [categories[0]]

    fig = go.Figure(data=go.Scatterpolar(
      r=values_plot,
      theta=categories_plot,
      fill='toself',
      line_color=dominant['color'],
      name='Seu Perfil'
    ))
    
    fig.update_layout(
      polar=dict(
        radialaxis=dict(visible=True, range=[0, max(values)+1])
      ),
      showlegend=False,
      margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- ANÁLISE SWOT & CARREIRA ---
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Plano de Carreira")
        if dominant_code == 'A':
            st.success("**Áreas Ideais:** Ciência de Dados, Engenharia, Finanças, Direito, TI.")
            st.info("**Foco de Desenvolvimento:** Evite a 'paralisia por análise'. O feito é melhor que o perfeito.")
        elif dominant_code == 'C':
            st.success("**Áreas Ideais:** RH, Vendas, Marketing, Psicologia, Ensino, Relações Públicas.")
            st.info("**Foco de Desenvolvimento:** Aprenda a focar em métricas objetivas e dizer 'não' para manter o foco.")
        elif dominant_code == 'I':
            st.success("**Áreas Ideais:** Design, Arquitetura, Empreendedorismo, P&D, Artes, Publicidade.")
            st.info("**Foco de Desenvolvimento:** Melhore sua 'acabativa'. Ideias sem execução não geram valor.")
        elif dominant_code == 'E':
            st.success("**Áreas Ideais:** Gestão de Projetos, Logística, Operações, Esportes, Cirurgia.")
            st.info("**Foco de Desenvolvimento:** Desenvolva a escuta ativa e a paciência com ritmos diferentes do seu.")

    with col2:
        st.subheader("🛡️ Análise SWOT Pessoal")
        
        # Lógica Dinâmica SWOT
        strengths = []
        weaknesses = []
        
        if scores['A'] >= 2: strengths.append("Pensamento Crítico"); strengths.append("Organização")
        else: weaknesses.append("Atenção aos detalhes")
        
        if scores['C'] >= 2: strengths.append("Empatia"); strengths.append("Persuasão")
        else: weaknesses.append("Comunicação difícil")
        
        if scores['I'] >= 2: strengths.append("Criatividade"); strengths.append("Flexibilidade")
        else: weaknesses.append("Resistência ao novo")
        
        if scores['E'] >= 2: strengths.append("Foco em Resultado"); strengths.append("Agilidade")
        else: weaknesses.append("Procrastinação")
        
        st.markdown(f"""
        **Forças (Interno):**
        :white_check_mark: {', '.join(strengths)}
        
        **Fraquezas (Interno):**
        :warning: {', '.join(weaknesses)}
        
        **Oportunidades (Externo):**
        :bulb: Mercado valoriza perfis **{dominant['name'].split()[-1].lower()}s** para liderança adaptativa.
        
        **Ameaças (Externo):**
        :rotating_light: Ambientes rígidos ou burocráticos podem desmotivar seu perfil.
        """)

    st.markdown("---")
    if st.button("🔄 Refazer Teste Completo"):
        reset_test()
