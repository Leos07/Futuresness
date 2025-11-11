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
        """Analyze text and return term matches with positions and snippets.

        Each match dict includes: term, category, frequency, positions, snippets
        """
        text_lower = text.lower()
        term_matches = []
        for term_info in self.flat_vocabulary:
            term = term_info['term']
            pattern = r'\b' + re.escape(term) + r'\b'
            matches = list(re.finditer(pattern, text_lower))
            if matches:
                positions = [m.start() for m in matches]
                snippets = []
                for pos in positions:
                    # context window in original text (preserve casing)
                    start = max(0, pos - 60)
                    end = min(len(text), pos + len(term) + 60)
                    snippet = text[start:end].strip()
                    snippets.append(snippet)

                term_matches.append({
                    'term': term,
                    'category': term_info['category'],
                    'frequency': len(matches),
                    'positions': positions,
                    'snippets': snippets
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

        # Normalized frequency per 1000 words
        normalized_per_1000 = (total_terms / word_count * 1000) if word_count > 0 else 0

        # Category coverage: percent of categories that appear at least once
        categories_present = sum(1 for v in category_freq.values() if v > 0)
        total_categories = len(self.vocabulary)
        category_coverage = (categories_present / total_categories * 100) if total_categories > 0 else 0

        return {
            'total_terms': total_terms,
            'unique_terms': unique_terms,
            'word_count': word_count,
            'density': (total_terms / word_count * 100) if word_count > 0 else 0,
            'normalized_per_1000': normalized_per_1000,
            'category_distribution': dict(category_freq),
            'category_coverage_percent': category_coverage,
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


def results_with_wordcloud(analyzer: FuturesVocabularyAnalyzer, text: str, include_wordcloud=True, cooccurrence_window: int = 100):
    term_matches = analyzer.analyze_document(text)
    stats = analyzer.calculate_statistics(term_matches, text)
    coocc = analyzer.analyze_co_occurrence(term_matches, window=cooccurrence_window)
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
    # Add CSV export string
    try:
        result['csv'] = export_terms_csv(term_matches)
    except Exception:
        result['csv'] = None

    # Add simple clustering information based on co-occurrence pairs
    try:
        term2cluster, clusters = compute_clusters_from_coocc(coocc)
        result['clusters'] = clusters
        result['term_cluster_map'] = term2cluster
    except Exception:
        result['clusters'] = []
        result['term_cluster_map'] = {}

    return result


def compute_clusters_from_coocc(co_occurrences):
    """Compute connected components (clusters) from co-occurrence pairs.

    co_occurrences: list of (pair, count) where pair is (term1, term2)
    Returns mapping term -> cluster_id and list of clusters (each cluster is list of terms)
    """
    # Build adjacency
    adj = {}
    for item in co_occurrences:
        # item may be ( (a,b), count ) or dict {'pair': [a,b], 'count': n}
        if isinstance(item, dict):
            pair = tuple(item.get('pair', []))
        else:
            pair = item[0]
        if not pair or len(pair) != 2:
            continue
        a, b = pair[0], pair[1]
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)

    visited = set()
    clusters = []
    for node in adj.keys():
        if node in visited:
            continue
        stack = [node]
        comp = []
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            comp.append(v)
            for nb in adj.get(v, []):
                if nb not in visited:
                    stack.append(nb)
        if comp:
            clusters.append(comp)

    # Also include isolated terms (if any) - caller can include them via word_frequencies but here we return clusters only for cooccurring terms
    term2cluster = {}
    for i, comp in enumerate(clusters):
        for term in comp:
            term2cluster[term] = i

    return term2cluster, clusters


def export_terms_csv(term_matches):
    """Return a CSV string of term matches suitable for download"""
    import csv

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['term', 'category', 'frequency', 'snippets'])
    for m in term_matches:
        snippets_joined = ' ||| '.join(m.get('snippets', [])[:3])
        writer.writerow([m['term'], m['category'], m['frequency'], snippets_joined])
    return output.getvalue()
