import os
from alphagenome import AlphaClient

ag = AlphaClient(api_key=os.getenv("ALPHAGENOME_API_KEY"))

async def predict_collision(gene: str, fasta: str | None, params: dict) -> dict:
    """
    Stub for ribosome collision/stalling prediction.
    """
    # TODO: call AlphaGenome's collision endpoint
    return {"collision_sites": [], "details": "Collision prediction not yet implemented"}
