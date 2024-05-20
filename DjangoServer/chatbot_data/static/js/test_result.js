function displayResults(data) {
    const intentResults = data.intent_evaluation;

    // Create a table for the intent predictions
    let intentTable = `
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

        intentResults.predictions.forEach(prediction => {
            intentTable += `
            <tr>
                <td>${prediction.text}</td>
                <td>${prediction.intent}</td>
                <td>${prediction.predicted}</td>
                <td>${prediction.confidence.toFixed(2)}</td>
            </tr>`;
    });

    intentTable += `
            </tbody>
        </table>`;

    // Create a summary report table
    let intentReportTable = `
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

        for (const [intent, metrics] of Object.entries(intentResults.report)) {
            if (intent !== 'accuracy' && intent !== 'macro avg' && intent !== 'weighted avg' && intent !== 'micro avg') {
                intentReportTable += `
                <tr>
                    <td>${intent}</td>
                    <td>${metrics.precision.toFixed(2)}</td>
                    <td>${metrics.recall.toFixed(2)}</td>
                    <td>${metrics['f1-score'].toFixed(2)}</td>
                    <td>${metrics.support}</td>
                </tr>`;
        }
    }

    intentReportTable += `
            </tbody>
        </table>`;

    // Create a summary statistics table for intents
    let intentSummaryTable = `
        <h3>Summary Statistics (Intents)</h3>
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
                    <td>${intentResults.precision.toFixed(2)}</td>
                </tr>
                <tr>
                    <td>F1-Score</td>
                    <td>${intentResults.f1_score.toFixed(2)}</td>
                </tr>
                <tr>
                    <td>Accuracy</td>
                    <td>${intentResults.accuracy.toFixed(2)}</td>
                </tr>
            </tbody>
        </table>`;
        // Create a table for intent errors
    let intentErrorsTable = `
    <h3>Intent Errors</h3>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Text</th>
                <th>Predicted Intent</th>
                <th>Actual Intent</th>
            </tr>
        </thead>
        <tbody>`;

intentResults.errors.forEach(error => {
    intentErrorsTable += `
        <tr>
            <td>${error.text}</td>
            <td>${error.predicted_intent}</td>
            <td>${error.intent}</td>
        </tr>`;
});

intentErrorsTable += `
        </tbody>
    </table>`;

    // Create a canvas for the confusion matrix chart
    let intentChartCanvas = `
        <h3>Confusion Matrix</h3>
        <canvas id="confusionMatrixChart"></canvas>`;

    $('#result').html(intentTable + intentReportTable + intentSummaryTable + intentErrorsTable + intentChartCanvas);

    // Create the confusion matrix chart for intents
    const ctx = document.getElementById('confusionMatrixChart').getContext('2d');
    const labels = Object.keys(intentResults.report).filter(intent => intent !== 'accuracy' && intent !== 'macro avg' && intent !== 'weighted avg' && intent !== 'micro avg');
    const dataMatrix = labels.map(intent => labels.map(label => intentResults.report[intent].confused_with[label] || 0));

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
    const entityResults = data.entity_evaluation.DIETClassifier;

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

    entityResults.errors.forEach(error => {
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

    // Create a summary report table for entities
    let entityReportTable = `
        <h3>Summary Report (Entities)</h3>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Entity</th>
                    <th>Precision</th>
                    <th>Recall</th>
                    <th>F1-Score</th>
                    <th>Support</th>
                </tr>
            </thead>
            <tbody>`;

    for (const [entity, metrics] of Object.entries(entityResults.report)) {
        if (entity !== 'accuracy' && entity !== 'macro avg' && entity !== 'weighted avg' && entity !== 'micro avg') {
            entityReportTable += `
                <tr>
                    <td>${entity}</td>
                    <td>${metrics.precision.toFixed(2)}</td>
                    <td>${metrics.recall.toFixed(2)}</td>
                    <td>${metrics['f1-score'].toFixed(2)}</td>
                    <td>${metrics.support}</td>
                </tr>`;
        }
    }

    entityReportTable += `
            </tbody>
        </table>`;

    // Create a summary statistics table for entities
    let entitySummaryTable = `
        <h3>Summary Statistics (Entities)</h3>
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
                    <td>${entityResults.precision.toFixed(2)}</td>
                </tr>
                <tr>
                    <td>F1-Score</td>
                    <td>${entityResults.f1_score.toFixed(2)}</td>
                </tr>
                <tr>
                    <td>Accuracy</td>
                    <td>${entityResults.accuracy.toFixed(2)}</td>
                </tr>
            </tbody>
        </table>`;

    // Create a canvas for the confusion matrix chart for entities
    let entityChartCanvas = `
        <h3>Entity Confusion Matrix</h3>
        <canvas id="entityConfusionMatrixChart"></canvas>`;

    $('#entityResult').html(entityTable + entityReportTable + entitySummaryTable + entityChartCanvas);

    // Create the confusion matrix chart for entities
    const entityCtx = document.getElementById('entityConfusionMatrixChart').getContext('2d');
    const entityLabels = Object.keys(entityResults.report).filter(entity => entity !== 'accuracy' && entity !== 'macro avg' && entity !== 'weighted avg' && entity !== 'micro avg');
    const entityDataMatrix = entityLabels.map(entity => entityLabels.map(label => entityResults.report[entity].confused_with[label] || 0));

    new Chart(entityCtx, {
        type: 'bar',
        data: {
            labels: entityLabels,
            datasets: entityLabels.map((label, i) => ({
                label: label,
                data: entityDataMatrix[i],
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
