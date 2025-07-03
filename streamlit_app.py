import os
import json
import streamlit as st
import openai
from alphagenome import AlphaClient
from schemas import AnalyzeRequest

# Initialize clients
openai.api_key = os.getenv('OPENAI_API_KEY')
ag = AlphaClient(api_key=os.getenv('ALPHAGENOME_API_KEY'))

# Page config
st.set_page_config(page_title='AlphaGenome Analysis', layout='wide')

st.title('AlphaGenome Analysis')

# --- Input Form ---
with st.form(key='analysis_form'):
    gene = st.text_input('Gene name', value='', help='e.g. TP53')
    fasta = st.text_area('FASTA sequence (optional)', height=100,
                         help='Paste a FASTA header and sequence')

    effects = st.multiselect(
        'Select analysis modules',
        options=[
            'nmd', 'collision', 'aars', 'cancer_translation',
            'codon_optimality', 'frameshift', 'utr_structure', 'custom'
        ],
        default=['nmd']
    )
    cell_type = st.text_input('Cell type', help='e.g. HeLa')
    treatment = st.text_input('Treatment', help='e.g. cisplatin 10 μM for 24h')
    experimental_conditions = st.text_area(
        'Experimental conditions (one per line)', height=80
    )
    hypothesis = st.text_area('Hypothesis / Notes', height=80)

    submitted = st.form_submit_button('Run Analysis')

# --- On Submit ---
if submitted:
    # Prepare request schema
    conditions = [c.strip() for c in experimental_conditions.split('\n') if c.strip()]
    req_data = AnalyzeRequest(
        gene=gene,
        fasta=fasta or None,
        effects=effects,
        cell_type=cell_type or None,
        treatment=treatment or None,
        experimental_conditions=conditions,
        hypothesis=hypothesis or None
    )

    # Display spinner
    with st.spinner('Running analysis...'):
        # 1) Parse free-text via ChatGPT
        parse_prompt = (
            f"Extract structured params:\n"
            f"cell_type: {req_data.cell_type}\n"
            f"treatment: {req_data.treatment}\n"
            f"experimental_conditions: {req_data.experimental_conditions}\n"
            f"hypothesis: {req_data.hypothesis}\n"
            "Return JSON."
        )
        parse_resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': parse_prompt}]
        )
        parsed = json.loads(parse_resp.choices[0].message.content)

        # 2) Call selected model stubs
        results = {}
        for eff in req_data.effects:
            if eff == 'nmd':
                results['nmd'] = st.experimental_singleton(predict_nmd)(
                    req_data.gene, req_data.fasta, parsed
                )
            elif eff == 'collision':
                results['collision'] = st.experimental_singleton(predict_collision)(
                    req_data.gene, req_data.fasta, parsed
                )
            elif eff == 'aars':
                results['aars'] = st.experimental_singleton(predict_aars)(
                    req_data.gene, req_data.fasta, parsed
                )
            elif eff == 'cancer_translation':
                results['cancer_translation'] = st.experimental_singleton(predict_cancer_translation)(
                    req_data.gene, req_data.fasta, parsed
                )
            elif eff == 'codon_optimality':
                results['codon_optimality'] = st.experimental_singleton(predict_codon_optimality)(
                    req_data.gene, req_data.fasta, parsed
                )
            elif eff == 'frameshift':
                results['frameshift'] = st.experimental_singleton(predict_frameshift)(
                    req_data.gene, req_data.fasta, parsed
                )
            elif eff == 'utr_structure':
                results['utr_structure'] = st.experimental_singleton(predict_utr_structure)(
                    req_data.gene, req_data.fasta, parsed
                )
            elif eff == 'custom':
                results['custom'] = st.experimental_singleton(predict_custom)(
                    req_data.gene, req_data.fasta, parsed
                )

        # 3) Summarize with ChatGPT
        summary_prompt = (
            f"Raw results:\n{json.dumps(results, indent=2)}\n"
            "Summarize findings and suggest next steps."
        )
        summary_resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': summary_prompt}]
        )
        summary = summary_resp.choices[0].message.content

    # --- Display Outputs ---
    st.header('Summary')
    st.write(summary)

    st.header('Detailed Results')
    st.json(results)
