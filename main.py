from fastapi import FastAPI, Query
from typing import List
import pandas as pd

app = FastAPI()

# ✅ Use the correct Google Drive direct download link
cutoff_df = pd.read_csv("https://drive.google.com/uc?export=download&id=1AkIPPpu1XGXhBleR-x1GFLpENISIGuFm")

@app.get("/preference-list")
def preference_list(place: str, percentile: float, branches: List[str] = Query(...)):
    df = cutoff_df.copy()
    df['Cutoff'] = pd.to_numeric(df['Cutoff'], errors='coerce')

    filtered = df[
        (df['Place'].str.strip().str.lower() == place.strip().lower()) & 
        (df['Branch'].isin(branches)) & 
        (df['Cutoff'].between(percentile - 10, percentile + 10))
    ]

    filtered['MatchScore'] = abs(filtered['Cutoff'] - percentile)
    filtered = filtered.sort_values(by='MatchScore')
    filtered = filtered.drop(columns='MatchScore')

    return filtered.to_dict(orient='records')

@app.get("/all")
def all_entries():
    df = cutoff_df.copy()
    df['Cutoff'] = pd.to_numeric(df['Cutoff'], errors='coerce')
    return df.to_dict(orient='records')
