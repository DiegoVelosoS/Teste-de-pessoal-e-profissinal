import streamlit as st
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
        border-radius: 8px;
        height: auto;
        min-height: 3.5em;
        background-color: #4CAF50;
        color: white;
        border: none;
        font-size: 16px;
        font-weight: bold;
        transition: background-color 0.2s;
        margin-bottom: 8px;
        white-space: normal;
        padding: 10px;
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
        color: #FFD700;
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
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Sydney_Opera_House_Sails.jpg/640px-Sydney_Opera_House_Sails.jpg",
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
    st.session_state.start_time = None
    st.session_state.time_taken = 0

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
        if st.session_state.start_time:
            st.session_state.time_taken = time.time() - st.session_state.start_time
        else:
            st.session_state.time_taken = 0
    st.rerun()

def calculate_speed_score(time_taken, total_questions):
    # A pontuação de velocidade é inversamente proporcional ao tempo.
    # Max time = 180s (3 min)
    max_score = 3
    
    # Garante que o tempo_gasto não seja zero
    time_taken = max(time_taken, 1) 
    
    # Se o tempo passou do limite (180s), zera o bonus
    if time_taken >= 180:
        return 0
    
    speed_score = (180 - time_taken) / 180 * max_score
    return round(speed_score, 1)

# --- TELA PRINCIPAL ---

