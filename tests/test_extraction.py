from src.iupac_extraction import extract_iupac


def test_extract_iupac_simple():
    text = "The compound benzene is aromatic."
    name = extract_iupac(text)
    assert name.lower() == "benzene"
