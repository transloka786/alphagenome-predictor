import os
from alphagenome import AlphaClient

ag = AlphaClient(api_key=os.getenv("ALPHAGENOME_API_KEY"))

async def predict_aars(gene: str, fasta: str | None, params: dict) -> dict:
    """
    Stub for aa-tRNA synthetase mutation effect prediction.
    """
    # TODO: call AlphaGenome's aaRS endpoint
    return {"aars_effects": {}, "details": "aaRS prediction not yet implemented"}
