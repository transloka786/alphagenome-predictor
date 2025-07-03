import os
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import openai
from alphagenome import AlphaClient

from schemas import AnalyzeRequest, AnalyzeResponse
from models.nmd import predict_nmd
from models.collision import predict_collision
from models.aars import predict_aars
from models.cancer_translation import predict_cancer_translation
from models.codon_optimality import predict_codon_optimality
from models.frameshift import predict_frameshift
from models.utr_structure import predict_utr_structure
from models.custom import predict_custom

# load keys from env
openai.api_key = os.getenv("OPENAI_API_KEY")
ag = AlphaClient(api_key=os.getenv("ALPHAGENOME_API_KEY"))

app = FastAPI()
# serve static/
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_ui():
    with open("static/index.html", "r") as f:
        return f.read()

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    # 1) parse the free‐text parts into structured params
    parse_prompt = (
        f"Extract structured parameters for analysis:\n"
        f"cell_type: {req.cell_type}\n"
        f"treatment: {req.treatment}\n"
        f"experimental_conditions: {req.experimental_conditions}\n"
        f"hypothesis: {req.hypothesis}\n\n"
        f"Return a JSON object."
    )
    parse_resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": parse_prompt}]
    )
    parsed = json.loads(parse_resp.choices[0].message.content)

    # 2) run each requested module
    results = {}
    for eff in req.effects:
        if eff == "nmd":
            results["nmd"] = await predict_nmd(req.gene, req.fasta, parsed)
        elif eff == "collision":
            results["collision"] = await predict_collision(req.gene, req.fasta, parsed)
        elif eff == "aars":
            results["aars"] = await predict_aars(req.gene, req.fasta, parsed)
        elif eff == "cancer_translation":
            results["cancer_translation"] = await predict_cancer_translation(req.gene, req.fasta, parsed)
        elif eff == "codon_optimality":
            results["codon_optimality"] = await predict_codon_optimality(req.gene, req.fasta, parsed)
        elif eff == "frameshift":
            results["frameshift"] = await predict_frameshift(req.gene, req.fasta, parsed)
        elif eff == "utr_structure":
            results["utr_structure"] = await predict_utr_structure(req.gene, req.fasta, parsed)
        elif eff == "custom":
            results["custom"] = await predict_custom(req.gene, req.fasta, parsed)

    # 3) summarize all outputs
    summary_prompt = (
        f"Here are the raw analysis results:\n{json.dumps(results, indent=2)}\n\n"
        "Please summarize the key findings and suggest next experimental or computational steps."
    )
    summary_resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": summary_prompt}]
    )
    summary = summary_resp.choices[0].message.content

    return AnalyzeResponse(results=results, summary=summary)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
