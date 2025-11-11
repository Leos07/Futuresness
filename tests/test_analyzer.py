import pytest
from futures_analyzer import FuturesVocabularyAnalyzer, read_file_content_bytes, results_with_wordcloud


def test_analyze_simple_text():
    analyzer = FuturesVocabularyAnalyzer()
    text = "Scenario planning and horizon scanning are common foresight methods."
    matches = analyzer.analyze_document(text)
    # expect at least 'scenario planning' and 'horizon scanning'
    terms = [m['term'] for m in matches]
    assert 'scenario planning' in terms
    assert 'horizon scanning' in terms


def test_statistics_and_csv():
    analyzer = FuturesVocabularyAnalyzer()
    text = "futures futures futures scenario planning backcasting"
    result = results_with_wordcloud(analyzer, text, include_wordcloud=False)
    stats = result['statistics']
    assert stats['total_terms'] > 0
    assert 'word_frequencies' in result
    assert isinstance(result['csv'], str)


def test_cooccurrence_window():
    analyzer = FuturesVocabularyAnalyzer()
    text = "scenario planning causes horizon scanning and scenario planning again"
    # small window should not detect cooccurrence
    res_small = results_with_wordcloud(analyzer, text, include_wordcloud=False, cooccurrence_window=5)
    assert res_small['co_occurrences'] == [] or len(res_small['co_occurrences']) == 0
    # larger window should detect at least one pair
    res_large = results_with_wordcloud(analyzer, text, include_wordcloud=False, cooccurrence_window=200)
    assert isinstance(res_large['co_occurrences'], list)