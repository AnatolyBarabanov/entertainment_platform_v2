# Entertainment & Media Recommendation Platform (v2)

- Movies: actors + ratings, actor search, min rating filter
- Music: expanded dataset, cosine feature similarity
- Hybrid recommender (prefs + graph neighbors + rating)
- Streamlit GUI

## Run
```bash
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/ui/streamlit_app.py
```