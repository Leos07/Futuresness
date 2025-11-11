"""
DEPRECATED: `app.py` (legacy Streamlit UI)

This file used to contain the Streamlit application. The project now uses a FastAPI
server (`api/main.py`) and a lightweight static frontend for deployment on Vercel.

If you still want to run the legacy Streamlit interface locally, run:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1   # PowerShell
    python -m pip install -r dev-requirements.txt
    streamlit run legacy_app.py

The full Streamlit app has been preserved in `legacy_app.py`.
"""

print("This repository has migrated to a FastAPI-based server. See README for details.")

# Comprehensive Futures Studies Vocabulary Database
FUTURES_VOCABULARY = {
    "Foresight Methods": [
        "scenario planning", "scenarios", "scenario analysis", "scenario building",
        "delphi method", "delphi", "expert panel", "expert consultation",
        "horizon scanning", "environmental scanning", "scanning",
        "trend analysis", "trend monitoring", "megatrends", "macro trends",
        "weak signals", "weak signal detection", "emerging issues",
        "wild cards", "black swans", "surprises",
        "backcasting", "normative scenarios",
        "causal layered analysis", "CLA",
        "futures wheel", "futures triangle",
        "cross-impact analysis", "morphological analysis",
        "roadmapping", "technology roadmapping",
        "visioning", "vision building", "preferred futures",
        "foresight", "strategic foresight", "corporate foresight",
        "forecasting", "predictive analytics", "extrapolation",
        "simulation", "modeling", "system dynamics",
    ],

    "Futures Concepts": [
        "futures", "future studies", "futures research", "futurism",
        "anticipation", "anticipatory systems", "anticipatory governance",
        "plausible futures", "possible futures", "probable futures", "preferable futures",
        "alternative futures", "multiple futures", "futures cone",
        "uncertainty", "ambiguity", "complexity", "volatility", "VUCA",
        "emergence", "emergent properties", "emerging trends",
        "disruption", "disruptive innovation", "discontinuity",
        "transformation", "transformative change", "transition",
        "resilience", "adaptive capacity", "adaptability",
        "long-term thinking", "long-term perspective", "temporal depth",
        "foresight capacity", "futures literacy", "futures thinking",
        "futures consciousness", "anticipatory awareness",
    ],

    "Strategic Planning": [
        "strategic planning", "strategy", "strategic management",
        "strategic analysis", "strategic options", "strategic choices",
        "strategic intelligence", "competitive intelligence",
        "risk management", "risk assessment", "risk analysis",
        "opportunity identification", "opportunity analysis",
        "contingency planning", "preparedness",
        "early warning systems", "monitoring systems",
        "decision support", "decision making", "strategic decisions",
        "innovation strategy", "innovation management",
        "change management", "organizational change",
    ],

    "Drivers of Change": [
        "drivers", "driving forces", "change drivers",
        "technological change", "technology trends", "digital transformation",
        "social change", "societal trends", "demographic shifts",
        "economic change", "economic trends", "globalization",
        "environmental change", "climate change", "sustainability",
        "political change", "geopolitical shifts", "governance",
        "cultural change", "values shift", "paradigm shift",
        "disruptors", "game changers", "tipping points",
    ],

    "Time Perspectives": [
        "near-term", "short-term", "medium-term", "long-term", "very long-term",
        "horizon", "time horizon", "temporal horizon",
        "2030", "2040", "2050", "next decade", "coming years",
        "future generations", "intergenerational",
        "nowcasting", "present", "current state",
    ],

    "Systems Thinking": [
        "systems thinking", "systems approach", "holistic approach",
        "interconnections", "interdependencies", "relationships",
        "feedback loops", "positive feedback", "negative feedback",
        "leverage points", "intervention points",
        "system boundaries", "system structure", "system behavior",
        "complexity science", "complex adaptive systems",
        "emergence", "self-organization", "nonlinearity",
    ],

    "Stakeholders & Participation": [
        "stakeholders", "stakeholder engagement", "stakeholder analysis",
        "participatory", "participation", "co-creation",
        "citizens", "civil society", "public engagement",
        "experts", "expertise", "knowledge integration",
        "multi-stakeholder", "collaborative foresight",
        "deliberation", "dialogue", "consultation",
    ],

    "Innovation & Technology": [
        "innovation", "technological innovation", "social innovation",
        "emerging technologies", "breakthrough technologies",
        "artificial intelligence", "AI", "machine learning",
        "biotechnology", "nanotechnology", "quantum computing",
        "automation", "robotics", "internet of things", "IoT",
        "blockchain", "cryptocurrencies",
        "renewable energy", "clean tech", "green technology",
        "space exploration", "synthetic biology",
    ],

    "Policy & Governance": [
        "policy", "public policy", "policy making", "policy design",
        "governance", "anticipatory governance", "adaptive governance",
        "regulation", "regulatory frameworks",
        "institutions", "institutional change",
        "government", "public sector", "policy makers",
        "legislation", "policy instruments",
    ],
}

