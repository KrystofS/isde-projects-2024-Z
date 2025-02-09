
$(document).ready(function () {
    var scripts = document.getElementById('makeGraph');
    var histogram_values = scripts.getAttribute('histogram_values');
    makeGraph(histogram_values);
});

function makeGraph(values) {
    const data = JSON.parse(values);

    const trace1 = {
        y: data.red,
        mode: 'lines',
        name: 'Red',
        type: 'scatter',
        marker: { color: 'red' },
        hoverinfo: 'skip'
    };

    const trace2 = {
        y: data.green,
        mode: 'lines',
        name: 'Green',
        type: 'scatter',
        marker: { color: 'green' },
        hoverinfo: 'skip'
    };

    const trace3 = {
        y: data.blue,
        mode: 'lines',
        name: 'Blue',
        type: 'scatter',
        marker: { color: 'blue' },
        hoverinfo: 'skip'
    };

    const traces = [trace1, trace2, trace3];

    const config = {
        xaxis: { showticklabels: false },
        yaxis: { showticklabels: false },
        width: 600,
        height: 400,
        showlegend: false
    };

    Plotly.newPlot("hist_graph", traces, config, {displayModeBar: false});
}