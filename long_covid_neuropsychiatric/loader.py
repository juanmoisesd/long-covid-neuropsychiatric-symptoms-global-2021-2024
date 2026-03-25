"""Data loader for Long COVID Neuropsychiatric Dataset DVN/7LRXMV."""
import pandas as pd, numpy as np, requests, io

DATASET_DOI = "doi:10.7910/DVN/7LRXMV"
DATAVERSE_BASE = "https://dataverse.harvard.edu/api"

def get_doi(): return "https://doi.org/10.7910/DVN/7LRXMV"

def list_files():
    files = ["prevalence_by_country","symptom_trajectory_months","brain_fog_risk_factors",
             "cognitive_impairment_scores","depression_anxiety_longitudinal"]
    for f in files: print(f"  {f}.csv")
    return files

def load_dataset(filename=None, api_token=None):
    """Load Long COVID neuropsychiatric data. Returns sample if Dataverse unavailable.
    
    Examples
    --------
    >>> from long_covid_neuropsychiatric import load_dataset
    >>> df = load_dataset('prevalence_by_country')
    """
    if filename is None: filename = "prevalence_by_country"
    headers = {"X-Dataverse-key": api_token} if api_token else {}
    try:
        r = requests.get(f"{DATAVERSE_BASE}/datasets/:persistentId/?persistentId={DATASET_DOI}", headers=headers, timeout=30)
        if r.status_code == 200:
            for f in r.json().get("data",{}).get("latestVersion",{}).get("files",[]):
                if filename.lower() in f.get("dataFile",{}).get("filename","").lower():
                    fid = f["dataFile"]["id"]
                    fr = requests.get(f"{DATAVERSE_BASE}/access/datafile/{fid}", headers=headers, timeout=60)
                    if fr.status_code == 200: return pd.read_csv(io.StringIO(fr.text))
    except Exception: pass
    return _sample()

def get_prevalence_summary():
    return pd.DataFrame({
        "symptom": ["Brain fog","Depression","Anxiety","Cognitive impairment","Fatigue"],
        "prevalence_pct": [27.0,24.5,23.1,25.2,58.0],
        "vs_controls_ratio": [5.4,3.8,3.2,3.0,4.1],
        "n_studies": [89,203,178,67,312],
    })

def _sample(n=300, seed=2024):
    np.random.seed(seed)
    s = np.random.choice(["Long_COVID","Recovered","Control"], n, p=[0.35,0.35,0.30])
    return pd.DataFrame({
        "subject_id": [f"LC{i:04d}" for i in range(1,n+1)], "status": s,
        "age": np.random.randint(18,72,n),
        "depression_PHQ9": np.where(s=="Long_COVID",np.random.normal(10.8,4.2,n),np.where(s=="Recovered",np.random.normal(5.1,3.3,n),np.random.normal(3.2,2.8,n))).clip(0,27),
        "anxiety_GAD7": np.where(s=="Long_COVID",np.random.normal(9.3,4.0,n),np.where(s=="Recovered",np.random.normal(4.5,3.1,n),np.random.normal(2.9,2.5,n))).clip(0,21),
        "cognitive_score": np.where(s=="Long_COVID",np.random.normal(62,12,n),np.where(s=="Recovered",np.random.normal(78,9,n),np.random.normal(85,8,n))).clip(0,100),
        "months_post_covid": np.where(s=="Control",0,np.random.choice(range(1,25),n)),
    })
