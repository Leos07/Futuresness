import re
import io
import json
import base64
from collections import defaultdict, Counter
from datetime import datetime
try:
    from wordcloud import WordCloud
except Exception:
    WordCloud = None

try:
    from docx import Document
except Exception:
    Document = None

try:
    import PyPDF2
except Exception:
    PyPDF2 = None

# Minimal vocabulary (kept from original app)
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
    # Other categories shortened for readability but you can expand as needed
    "Futures Concepts": [
        "futures", "future studies", "futures research", "futurism",
        "anticipation", "anticipatory systems", "anticipatory governance",
        "plausible futures", "possible futures", "probable futures", "preferable futures",
    ],
}


class FuturesVocabularyAnalyzer:
    def __init__(self, vocabulary_dict=None):
        self.vocabulary = vocabulary_dict or FUTURES_VOCABULARY
        self.flat_vocabulary = self._flatten_vocabulary()

    def _flatten_vocabulary(self):
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
        text_lower = text.lower()
        term_matches = []
        for term_info in self.flat_vocabulary:
            term = term_info['term']
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
        total_terms = sum(m['frequency'] for m in term_matches)
        unique_terms = len(term_matches)
        word_count = len(text.split())
        category_freq = defaultdict(int)
        for match in term_matches:
            category_freq[match['category']] += match['frequency']
        top_terms = sorted(term_matches, key=lambda x: x['frequency'], reverse=True)[:20]
        return {
            'total_terms': total_terms,
            'unique_terms': unique_terms,
            'word_count': word_count,
            'density': (total_terms / word_count * 100) if word_count > 0 else 0,
            'category_distribution': dict(category_freq),
            'top_terms': top_terms
        }

    def analyze_co_occurrence(self, term_matches, window=100):
        co_occurrences = defaultdict(int)
        for i, match1 in enumerate(term_matches):
            for match2 in term_matches[i+1:]:
                for pos1 in match1['positions']:
                    for pos2 in match2['positions']:
                        if abs(pos1 - pos2) <= window:
                            pair = tuple(sorted([match1['term'], match2['term']]))
                            co_occurrences[pair] += 1
                            break
        return sorted(co_occurrences.items(), key=lambda x: x[1], reverse=True)[:20]

    def detect_methodological_approach(self, term_matches):
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


def read_file_content_bytes(file_bytes: bytes, filename: str):
    """Return text extracted from uploaded bytes and filename-based type detection."""
    file_type = filename.split('.')[-1].lower()
    if file_type == 'txt':
        return file_bytes.decode('utf-8', errors='replace')
    elif file_type == 'pdf' and PyPDF2 is not None:
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text() or ''
            return text
        except Exception:
            return ''
    elif file_type in ['docx', 'doc'] and Document is not None:
        try:
            doc = Document(io.BytesIO(file_bytes))
            return '\n'.join([p.text for p in doc.paragraphs])
        except Exception:
            return ''
    else:
        # Unknown type - try decode
        try:
            return file_bytes.decode('utf-8', errors='replace')
        except Exception:
            return ''


def create_wordcloud_image_bytes(term_matches):
    """Return PNG bytes of a generated wordcloud from term_matches frequencies.
    If WordCloud is not available, return None.
    """
    if WordCloud is None:
        return None
    word_freq = {m['term']: m['frequency'] for m in term_matches}
    if not word_freq:
        return None
    wc = WordCloud(width=800, height=400, background_color='white')
    wc = wc.generate_from_frequencies(word_freq)
    img = wc.to_image()
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.read()


def results_with_wordcloud(analyzer: FuturesVocabularyAnalyzer, text: str, include_wordcloud=True):
    term_matches = analyzer.analyze_document(text)
    stats = analyzer.calculate_statistics(term_matches, text)
    coocc = analyzer.analyze_co_occurrence(term_matches)
    approach = analyzer.detect_methodological_approach(term_matches)
    result = {
        'analysis_timestamp': datetime.now().isoformat(),
        'statistics': stats,
        'term_matches': term_matches,
        'co_occurrences': [{'pair': list(pair), 'count': count} for pair, count in coocc],
        'approach_scores': approach,
    }
    # Always include raw word frequencies for client-side rendering
    result['word_frequencies'] = {m['term']: m['frequency'] for m in term_matches}

    # Optionally include a server-generated image (only when WordCloud is available)
    if include_wordcloud and WordCloud is not None:
        img_bytes = create_wordcloud_image_bytes(term_matches)
        if img_bytes:
            data_url = 'data:image/png;base64,' + base64.b64encode(img_bytes).decode('ascii')
            result['wordcloud_data_url'] = data_url
    return result
