// static/main.js
// Handles form submission and displays results

document.getElementById('analysis-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  const form = e.target;

  // Gather form data
  const data = {
    gene: form.gene.value.trim(),
    fasta: form.fasta.value.trim() || undefined,
    effects: Array.from(form.effects.selectedOptions).map(opt => opt.value),
    cell_type: form.cell_type.value.trim() || undefined,
    treatment: form.treatment.value.trim() || undefined,
    experimental_conditions: form.experimental_conditions.value
      .split('\n')
      .map(line => line.trim())
      .filter(line => line),
    hypothesis: form.hypothesis.value.trim() || undefined
  };

  const outputEl = document.getElementById('output');
  outputEl.innerHTML = '<em>Running analysis...</em>';

  try {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const json = await res.json();

    // Escape HTML helper
    const escapeHtml = (unsafe) => {
      return unsafe
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    };

    // Build result HTML
    let html = '<h2>Summary</h2>';
    html += '<pre>' + escapeHtml(json.summary) + '</pre>';
    html += '<h2>Results</h2>';
    html += '<pre>' + escapeHtml(JSON.stringify(json.results, null, 2)) + '</pre>';

    outputEl.innerHTML = html;
  } catch (err) {
    outputEl.innerHTML = `<span style="color:red;">Error: ${err.message}</span>`;
  }
});
