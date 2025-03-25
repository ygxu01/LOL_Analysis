chartInstance = new Chart(ctx, {
    type: "scatter",
    data: {
        labels: labels,
        datasets: [{
            label: `${yVar} vs. ${xVar}`,
            data: xData.map((x, i) => ({ x, y: yData[i] })),
            backgroundColor: "blue",
            pointRadius: 5
        }]
    },
    options: {
        responsive: false,  // Disable auto resizing
        maintainAspectRatio: false, // Ensure chart uses full width/height
        scales: {
            x: { title: { display: true, text: xVar } },
            y: { title: { display: true, text: yVar } }
        }
    }
});
