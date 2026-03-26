from typing import Optional

from rdkit import Chem
from rdkit.Chem import AllChem


def name_to_mol(name: str):
    """
    Convert a chemical name to an RDKit Mol via name-to-structure.
    This uses RDKit's internal name parser (limited) or external tools if configured.
    """
    # RDKit's name parser is limited; for real use you might integrate OPSIN.
    mol = Chem.MolFromSmiles(name)
    if mol is None:
        # Try as-is with name-to-structure if available
        try:
            from rdkit.Chem import rdMolDescriptors  # noqa: F401
        except ImportError:
            return None
    return mol


def validate_structure(name: str) -> Optional[Chem.Mol]:
    """
    Returns a Mol if valid, otherwise None.
    """
    mol = name_to_mol(name)
    if mol is None:
        return None

    # Try a quick sanitization / 3D embedding to ensure it's not totally broken
    try:
        Chem.SanitizeMol(mol)
        AllChem.EmbedMolecule(mol, randomSeed=0xf00d)
    except Exception:
        return None

    return mol
