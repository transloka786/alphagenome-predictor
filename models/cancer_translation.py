import os
from alphagenome import AlphaClient

ag = AlphaClient(api_key=os.getenv("ALPHAGENOME_API_KEY"))

async def predict_cancer_translation(gene: str, fasta: str | None, params: dict) -> dict:
    """
    Stub for cancer-gene translation (e.g. p53) effects.
    """
    # TODO: call AlphaGenome's cancer_translation endpoint
    return {"translation_changes": {}, "details": "Cancer translation prediction not yet implemented"}
