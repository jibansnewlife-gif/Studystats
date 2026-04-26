document.addEventListener("DOMContentLoaded", () => {
    const ctx = document.getElementById("studyChart");

    if (ctx) {
        const dates = JSON.parse(ctx.dataset.dates);
        const minutes = JSON.parse(ctx.dataset.minutes);

        new Chart(ctx, {
            type: "bar",
            data: {
                labels: dates,
                datasets: [{
                    label: "Minutes Studied",
                    data: minutes
                }]
            }
        });
    }
});

// TIMER
let timer;
let seconds = 0;

function startTimer() {
    clearInterval(timer);
    timer = setInterval(() => {
        seconds++;
        document.getElementById("timerDisplay").innerText =
            Math.floor(seconds / 60) + " min " + (seconds % 60) + " sec";
    }, 1000);
}

function stopTimer() {
    clearInterval(timer);
    document.getElementById("durationInput").value = Math.floor(seconds / 60);
    seconds = 0;
}