import os
from alphagenome import AlphaClient

ag = AlphaClient(api_key=os.getenv("ALPHAGENOME_API_KEY"))

async def predict_frameshift(gene: str, fasta: str | None, params: dict) -> dict:
    """
    Stub for frameshifting potential prediction.
    """
    # TODO: call AlphaGenome's frameshift endpoint
    return {"frameshift_probabilities": {}, "details": "Frameshift prediction not yet implemented"}
