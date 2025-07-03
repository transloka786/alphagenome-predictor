import os
from alphagenome import AlphaClient
import json

ag = AlphaClient(api_key=os.getenv("ALPHAGENOME_API_KEY"))

async def predict_custom(gene: str, fasta: str | None, params: dict) -> dict:
    """
    Stub for a custom, free-form ChatGPT+AlphaGenome query.
    You might send `params` directly to ChatGPT or AlphaGenome here.
    """
    # TODO: implement custom pipeline
    return {"custom_result": None, "details": "Custom query not yet implemented"}
