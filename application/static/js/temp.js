$(document).ready(function () {
    const config = {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: "T1",
                backgroundColor: 'rgb(211, 94, 96)',
                borderColor: 'rgb(255, 99, 132)',
                data: [],
                fill: false,
            }],
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Temperature Sensor Response'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
                yAxes: [{
                    ticks: {
                        suggestedMin: 10,
                        suggestedMax: 40
                    },
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Temperature (celcius)'
                    }
                }]
            }
        }
    };
    const context = document.getElementById('canvas').getContext('2d');
    const lineChart = new Chart(context, config);
    const source = new EventSource("/temp_sensor_data");
    source.onmessage = function (event) {
        const data = JSON.parse(event.data);
        if (config.data.labels.length === 20) {
            config.data.labels.shift();
            config.data.datasets[0].data.shift();
        }
        config.data.labels.push(data.time);
        config.data.datasets[0].data.push(data.value);
        lineChart.update();
    }
});
