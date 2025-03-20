let data = [];

// 读取 JSON 数据
fetch("data/matches.json")
    .then(response => response.json())
    .then(jsonData => {
        data = jsonData;

        let variables = Object.keys(data[0]).filter(k => k !== "Team");
        let xSelect = document.getElementById("xVar");
        let ySelect = document.getElementById("yVar");

        variables.forEach(v => {
            let optionX = document.createElement("option");
            optionX.value = v;
            optionX.textContent = v;
            xSelect.appendChild(optionX);

            let optionY = document.createElement("option");
            optionY.value = v;
            optionY.textContent = v;
            ySelect.appendChild(optionY);
        });

        updateChart(variables[0], variables[1]);
    });

function updateChart(xVar, yVar) {
    let ctx = document.getElementById("chart").getContext("2d");
    let labels = data.map(d => d["Team"]);
    let xData = data.map(d => d[xVar]);
    let yData = data.map(d => d[yVar]);

    new Chart(ctx, {
        type: "scatter",
        data: {
            labels: labels,
            datasets: [{
                label: `${yVar} vs. ${xVar}`,
                data: xData.map((x, i) => ({x, y: yData[i]})),
                backgroundColor: "blue",
                pointRadius: 5
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: xVar } },
                y: { title: { display: true, text: yVar } }
            }
        }
    });
}

// 监听选择框
document.getElementById("xVar").addEventListener("change", function() {
    updateChart(this.value, document.getElementById("yVar").value);
});
document.getElementById("yVar").addEventListener("change", function() {
    updateChart(document.getElementById("xVar").value, this.value);
});
