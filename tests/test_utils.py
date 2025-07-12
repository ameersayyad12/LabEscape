from get_papers.utils import is_non_academic_affiliation

def test_is_non_academic_affiliation():
    assert is_non_academic_affiliation("Pfizer Inc.") == True
    assert is_non_academic_affiliation("Harvard University") == False
    assert is_non_academic_affiliation("Genentech Labs, CA") == True
    assert is_non_academic_affiliation("Oxford University Hospitals") == False
