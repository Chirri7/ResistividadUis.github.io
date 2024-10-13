document.getElementById('calculo').addEventListener('change', function () {
    const seleccion = this.value;
    const inputsDiv = document.getElementById('inputs');

    inputsDiv.innerHTML = '';

    if (seleccion === 'resistencia') {
        inputsDiv.innerHTML = `
            <label for="resistivity">Resistividad (ρ):</label>
            <input type="number" id="resistivity" name="resistivity" step="any" required>
            <label for="length">Longitud (L):</label>
            <input type="number" id="length" name="length" step="any" required>
            <label for="area">Área (A):</label>
            <input type="number" id="area" name="area" step="any" required>
        `;
    } else if (seleccion === 'resistividad') {
        inputsDiv.innerHTML = `
            <label for="resistance">Resistencia (R):</label>
            <input type="number" id="resistance" name="resistance" step="any" required>
            <label for="length">Longitud (L):</label>
            <input type="number" id="length" name="length" step="any" required>
            <label for="area">Área (A):</label>
            <input type="number" id="area" name="area" step="any" required>
        `;
    } else if (seleccion === 'longitud') {
        inputsDiv.innerHTML = `
            <label for="resistance">Resistencia (R):</label>
            <input type="number" id="resistance" name="resistance" step="any" required>
            <label for="resistivity">Resistividad (ρ):</label>
            <input type="number" id="resistivity" name="resistivity" step="any" required>
            <label for="area">Área (A):</label>
            <input type="number" id="area" name="area" step="any" required>
        `;
    } else if (seleccion === 'area') {
        inputsDiv.innerHTML = `
            <label for="resistance">Resistencia (R):</label>
            <input type="number" id="resistance" name="resistance" step="any" required>
            <label for="resistivity">Resistividad (ρ):</label>
            <input type="number" id="resistivity" name="resistivity" step="any" required>
            <label for="length">Longitud (L):</label>
            <input type="number" id="length" name="length" step="any" required>
        `;
    }
});

document.getElementById('resistivityForm').addEventListener('submit', function (event) {
    event.preventDefault();

    let resistance, resistivity, length, area;
    const calculo = document.getElementById('calculo').value;
    const feedback = document.getElementById('feedbackTexto');
    const suggestion = document.getElementById('sugerenciaTexto');
    feedback.innerHTML = '';
    suggestion.innerHTML = '';

    if (calculo === 'resistencia') {
        resistivity = parseFloat(document.getElementById('resistivity').value);
        length = parseFloat(document.getElementById('length').value);
        area = parseFloat(document.getElementById('area').value);

        resistance = resistivity * (length / area);
        document.getElementById('resultadoTexto').innerHTML = `Resistencia: ${resistance.toExponential(2)} ohms`;

        feedback.innerHTML = 'La resistencia determina qué tan difícil es para la corriente fluir a través de un material.';
        
        if (resistance > 1e6) {
            suggestion.innerHTML = 'El valor de resistencia es alto. Esto indica un aislante fuerte.';
        } else if (resistance < 1) {
            suggestion.innerHTML = 'El valor de resistencia es muy bajo, lo que sugiere un buen conductor.';
        }

    } else if (calculo === 'resistividad') {
        resistance = parseFloat(document.getElementById('resistance').value);
        length = parseFloat(document.getElementById('length').value);
        area = parseFloat(document.getElementById('area').value);

        resistivity = (resistance * area) / length;
        document.getElementById('resultadoTexto').innerHTML = `Resistividad: ${resistivity.toExponential(2)} ohms*m`;

        feedback.innerHTML = 'La resistividad describe la capacidad intrínseca de un material para resistir el flujo de corriente.';
        
        if (resistivity > 1e-3) {
            suggestion.innerHTML = 'Este valor sugiere un material con alta resistividad, como un aislante.';
        } else if (resistivity < 1e-6) {
            suggestion.innerHTML = 'Este valor sugiere un material muy buen conductor, como el cobre o la plata.';
        }

    } else if (calculo === 'longitud') {
        resistance = parseFloat(document.getElementById('resistance').value);
        resistivity = parseFloat(document.getElementById('resistivity').value);
        area = parseFloat(document.getElementById('area').value);

        length = (resistance * area) / resistivity;
        document.getElementById('resultadoTexto').innerHTML = `Longitud: ${length.toExponential(2)} m`;

        feedback.innerHTML = 'La longitud afecta directamente la resistencia total de un material conductor.';

    } else if (calculo === 'area') {
        resistance = parseFloat(document.getElementById('resistance').value);
        resistivity = parseFloat(document.getElementById('resistivity').value);
        length = parseFloat(document.getElementById('length').value);

        area = (resistivity * length) / resistance;
        document.getElementById('resultadoTexto').innerHTML = `Área: ${area.toExponential(2)} m²`;

        feedback.innerHTML = 'El área transversal afecta la facilidad con la que la corriente puede fluir.';
        
        if (area > 1) {
            suggestion.innerHTML = 'Mayor área significa menor resistencia, lo que indica un mejor conductor.';
        } else if (area < 0.01) {
            suggestion.innerHTML = 'Área muy pequeña, lo que aumenta la resistencia significativamente.';
        }
    }
});