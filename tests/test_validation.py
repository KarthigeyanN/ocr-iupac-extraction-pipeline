from src.rdkit_validation import validate_structure


def test_validate_structure_benzene():
    mol = validate_structure("c1ccccc1")  # SMILES for benzene
    assert mol is not None
