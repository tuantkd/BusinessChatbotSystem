function displayResults(data) {
    const results = data.intent_evaluation;

    // Create a table for the intent predictions
    let table = `
        <h3>Intent Predictions</h3>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Text</th>
                    <th>Intent</th>
                    <th>Predicted</th>
                    <th>Confidence</th>
                </tr>
            </thead>
            <tbody>`;

    results.predictions.forEach(prediction => {
        table += `
            <tr>
                <td>${prediction.text}</td>
                <td>${prediction.intent}</td>
                <td>${prediction.predicted}</td>
                <td>${prediction.confidence.toFixed(2)}</td>
            </tr>`;
    });

    table += `
            </tbody>
        </table>`;

    // Create a summary report table
    let reportTable = `
        <h3>Summary Report</h3>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Intent</th>
                    <th>Precision</th>
                    <th>Recall</th>
                    <th>F1-Score</th>
                    <th>Support</th>
                </tr>
            </thead>
            <tbody>`;

    for (const [intent, metrics] of Object.entries(results.report)) {
        if (intent !== 'accuracy' && intent !== 'macro avg' && intent !== 'weighted avg' && intent !== 'micro avg') {
            reportTable += `
                <tr>
                    <td>${intent}</td>
                    <td>${metrics.precision.toFixed(2)}</td>
                    <td>${metrics.recall.toFixed(2)}</td>
                    <td>${metrics['f1-score'].toFixed(2)}</td>
                    <td>${metrics.support}</td>
                </tr>`;
        }
    }

    reportTable += `
            </tbody>
        </table>`;

    // Create a summary statistics table
    let summaryTable = `
        <h3>Summary Statistics</h3>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Precision</td>
                    <td>${results.precision.toFixed(2)}</td>
                </tr>
                <tr>
                    <td>F1-Score</td>
                    <td>${results.f1_score.toFixed(2)}</td>
                </tr>
                <tr>
                    <td>Accuracy</td>
                    <td>${results.accuracy.toFixed(2)}</td>
                </tr>
            </tbody>
        </table>`;

    // Create a canvas for the confusion matrix chart
    let chartCanvas = `
        <h3>Confusion Matrix</h3>
        <canvas id="confusionMatrixChart"></canvas>`;

    $('#result').html(table + reportTable + summaryTable + chartCanvas);

    // Create the confusion matrix chart
    const ctx = document.getElementById('confusionMatrixChart').getContext('2d');
    const labels = Object.keys(results.report).filter(intent => intent !== 'accuracy' && intent !== 'macro avg' && intent !== 'weighted avg' && intent !== 'micro avg');
    const dataMatrix = labels.map(intent => labels.map(label => results.report[intent].confused_with[label] || 0));

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: labels.map((label, i) => ({
                label: label,
                data: dataMatrix[i],
                backgroundColor: `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.5)`,
                borderColor: `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 1)`,
                borderWidth: 1
            }))
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    stacked: true
                },
                y: {
                    stacked: true
                }
            }
        }
    });
}

// Function to handle the display of entity evaluation
function displayEntityResults(data) {
    const results = data.entity_evaluation;

    // Create a table for the entity errors
    let entityTable = `
        <h3>Entity Errors</h3>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Text</th>
                    <th>Entities</th>
                    <th>Predicted Entities</th>
                </tr>
            </thead>
            <tbody>`;

    results.DIETClassifier.errors.forEach(error => {
        let entities = error.entities.map(entity => `${entity.entity}: ${entity.value}`).join('<br>');
        let predictedEntities = error.predicted_entities.map(entity => `${entity.entity}: ${entity.value}`).join('<br>');

        entityTable += `
            <tr>
                <td>${error.text}</td>
                <td>${entities}</td>
                <td>${predictedEntities}</td>
            </tr>`;
    });

    entityTable += `
            </tbody>
        </table>`;

    $('#entityResult').html(entityTable);
}
