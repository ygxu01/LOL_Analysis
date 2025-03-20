let data = [];
let chartInstance = null;  // 存储 Chart.js 实例

// 读取 JSON 数据
fetch("data/matches.json")
    .then(response => response.json())
    .then(jsonData => {
        data = jsonData;

        let variables = Object.keys(data[0]).filter(k => k !== "Team");
        let xSelect = document.getElementById("xVar");
        let ySelect = document.getElementById("yVar");

        // 动态生成 X 轴 和 Y 轴 的选择项
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

        // 默认绘制图表
        updateChart(variables[0], variables[1]);
    });

// **修改 updateChart 以支持销毁旧图表**
function updateChart(xVar, yVar) {
    let ctx = document.getElementById("chart").getContext("2d");
    let labels = data.map(d => d["Team"]);
    let xData = data.map(d => parseFloat(d[xVar])); // 确保数值正确
    let yData = data.map(d => parseFloat(d[yVar]));

    // **如果已有旧图表，先销毁**
    if (chartInstance) {
        chartInstance.destroy();
    }

    // **创建新图表**
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
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { title: { display: true, text: xVar } },
                y: { title: { display: true, text: yVar } }
            }
        }
    });
}

// **监听选择框变化，重新绘制图表**
document.getElementById("xVar").addEventListener("change", function() {
    updateChart(this.value, document.getElementById("yVar").value);
});
document.getElementById("yVar").addEventListener("change", function() {
    updateChart(document.getElementById("xVar").value, this.value);
});
