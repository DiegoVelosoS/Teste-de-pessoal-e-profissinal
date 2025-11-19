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
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Artificial_neural_network.svg/640px-Artificial_neural_network.svg.png",
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
    # Título Principal
    st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🎯 Seu Dossiê Profissional</h1>", unsafe_allow_html=True)

    # Cálculo de Velocidade e Pontuação Final
    speed_score = calculate_speed_score(st.session_state.time_taken, len(questions))
    final_scores = st.session_state.scores.copy()
    
    if speed_score >= 2:
        final_scores['E'] += speed_score / 2
        final_scores['A'] += speed_score / 2
    else:
        final_scores['E'] += speed_score / 2
    
    dominant_code = max(final_scores, key=final_scores.get)
    
    # --- BASE DE DADOS DE INTELIGÊNCIA DE RH ---
    # Aqui definimos os "scripts" prontos para entrevistas baseados no perfil dominante
    hr_intelligence = {
        'A': {
            'name': 'O ANALISTA ESTRATEGISTA',
            'desc': 'Perfil movido por dados, lógica e precisão. O pilar da organização.',
            'color': '#3498db',
            'qualities': ['Alta capacidade analítica e crítica', 'Organização e método impecáveis', 'Tomada de decisão baseada em fatos', 'Disciplina e foco em qualidade', 'Habilidade de prever riscos'],
            'defects': ['Perfeccionismo (as vezes atrasa entregas)', 'Dificuldade em delegar tarefas complexas', 'Desconforto com improvisos sem dados', 'Posso parecer frio ou distante', 'Excesso de cautela em momentos de urgência'],
            'resume_keywords': ['Análise de Dados', 'Planejamento Estratégico', 'Otimização de Processos', 'Gestão de Riscos', 'Auditoria', 'Compliance', 'KPIs', 'Metodologia Ágil'],
            'avoid': ['Vendas porta-a-porta (agressivas)', 'Ambientes caóticos/sem processos', 'Funções puramente sociais sem desafio intelectual']
        },
        'C': {
            'name': 'O DIPLOMATA COMUNICADOR',
            'desc': 'Perfil movido por conexões, influência e empatia. A cola que une a equipe.',
            'color': '#e91e63',
            'qualities': ['Empatia e inteligência emocional', 'Excelente comunicação verbal e escrita', 'Capacidade de mediação de conflitos', 'Facilidade em networking', 'Persuasão natural'],
            'defects': ['Dificuldade em dizer "não" (sobrecarga)', 'Posso perder o foco em tarefas repetitivas', 'Decido muito pelo coração/emoção', 'Necessidade de aprovação externa', 'Falo demais em reuniões objetivas'],
            'resume_keywords': ['Comunicação Corporativa', 'Liderança de Equipes', 'Negociação', 'Atendimento ao Cliente', 'Treinamento e Desenvolvimento', 'Cultura Organizacional', 'Relações Públicas'],
            'avoid': ['Trabalho isolado em laboratório/ti', 'Análise de planilhas o dia todo', 'Ambientes silenciosos e sem interação']
        },
        'I': {
            'name': 'O VISIONÁRIO INOVADOR',
            'desc': 'Perfil movido por ideias, futuro e criatividade. O motor da mudança.',
            'color': '#9b59b6',
            'qualities': ['Criatividade e "pensar fora da caixa"', 'Adaptabilidade a mudanças rápidas', 'Visão de futuro e tendências', 'Curiosidade intelectual', 'Otimismo diante de problemas'],
            'defects': ['Desorganização com documentos/prazos', 'Dificuldade em terminar o que começa (acabativa)', 'Perco interesse em rotinas', 'Impulsividade com novas ideias', 'Resistência a regras rígidas'],
            'resume_keywords': ['Inovação', 'Design Thinking', 'Solução Criativa de Problemas', 'Empreendedorismo', 'UX/UI', 'Brainstorming', 'Gestão de Mudança', 'Prototipagem'],
            'avoid': ['Contabilidade/Fiscal (regras rígidas)', 'Burocracia estatal repetitiva', 'Funções operacionais de linha de produção']
        },
        'E': {
            'name': 'O EXECUTOR PRAGMÁTICO',
            'desc': 'Perfil movido por ação, metas e velocidade. A força que faz acontecer.',
            'color': '#e67e22',
            'qualities': ['Foco total em resultados e metas', 'Agilidade e senso de urgência', 'Liderança prática e direta', 'Não tenho medo de trabalho duro', 'Resiliência sob pressão'],
            'defects': ['Impaciência com processos lentos', 'Posso ser insensível com a equipe', 'Tendência a assumir trabalho demais', 'Dificuldade em ouvir opiniões longas', 'Foco no curto prazo (apagar incêndio)'],
            'resume_keywords': ['Gestão de Projetos', 'Liderança Orientada a Resultados', 'Eficiência Operacional', 'Logística', 'Vendas', 'Alta Performance', 'Scrum', 'Delivery'],
            'avoid': ['Pesquisa acadêmica de longo prazo', 'Setores muito lentos/burocráticos', 'Funções de suporte passivo']
        }
    }

    profile = hr_intelligence[dominant_code]

    # Exibição do Card Principal
    st.markdown(f"""
        <div style="padding: 20px; background-color: {profile['color']}; color: white; border-radius: 10px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h2 style="color: white; margin:0;">{profile['name']}</h2>
            <p style="font-size: 18px; margin-top: 5px; font-style: italic;">"{profile['desc']}"</p>
        </div>
    """, unsafe_allow_html=True)

    # --- ABA DE PREPARAÇÃO PARA ENTREVISTA ---
    st.subheader("🎙️ Preparação para Entrevista")
    st.info("Use as frases abaixo quando o recrutador perguntar: **'Fale sobre seus pontos fortes e pontos a melhorar'**.")

    col_q, col_d = st.columns(2)
    with col_q:
        st.markdown("### ✅ 5 Qualidades (Para citar)")
        for q in profile['qualities']:
            st.markdown(f"- {q}")
    
    with col_d:
        st.markdown("### ⚠️ 5 Pontos de Melhoria (Honestos)")
        for d in profile['defects']:
            st.markdown(f"- {d}")

    st.markdown("---")

    # --- ABA DE CURRÍCULO E CARREIRA ---
    col_cv, col_risk = st.columns(2)
    
    with col_cv:
        st.subheader("📄 Para seu Currículo (Resumo)")
        st.write("Adicione estes termos no seu 'Resumo Profissional' ou 'Competências':")
        
        # Cria tags visuais para as palavras-chave
        tags_html = "".join([f"<span style='background-color:#e0e0e0; color:#333; padding:4px 8px; border-radius:4px; margin:2px; display:inline-block; font-size:0.9em;'>{k}</span>" for k in profile['resume_keywords']])
        st.markdown(tags_html, unsafe_allow_html=True)

    with col_risk:
        st.subheader("⛔ Áreas para Evitar")
        st.write("Ambientes que podem causar frustração ou baixo desempenho para seu perfil:")
        for avoid in profile['avoid']:
            st.markdown(f"❌ **{avoid}**")

    # --- GRÁFICO DE RADAR ---
    st.markdown("---")
    st.subheader("📊 Raio-X Visual das Competências")
    
    categories_for_chart = ['Analítico', 'Comunicador', 'Inovador', 'Executor', 'Velocidade']
    values_for_chart = [final_scores['A'], final_scores['C'], final_scores['I'], final_scores['E'], speed_score]
    values_plot = values_for_chart + [values_for_chart[0]]
    categories_plot = categories_for_chart + [categories_for_chart[0]]

    fig = go.Figure(data=go.Scatterpolar(
      r=values_plot,
      theta=categories_plot,
      fill='toself',
      line_color=profile['color'],
      name='Seu Perfil'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, max(values_for_chart)+1])), showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)

    st.success(f"⏱️ Tempo de Resposta: {int(st.session_state.time_taken)} segundos. " + 
               ("Ótima agilidade!" if speed_score >= 2 else "Perfil cauteloso e analítico."))

    if st.button("🔄 Refazer Teste"):
        reset_test()
