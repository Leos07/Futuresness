# 🔮 Futuresness: Futures Studies Vocabulary Analyzer

An interactive web application for analyzing documents to identify and measure the use of futures studies and foresight terminology. This tool helps researchers, practitioners, and students evaluate how futures-oriented their documents are and understand the methodological approaches employed.

## Features

### Core Analysis
- **Comprehensive Vocabulary Database**: 150+ terms across 9 categories of futures studies terminology
- **Frequency Analysis**: Track how often futures terms appear in your documents
- **Category Distribution**: Understand which areas of futures studies are most represented
- **Futures Density Metric**: Calculate the percentage of futures-related terminology in your text

### Enhanced Analytics
- **Methodological Approach Detection**: Automatically identify whether your document uses exploratory, normative, predictive, participatory, or strategic approaches
- **Co-occurrence Analysis**: Discover which futures terms appear together in your document
- **Interactive Visualizations**:
  - Category distribution bar charts
  - Top terms frequency charts
  - Methodological approach pie charts
  - Word clouds of futures terminology
- **Detailed Term Lists**: Export complete lists of all identified terms with frequencies

### Vocabulary Categories
1. **Foresight Methods**: Scenario planning, Delphi method, horizon scanning, weak signals, backcasting, etc.
2. **Futures Concepts**: Plausible futures, uncertainty, disruption, resilience, futures literacy, etc.
3. **Strategic Planning**: Strategy, risk management, early warning systems, decision support, etc.
4. **Drivers of Change**: Technological change, social change, environmental change, disruptors, etc.
5. **Time Perspectives**: Near-term, long-term, horizons, future generations, etc.
6. **Systems Thinking**: Interconnections, feedback loops, complexity, emergence, etc.
7. **Stakeholders & Participation**: Stakeholder engagement, co-creation, participatory methods, etc.
8. **Innovation & Technology**: AI, biotechnology, emerging technologies, clean tech, etc.
9. **Policy & Governance**: Anticipatory governance, policy making, regulation, institutions, etc.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone this repository:
```bash
git clone https://github.com/Leos07/Futuresness.git
cd Futuresness
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Download NLTK data (first time only):
```python
python -c "import nltk; nltk.download('punkt')"
```

## Usage

### Running the Application (Local & Vercel)

There are two supported ways to run the project now:

1) Run the new FastAPI server locally (recommended for Vercel parity):

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000 to use the simple static frontend which calls the API.

2) (Optional) Legacy Streamlit interface

If you prefer the original Streamlit UI (kept for convenience), you can run the preserved legacy app:

```bash
pip install -r dev-requirements.txt
streamlit run legacy_app.py
```

Note: the Streamlit app is kept as a legacy entrypoint. The Vercel-targeted FastAPI server is the primary deployment target.

### Input Methods

**Option 1: Text Input**
- Select "Text Input" in the sidebar
- Paste your text directly into the text area
- Click "Analyze Document"

**Option 2: File Upload**
- Select "File Upload" in the sidebar
- Upload a supported file (TXT, PDF, DOCX)
- Click "Analyze Document"

### Configuration Options

- **Word Cloud**: Toggle visualization of term frequency as a word cloud
- **Co-occurrence Analysis**: Enable analysis of terms appearing together
- **Co-occurrence Window**: Adjust the character distance for co-occurrence detection (50-300 characters)

### Interpreting Results

#### Key Metrics
- **Total Words**: Number of words in your document
- **Futures Terms Found**: Total count of all futures vocabulary occurrences
- **Unique Terms**: Number of different futures terms identified
- **Futures Density**: Percentage of text containing futures terminology (higher = more futures-oriented)

#### Category Distribution
Shows which categories of futures studies are most prevalent in your document. Useful for understanding the breadth of your futures thinking.

#### Methodological Approach
Identifies the dominant futures research approaches in your document:
- **Exploratory**: Exploring multiple possible futures (scenarios, alternatives)
- **Normative**: Working backward from desired futures (backcasting, visioning)
- **Predictive**: Forecasting and trend analysis
- **Participatory**: Stakeholder engagement and co-creation
- **Strategic**: Planning and decision-making focus

#### Co-occurrence Analysis
Reveals which futures concepts are discussed together, helping identify key relationships and themes in your document.

### Exporting Results

Download your analysis results in two formats:
- **CSV**: Spreadsheet-friendly format with term frequencies and categories
- **JSON**: Complete analysis data including statistics and metadata

## Example Use Cases

### Academic Research
- Analyze research papers to quantify futures orientation
- Compare methodological approaches across different studies
- Identify gaps in futures vocabulary coverage

### Strategic Documents
- Evaluate organizational strategic plans for futures thinking
- Assess foresight reports and scenario documents
- Benchmark futures literacy across departments

### Teaching & Learning
- Help students understand different futures methods
- Evaluate assignment quality and futures content
- Demonstrate vocabulary usage in exemplar documents

### Policy Analysis
- Assess policy documents for anticipatory thinking
- Identify dominant approaches in policy foresight
- Compare futures orientation across policy domains

## Technical Details

- **FastAPI**: Server API used by the Vercel deployment and local server
- **Static frontend**: Lightweight `static/index.html` used to call the API
- **Uvicorn**: ASGI server for running the FastAPI app locally
- **Streamlit** (optional): Original interactive UI (kept for local use)
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **Matplotlib/Seaborn**: Static visualizations
- **WordCloud**: Term cloud generation
- **PyPDF2**: PDF file processing
- **python-docx**: Word document processing

### Analysis Algorithm
1. Text preprocessing and normalization
2. Pattern matching with word boundaries for accuracy
3. Multi-word term detection (prioritizes longer phrases)
4. Category aggregation and statistical calculation
5. Co-occurrence detection within configurable windows
6. Methodological approach scoring based on keyword presence

## Contributing

Contributions are welcome! Areas for enhancement:
- Additional futures studies terminology
- New analysis features
- Support for additional file formats
- Multilingual vocabulary support
- Advanced NLP analysis

## License

MIT License - see LICENSE file for details

## Citation

If you use this tool in your research, please cite:
```
Futuresness: Futures Studies Vocabulary Analyzer
https://github.com/Leos07/Futuresness
```

## Contact

For questions, suggestions, or issues, please open an issue on GitHub.

## Acknowledgments

Built with the futures studies and foresight community in mind. Vocabulary compiled from leading futures research methods and frameworks.