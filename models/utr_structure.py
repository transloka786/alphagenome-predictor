import os
from alphagenome import AlphaClient

ag = AlphaClient(api_key=os.getenv("ALPHAGENOME_API_KEY"))

async def predict_utr_structure(gene: str, fasta: str | None, params: dict) -> dict:
    """
    Stub for UTR structure & IRES prediction.
    """
    # TODO: call AlphaGenome's utr_structure endpoint
    return {"utr_structures": {}, "details": "UTR structure prediction not yet implemented"}
