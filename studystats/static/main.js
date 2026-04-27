// -----------------------------
// NAVIGATION
// -----------------------------
function showSection(id) {
    document.querySelectorAll(".section").forEach(s => s.style.display = "none");
    document.getElementById(id).style.display = "block";

    document.querySelectorAll(".sidebar button").forEach(btn => {
        btn.classList.remove("active");
    });

    document.querySelector(`[onclick="showSection('${id}')"]`)?.classList.add("active");
}

// -----------------------------
// ON LOAD
// -----------------------------
document.addEventListener("DOMContentLoaded", () => {
    showSection("dashboard");

    // Load saved theme
    const savedTheme = localStorage.getItem("theme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);

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
                    data: minutes,
                    backgroundColor: getComputedStyle(document.documentElement)
                        .getPropertyValue('--accent')
                }]
            }
        });
    }
});


// -----------------------------
// TIMER
// -----------------------------
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


// -----------------------------
// THEME TOGGLE
// -----------------------------
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


// -----------------------------
// NOTIFICATION CORE (FIXED)
// -----------------------------
function sendNotification(title, body) {
    if (Notification.permission !== "granted") return;

    // Try service worker (better)
    if ("serviceWorker" in navigator) {
        navigator.serviceWorker.getRegistration().then(reg => {
            if (reg) {
                reg.showNotification(title, { body: body });
            } else {
                // fallback
                new Notification(title, { body: body });
            }
        });
    } else {
        // fallback
        new Notification(title, { body: body });
    }
}


// -----------------------------
// REMINDERS
// -----------------------------
function checkReminders() {
    const todayMinutes = window.todayMinutes || 0;
    const streak = window.streak || 0;

    Notification.requestPermission().then(permission => {
        if (permission !== "granted") return;

        if (todayMinutes === 0) {
            sendNotification("📚 Study Reminder", "You haven't studied today!");
        }

        if (streak >= 3 && todayMinutes === 0) {
            sendNotification("🔥 Streak Alert", "Your streak is at risk!");
        }
    });
}


// -----------------------------
// TEST BUTTON
// -----------------------------
function testNotification() {
    Notification.requestPermission().then(permission => {
        if (permission !== "granted") return;

        sendNotification("🧪 Test Notification", "Notifications are working!");
    });
}