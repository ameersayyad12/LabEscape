# fetch.py

import requests
import pandas as pd
from typing import List
from get_papers.utils import is_non_academic_affiliation

BASE_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
BASE_EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_and_process_papers(query: str, debug: bool = False) -> pd.DataFrame:
    if debug:
        print(f"🔍 Fetching PubMed IDs for query: {query}")

    # Step 1: Search for PMIDs
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 50
    }

    response = requests.get(BASE_ESEARCH_URL, params=search_params)
    response.raise_for_status()
    pmids = response.json()["esearchresult"]["idlist"]

    if debug:
        print(f"✅ Found {len(pmids)} paper(s): {pmids}")

    # Step 2: Fetch metadata for those PMIDs
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }

    response = requests.get(BASE_EFETCH_URL, params=fetch_params)
    response.raise_for_status()

    from xml.etree import ElementTree as ET
    root = ET.fromstring(response.text)

    papers = []
    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date = article.findtext(".//PubDate/Year") or "N/A"
        authors = article.findall(".//Author")

        non_acad_authors = []
        affiliations = set()
        corresponding_email = None

        for author in authors:
            fname = author.findtext("ForeName") or ""
            lname = author.findtext("LastName") or ""
            name = f"{fname.strip()} {lname.strip()}".strip()

            affs = author.findall(".//AffiliationInfo/Affiliation")
            aff_texts = [aff.text.strip() for aff in affs if aff is not None and aff.text]

            # DEBUG: print raw affiliations
            if debug and aff_texts:
                print(f"👤 {name} affiliations: {aff_texts}")

            # Apply heuristic filter
            non_academic_affs = [aff for aff in aff_texts if is_non_academic_affiliation(aff)]
            if debug and non_academic_affs:
                print(f"✅ Non-academic: {non_academic_affs}")

            if non_academic_affs:
                non_acad_authors.append(name)
                affiliations.update(non_academic_affs)

            # Capture email
            if not corresponding_email:
                for aff in aff_texts:
                    if "@" in aff:
                        for word in aff.split():
                            if "@" in word:
                                corresponding_email = word.strip(".,;()")
                                break

        if non_acad_authors:
            papers.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": "; ".join(set(non_acad_authors)),
                "Company Affiliation(s)": "; ".join(affiliations),
                "Corresponding Author Email": corresponding_email or "N/A"
            })

    if debug:
        print(f"📄 Returning {len(papers)} filtered papers")

    return pd.DataFrame(papers) if papers else pd.DataFrame()
