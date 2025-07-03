from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel

EffectKey = Literal[
    "nmd",
    "collision",
    "aars",
    "cancer_translation",
    "codon_optimality",
    "frameshift",
    "utr_structure",
    "custom",
]

class AnalyzeRequest(BaseModel):
    gene: str
    fasta: Optional[str] = None
    effects: List[EffectKey]
    cell_type: Optional[str] = None
    treatment: Optional[str] = None
    experimental_conditions: List[str] = []
    hypothesis: Optional[str] = None

class AnalyzeResponse(BaseModel):
    results: Dict[str, Any]
    summary: str
