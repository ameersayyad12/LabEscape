# utils.py

def is_non_academic_affiliation(affiliation: str) -> bool:
    """
    Heuristic: returns True if affiliation appears to be non-academic.
    """
    academic_keywords = [
        "university", "college", "institute", "school", "faculty", "hospital",
        "center", "centre", "department", "dept"
    ]

    # NOTE: We're allowing 'lab' and 'laboratory' because they occur in company names too.
    affiliation = affiliation.lower()
    return not any(keyword in affiliation for keyword in academic_keywords)