if not st.session_state.finished:
    # HEADER
    st.title("🧠 NeuroCareer: Mapeamento Profissional")
    st.markdown("Responda com honestidade. Algumas questões usam **psicologia projetiva** (imagens), não há resposta certa ou errada.")
    
    # Inicia o timer APENAS se o usuário clicar no botão
    if st.session_state.start_time is None:
        if st.button("⏱️ INICIAR ANÁLISE (3 MINUTOS)", use_container_width=True):
            st.session_state.start_time = time.time()
            st.rerun()
        else:
            st.info("Você terá 3 minutos para concluir o teste. O tempo influenciará seu perfil.")
            st.stop()

    if st.session_state.start_time is not None:
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = max(0, 180 - int(elapsed_time))

        # Se o tempo acabar
        if remaining_time == 0:
            st.error("⌛ TEMPO ESGOTADO!")
            st.session_state.time_taken = 180
            st.session_state.finished = True
            time.sleep(2)
            st.rerun()

        # BARRA DE PROGRESSO
        progress = (st.session_state.current_q) / len(questions)
        st.progress(progress)

        # EXIBIÇÃO DA PERGUNTA
        q = questions[st.session_state.current_q]
        
        with st.container():
            st.markdown(f"""
                <div class='question-card'>
                    <h3>Questão {st.session_state.current_q + 1}: {q['title']}</h3>
                    <p>{q['text']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if q['type'] == 'image' and q['image']:
                try:
                    st.image(q['image'], use_container_width=True)
                    st.caption("Selecione a opção que melhor descreve sua percepção.")
                except Exception:
                    st.warning("Imagem indisponível no momento. Prossiga pelo texto.")

            # OPÇÕES
            # O segredo está aqui: chaves (keys) dinâmicas!
            idx = st.session_state.current_q
            
            st.write("")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(q['options'][0]['txt'], key=f"q{idx}_opt1"): process_answer(q['options'][0]['cat'])
                if st.button(q['options'][1]['txt'], key=f"q{idx}_opt2"): process_answer(q['options'][1]['cat'])
            with col2:
                if st.button(q['options'][2]['txt'], key=f"q{idx}_opt3"): process_answer(q['options'][2]['cat'])
                if st.button(q['options'][3]['txt'], key=f"q{idx}_opt4"): process_answer(q['options'][3]['cat'])
        
        # FOOTER
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        st.markdown(f"""
            <div class="footer-info">
                <span>Etapa: {st.session_state.current_q + 1} de {len(questions)}</span>
                <span class="timer">⏳ {minutes:02d}:{seconds:02d}</span>
            </div>
        """, unsafe_allow_html=True)
        
        time.sleep(1)
        st.rerun()

else: # TELA FINAL
    st.balloons()
    st.title("📊 Seu Mapeamento Profissional")

    speed_score = calculate_speed_score(st.session_state.time_taken, len(questions))
    
    final_scores = st.session_state.scores.copy()
    
    # Ajuste de pontuação baseado na velocidade
    if speed_score >= 2:
        final_scores['E'] += speed_score / 2
        final_scores['A'] += speed_score / 2
    else:
        final_scores['E'] += speed_score / 2
    
    dominant_code = max(final_scores, key=final_scores.get)
    
    profiles = {
        'A': {'name': 'O ANALISTA ESTRATEGISTA', 'desc': 'Você é movido por lógica, dados e eficiência. Prefere planejar e entender profundamente antes de agir.', 'color': '#3498db'},
        'C': {'name': 'O DIPLOMATA COMUNICADOR', 'desc': 'Você é movido por conexões humanas, influência e harmonia. Excelente em construir pontes.', 'color': '#e91e63'},
        'I': {'name': 'O VISIONÁRIO INOVADOR', 'desc': 'Você é movido por ideias, criação e o futuro. Gosta de experimentar e pensar fora da caixa.', 'color': '#9b59b6'},
        'E': {'name': 'O EXECUTOR PRAGMÁTICO', 'desc': 'Você é movido por ação, resultados e velocidade. Focado em fazer acontecer e entregar.', 'color': '#e67e22'}
    }
    
    dominant = profiles[dominant_code]
    
    st.markdown(f"""
        <div style="padding: 20px; background-color: {dominant['color']}; color: white; border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <h2 style="color: white; margin:0;">Seu Arquétipo: {dominant['name']}</h2>
            <p style="font-size: 18px; margin-top: 10px;">{dominant['desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("Raio-X das Competências")
    
    categories_for_chart = ['Analítico', 'Comunicador', 'Inovador', 'Executor', 'Velocidade']
    values_for_chart = [final_scores['A'], final_scores['C'], final_scores['I'], final_scores['E'], speed_score]
    
    values_plot = values_for_chart + [values_for_chart[0]]
    categories_plot = categories_for_chart + [categories_for_chart[0]]

    fig = go.Figure(data=go.Scatterpolar(
      r=values_plot,
      theta=categories_plot,
      fill='toself',
      line_color=dominant['color'],
      name='Seu Perfil'
    ))
    
    fig.update_layout(
      polar=dict(
        radialaxis=dict(visible=True, range=[0, max(values_for_chart)+1])
      ),
      showlegend=False,
      margin=dict(t=20, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info(f"Tempo total: {int(st.session_state.time_taken)} segundos.")

    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Plano de Carreira")
        if dominant_code == 'A':
            st.success("**Áreas Ideais:** Ciência de Dados, Engenharia, Finanças, Direito, TI.")
            st.info("**Foco de Desenvolvimento:** Evite a 'paralisia por análise'. O feito é melhor que o perfeito.")
        elif dominant_code == 'C':
            st.success("**Áreas Ideais:** RH, Vendas, Marketing, Psicologia, Ensino.")
            st.info("**Foco de Desenvolvimento:** Aprenda a focar em métricas objetivas e dizer 'não'.")
        elif dominant_code == 'I':
            st.success("**Áreas Ideais:** Design, Arquitetura, Empreendedorismo, P&D, Publicidade.")
            st.info("**Foco de Desenvolvimento:** Melhore sua 'acabativa'. Ideias precisam de execução.")
        elif dominant_code == 'E':
            st.success("**Áreas Ideais:** Gestão de Projetos, Logística, Operações, Cirurgia.")
            st.info("**Foco de Desenvolvimento:** Desenvolva paciência e escuta ativa.")

    with col2:
        st.subheader("🛡️ Análise SWOT")
        
        strengths = []
        weaknesses = []
        
        if final_scores['A'] >= 2: strengths.append("Pensamento Crítico"); strengths.append("Organização")
        else: weaknesses.append("Atenção aos detalhes")
        
        if final_scores['C'] >= 2: strengths.append("Empatia"); strengths.append("Persuasão")
        else: weaknesses.append("Comunicação Assertiva")
        
        if final_scores['I'] >= 2: strengths.append("Criatividade"); strengths.append("Flexibilidade")
        else: weaknesses.append("Inovação")
        
        if final_scores['E'] >= 2: strengths.append("Foco em Resultado"); strengths.append("Agilidade")
        else: weaknesses.append("Procrastinação")

        if speed_score >= 2:
            strengths.append("Decisão Rápida")
        else:
            strengths.append("Cautela/Prudência")
            weaknesses.append("Lentidão na Decisão")
        
        st.markdown(f"""
        **Forças:** {', '.join(list(set(strengths)))}
        
        **Fraquezas:** {', '.join(list(set(weaknesses)))}
        
        **Oportunidade:** Mercado valoriza {dominant['name'].split()[-1]}s ágeis.
        """)

    st.markdown("---")
    if st.button("🔄 Refazer Teste"):
        reset_test()