class FuturesVocabularyAnalyzer:
    def __init__(self, vocabulary_dict):
        self.vocabulary = vocabulary_dict
        self.flat_vocabulary = self._flatten_vocabulary()

    def _flatten_vocabulary(self):
        """Flatten vocabulary dictionary to list with categories"""
        flat_list = []
        for category, terms in self.vocabulary.items():
            for term in terms:
                flat_list.append({
                    'term': term.lower(),
                    'category': category,
                    'length': len(term.split())
                })
        return sorted(flat_list, key=lambda x: x['length'], reverse=True)

    def analyze_document(self, text):
        """Analyze document for futures vocabulary"""
        text_lower = text.lower()

        # Find all term occurrences
        term_matches = []
        for term_info in self.flat_vocabulary:
            term = term_info['term']
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(term) + r'\b'
            matches = list(re.finditer(pattern, text_lower))

            if matches:
                term_matches.append({
                    'term': term,
                    'category': term_info['category'],
                    'frequency': len(matches),
                    'positions': [m.start() for m in matches]
                })

        return term_matches

    def calculate_statistics(self, term_matches, text):
        """Calculate various statistics"""
        total_terms = sum(m['frequency'] for m in term_matches)
        unique_terms = len(term_matches)
        word_count = len(text.split())

        # Category distribution
        category_freq = defaultdict(int)
        for match in term_matches:
            category_freq[match['category']] += match['frequency']

        # Most common terms
        top_terms = sorted(term_matches, key=lambda x: x['frequency'], reverse=True)[:20]

        return {
            'total_terms': total_terms,
            'unique_terms': unique_terms,
            'word_count': word_count,
            'density': (total_terms / word_count * 100) if word_count > 0 else 0,
            'category_distribution': dict(category_freq),
            'top_terms': top_terms
        }

    def analyze_co_occurrence(self, term_matches, text, window=100):
        """Analyze term co-occurrences within a window"""
        co_occurrences = defaultdict(int)

        for i, match1 in enumerate(term_matches):
            for match2 in term_matches[i+1:]:
                # Check if terms co-occur within window
                for pos1 in match1['positions']:
                    for pos2 in match2['positions']:
                        if abs(pos1 - pos2) <= window:
                            pair = tuple(sorted([match1['term'], match2['term']]))
                            co_occurrences[pair] += 1
                            break

        return sorted(co_occurrences.items(), key=lambda x: x[1], reverse=True)[:20]

    def detect_methodological_approach(self, term_matches):
        """Detect the dominant methodological approach"""
        method_keywords = {
            'Exploratory': ['scenario', 'futures cone', 'alternative futures', 'possible futures'],
            'Normative': ['backcasting', 'visioning', 'preferred futures', 'vision building'],
            'Predictive': ['forecasting', 'trend analysis', 'extrapolation', 'predictive'],
            'Participatory': ['stakeholder', 'participatory', 'co-creation', 'engagement'],
            'Strategic': ['strategic', 'planning', 'decision', 'risk management'],
        }

        approach_scores = defaultdict(int)
        for match in term_matches:
            term = match['term']
            for approach, keywords in method_keywords.items():
                if any(keyword in term for keyword in keywords):
                    approach_scores[approach] += match['frequency']

        return dict(sorted(approach_scores.items(), key=lambda x: x[1], reverse=True))

