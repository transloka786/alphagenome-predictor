import os
from alphagenome import AlphaClient

ag = AlphaClient(api_key=os.getenv("ALPHAGENOME_API_KEY"))

async def predict_nmd(gene: str, fasta: str | None, params: dict) -> dict:
    """
    Stub for NMD prediction.
    Replace the body with:
      return ag.predict_nmd(gene=gene, fasta=fasta, **params)
    """
    # TODO: call AlphaGenome's NMD endpoint
    return {"nmd_score": None, "details": "NMD prediction not yet implemented"}
