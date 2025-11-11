# Quick Start Guide

## Install and Run in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

-### 2. Run the Application (Local server)

Run the FastAPI server and open the static frontend:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
python -m pip install -r requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` in your browser and paste text or upload a file and click Analyze.

### 3. (Optional) Run legacy Streamlit UI

If you prefer the original Streamlit interface (kept for convenience):

```bash
pip install -r dev-requirements.txt
streamlit run legacy_app.py
```

- Try the included sample: Copy text from `sample_document.txt`
- Paste into the text area or upload your own document
- Click "Analyze Document"

## What You'll See

The analysis provides:
- **Key metrics**: Total words, futures terms found, unique terms, and futures density
- **Visual charts**: Category distribution, top terms, methodological approaches
- **Word cloud**: Visual representation of term frequencies
- **Co-occurrence analysis**: Terms that appear together
- **Export options**: Download results as CSV or JSON

## Tips for Best Results

1. **Longer documents work better**: At least 500 words recommended
2. **Academic or strategic documents**: Papers, reports, policy documents yield rich analysis
3. **Adjust co-occurrence window**: Use 50-100 for focused analysis, 200-300 for broader connections
4. **Compare documents**: Analyze multiple documents to benchmark futures orientation

## Sample Analysis

Try analyzing the included `sample_document.txt` to see a well-structured futures document with:
- 70+ unique futures terms
- Coverage across all 9 vocabulary categories
- Multiple methodological approaches
- Rich co-occurrence patterns

## Troubleshooting

**Issue**: Module not found errors
**Solution**: Run `pip install -r requirements.txt` again

**Issue**: File upload not working for PDF/DOCX
**Solution**: Ensure PyPDF2 and python-docx are installed

**Issue**: Visualizations not displaying
**Solution**: Clear browser cache and refresh the page

## Next Steps

- Analyze your own strategic documents
- Compare different time periods or departments
- Use results to improve futures literacy
- Export data for further analysis in Excel or other tools

For detailed documentation, see [README.md](README.md)
