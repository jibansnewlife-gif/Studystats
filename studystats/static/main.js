// NAVIGATION
function showSection(id) {
    document.querySelectorAll(".section").forEach(s => s.style.display = "none");
    document.getElementById(id).style.display = "block";
}

document.addEventListener("DOMContentLoaded", () => {
    showSection("dashboard");

    // Chart
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
    document.getElementById("timerDisplay").innerText = "0 min 0 sec";
}

function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme");

    if (current === "light") {
        document.documentElement.setAttribute("data-theme", "dark");
        localStorage.setItem("theme", "dark");
    } else {
        document.documentElement.setAttribute("data-theme", "light");
        localStorage.setItem("theme", "light");
    }
}