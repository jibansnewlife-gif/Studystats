// Weekly Study Chart

document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('studyChart');

    if (!ctx) return;

    const dates = JSON.parse(ctx.dataset.dates);
    const minutes = JSON.parse(ctx.dataset.minutes);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dates,
            datasets: [{
                label: 'Minutes Studied',
                data: minutes,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: "white"
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: "white"
                    }
                },
                y: {
                    ticks: {
                        color: "white"
                    }
                }
            }
        }
    });
});