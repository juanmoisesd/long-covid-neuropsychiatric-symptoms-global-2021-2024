"""Global prevalence data on Long COVID neurological and psychiatric symptoms (brain fog, anxiety, depr
DOI: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/7LRXMV | GitHub: https://github.com/juanmoisesd/long-covid-neuropsychiatric-symptoms-global-2021-2024"""
__version__="1.0.0"
__author__="de la Serna, Juan Moisés"
import pandas as pd, io
try:
    import requests
except ImportError:
    raise ImportError("pip install requests")

def load_data(filename=None):
    """Load dataset from Zenodo. Returns pandas DataFrame."""
    rid="https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/7LRXMV".split(".")[-1]
    meta=requests.get(f"https://zenodo.org/api/records/{rid}",timeout=30).json()
    csvs=[f for f in meta.get("files",[]) if f["key"].endswith(".csv")]
    if not csvs: raise ValueError("No CSV files found")
    f=next((x for x in csvs if filename and x["key"]==filename),csvs[0])
    return pd.read_csv(io.StringIO(requests.get(f["links"]["self"],timeout=60).text))

def cite(): return f'de la Serna, Juan Moisés (2025). Global prevalence data on Long COVID neurological and psychiatric symptoms (brai. Zenodo. https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/7LRXMV'
def info(): print(f"Dataset: Global prevalence data on Long COVID neurological and psychiatric symptoms (brai\nDOI: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/7LRXMV\nGitHub: https://github.com/juanmoisesd/long-covid-neuropsychiatric-symptoms-global-2021-2024")