def read_file_content(uploaded_file):
    """Read content from uploaded file"""
    try:
        file_type = uploaded_file.name.split('.')[-1].lower()

        if file_type == 'txt':
            return uploaded_file.getvalue().decode('utf-8')

        elif file_type == 'pdf':
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text

        elif file_type in ['docx', 'doc']:
            doc = Document(io.BytesIO(uploaded_file.getvalue()))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text

        else:
            st.error(f"Unsupported file type: {file_type}")
            return None

    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None

def create_wordcloud(term_matches):
    """Create word cloud from term matches"""
    word_freq = {match['term']: match['frequency'] for match in term_matches}

    if not word_freq:
        return None

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        relative_scaling=0.5,
        min_font_size=10
    ).generate_from_frequencies(word_freq)

    return wordcloud

def plot_category_distribution(category_dist):
    """Create interactive bar chart for category distribution"""
    df = pd.DataFrame(list(category_dist.items()), columns=['Category', 'Frequency'])
    df = df.sort_values('Frequency', ascending=True)

    fig = px.bar(df, x='Frequency', y='Category', orientation='h',
                 title='Futures Vocabulary by Category',
                 color='Frequency',
                 color_continuous_scale='Blues')
    fig.update_layout(showlegend=False, height=500)
    return fig

def plot_top_terms(top_terms):
    """Create bar chart for top terms"""
    df = pd.DataFrame([
        {'Term': t['term'], 'Frequency': t['frequency'], 'Category': t['category']}
        for t in top_terms
    ])

    fig = px.bar(df, x='Frequency', y='Term', orientation='h',
                 title='Top 20 Most Frequent Terms',
                 color='Category',
                 hover_data=['Category'])
    fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
    return fig

def plot_methodological_approach(approach_scores):
    """Create pie chart for methodological approaches"""
    if not approach_scores:
        return None

    fig = go.Figure(data=[go.Pie(
        labels=list(approach_scores.keys()),
        values=list(approach_scores.values()),
        hole=.3
    )])
    fig.update_layout(title='Detected Methodological Approaches')
    return fig

def export_results(term_matches, statistics, text):
    """Export results to various formats"""
    results = {
        'analysis_timestamp': datetime.now().isoformat(),
        'statistics': statistics,
        'term_matches': term_matches,
        'document_preview': text[:500] + '...' if len(text) > 500 else text
    }
    return json.dumps(results, indent=2)

