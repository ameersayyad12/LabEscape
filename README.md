# 🧪 LabEscape

> **Escape the academic bubble — find real-world research**

LabEscape helps you filter PubMed results to find papers authored by **non-academic researchers** — including industry scientists, biotech firms, and pharma teams.

![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/built_with-streamlit-orange?logo=streamlit)
![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 🚀 Features

- 🔍 Search PubMed with any topic
- 🧪 Filters results to show only **non-academic author affiliations**
- 📊 Displays author names, affiliations, publication year, and emails (if available)
- 📥 CSV export support
- 💡 Streamlit-based interactive UI
- 🧠 Heuristic keyword filtering for academic institutions

---

## 📸 Demo

<img width="1914" height="767" alt="Screenshot 2025-07-12 192359" src="https://github.com/user-attachments/assets/ac719657-5641-4915-8c8e-8722b0bbd1e6" />



---

## 🛠 Tech Stack

| Layer          | Tools                                 |
|----------------|----------------------------------------|
| Language       | Python 3.10+                          |
| CLI Backend    | Typer + requests + pandas             |
| Web UI         | Streamlit                             |
| Data Source    | PubMed E-utilities API (efetch, esearch) |
| Testing        | pytest                                |
| Deployment     | Streamlit Cloud (optional)            |

---

## 🧪 How it Works

1. Sends query to PubMed using E-utilities API
2. Parses returned article metadata (authors, affiliations)
3. Filters out affiliations that contain keywords like `"university"`, `"college"`, `"hospital"`, etc.
4. Returns only those with at least one **non-academic** author

---

## 🧪 Run It Locally

```bash
git clone https://github.com/ameersayyad12/LabEscape.git
cd LabEscape

# Install dependencies via poetry
poetry install

# Run CLI (optional)
poetry run get-papers-list "machine learning in drug discovery"

# Run Streamlit UI
poetry run streamlit run streamlit_app.py