# Main App
def main():
    st.markdown('<h1 class="main-header">🔮 Futures Studies Vocabulary Analyzer</h1>', unsafe_allow_html=True)

    st.markdown("""
    This application analyzes documents to identify and measure the use of futures studies and
    foresight terminology. Upload a document or paste text to get comprehensive insights.
    """)

    # Initialize analyzer
    analyzer = FuturesVocabularyAnalyzer(FUTURES_VOCABULARY)

    # Sidebar
    with st.sidebar:
        st.header("📋 Configuration")

        st.subheader("Input Method")
        input_method = st.radio("Choose input method:", ["Text Input", "File Upload"])

        st.subheader("Analysis Options")
        show_wordcloud = st.checkbox("Show Word Cloud", value=True)
        show_cooccurrence = st.checkbox("Show Co-occurrence Analysis", value=True)
        cooccurrence_window = st.slider("Co-occurrence Window (characters)", 50, 300, 100)

        st.subheader("Vocabulary Coverage")
        total_terms = sum(len(terms) for terms in FUTURES_VOCABULARY.values())
        st.info(f"📚 Database contains **{total_terms}** futures studies terms across **{len(FUTURES_VOCABULARY)}** categories")

        with st.expander("View Vocabulary Categories"):
            for category, terms in FUTURES_VOCABULARY.items():
                st.write(f"**{category}** ({len(terms)} terms)")

    # Main content area
    text = None

    if input_method == "Text Input":
        text = st.text_area(
            "Paste your text here:",
            height=300,
            placeholder="Enter or paste the document text you want to analyze..."
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload a document (TXT, PDF, DOCX)",
            type=['txt', 'pdf', 'docx']
        )
        if uploaded_file:
            with st.spinner("Reading file..."):
                text = read_file_content(uploaded_file)
                if text:
                    st.success(f"✅ File loaded: {uploaded_file.name}")
                    with st.expander("Preview document"):
                        st.text(text[:1000] + "..." if len(text) > 1000 else text)

    # Analyze button
    if st.button("🔍 Analyze Document", type="primary", use_container_width=True):
        if not text or len(text.strip()) == 0:
            st.error("Please provide text to analyze")
        else:
            with st.spinner("Analyzing document..."):
                # Perform analysis
                term_matches = analyzer.analyze_document(text)

                if not term_matches:
                    st.warning("No futures studies vocabulary found in the document.")
                else:
                    statistics = analyzer.calculate_statistics(term_matches, text)

                    # Display key metrics
                    st.header("📊 Analysis Results")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Words", f"{statistics['word_count']:,}")
                    with col2:
                        st.metric("Futures Terms Found", statistics['total_terms'])
                    with col3:
                        st.metric("Unique Terms", statistics['unique_terms'])
                    with col4:
                        st.metric("Futures Density", f"{statistics['density']:.2f}%")

                    st.divider()

                    # Category distribution
                    st.subheader("📈 Category Distribution")
                    fig_category = plot_category_distribution(statistics['category_distribution'])
                    st.plotly_chart(fig_category, use_container_width=True)

                    # Top terms
                    st.subheader("🏆 Top Terms")
                    fig_terms = plot_top_terms(statistics['top_terms'])
                    st.plotly_chart(fig_terms, use_container_width=True)

                    # Methodological approach
                    st.subheader("🎯 Methodological Approach Detection")
                    approach_scores = analyzer.detect_methodological_approach(term_matches)

                    if approach_scores:
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            fig_approach = plot_methodological_approach(approach_scores)
                            st.plotly_chart(fig_approach, use_container_width=True)
                        with col2:
                            st.write("**Approach Breakdown:**")
                            for approach, score in approach_scores.items():
                                percentage = (score / statistics['total_terms'] * 100) if statistics['total_terms'] > 0 else 0
                                st.write(f"- **{approach}**: {score} terms ({percentage:.1f}%)")

                    # Word cloud
                    if show_wordcloud:
                        st.subheader("☁️ Term Cloud")
                        wordcloud = create_wordcloud(term_matches)
                        if wordcloud:
                            fig, ax = plt.subplots(figsize=(12, 6))
                            ax.imshow(wordcloud, interpolation='bilinear')
                            ax.axis('off')
                            st.pyplot(fig)

                    # Co-occurrence analysis
                    if show_cooccurrence:
                        st.subheader("🔗 Term Co-occurrence Analysis")
                        st.write(f"Terms appearing within {cooccurrence_window} characters of each other:")
                        co_occurrences = analyzer.analyze_co_occurrence(term_matches, text, cooccurrence_window)

                        if co_occurrences:
                            cooc_df = pd.DataFrame([
                                {'Term 1': pair[0], 'Term 2': pair[1], 'Co-occurrences': count}
                                for pair, count in co_occurrences
                            ])
                            st.dataframe(cooc_df, use_container_width=True)
                        else:
                            st.info("No significant co-occurrences found.")

                    # Detailed term list
                    st.subheader("📋 Complete Term List")
                    term_df = pd.DataFrame([
                        {
                            'Term': m['term'],
                            'Category': m['category'],
                            'Frequency': m['frequency']
                        }
                        for m in term_matches
                    ]).sort_values('Frequency', ascending=False)

                    st.dataframe(term_df, use_container_width=True, height=400)

                    # Export options
                    st.subheader("💾 Export Results")
                    col1, col2 = st.columns(2)

                    with col1:
                        csv_data = term_df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv_data,
                            file_name=f"futures_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )

                    with col2:
                        json_data = export_results(term_matches, statistics, text)
                        st.download_button(
                            label="Download JSON",
                            data=json_data,
                            file_name=f"futures_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )

if __name__ == "__main__":
    main()
