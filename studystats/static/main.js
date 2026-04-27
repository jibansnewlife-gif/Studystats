// -----------------------------
// NAVIGATION
// -----------------------------

// REMOVED: alert("JS LOADED") — this was blocking and annoying

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

    // Theme
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

    // FIX: Request notification permission early on page load,
    // so it's already granted when reminders are triggered.
    if ("Notification" in window && Notification.permission === "default") {
        Notification.requestPermission().then(p => {
            console.log("Notification permission on load:", p);
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
// IN-APP ALERT (RELIABLE)
// -----------------------------
function showInAppAlert(message) {
    const container = document.getElementById("alerts");
    if (!container) return;

    const div = document.createElement("div");
    div.className = "card";
    div.style.borderLeft = "4px solid orange";
    div.style.marginBottom = "10px";
    div.innerText = message;

    container.appendChild(div);
}


// -----------------------------
// NOTIFICATION CORE
// FIX: now returns a Promise so callers can await it
// -----------------------------
async function sendNotification(title, body) {
    console.log("🔔 Attempting notification:", title);

    if (!("Notification" in window)) {
        console.log("❌ Notifications not supported in this browser");
        return;
    }

    // FIX: If permission isn't granted yet, request it now and wait
    if (Notification.permission !== "granted") {
        const permission = await Notification.requestPermission();
        if (permission !== "granted") {
            console.log("❌ Permission denied");
            return;
        }
    }

    try {
        new Notification(title, { body: body });
        console.log("✅ Notification sent:", title);
    } catch (e) {
        console.log("❌ Notification error:", e);
        // FIX: On some browsers/OS combos, Notification constructor throws.
        // Fall back to in-app alert.
        showInAppAlert(`🔔 ${title}: ${body}`);
    }
}


// -----------------------------
// REMINDERS (MAIN LOGIC)
// FIX: made async so sendNotification awaits properly
// -----------------------------
async function checkReminders() {
    console.log("🔍 checkReminders triggered");

    const todayMinutes = window.todayMinutes || 0;
    const streak = window.streak || 0;

    console.log("todayMinutes:", todayMinutes);
    console.log("streak:", streak);

    // Always show in-app alerts (reliable fallback)
    if (todayMinutes === 0) {
        showInAppAlert("⚠️ You haven't studied today");
    }

    if (streak >= 3 && todayMinutes === 0) {
        showInAppAlert("🔥 Your streak is at risk!");
    }

    // FIX: await each notification so they fire in order
    if (!("Notification" in window)) {
        console.log("❌ This browser doesn't support notifications");
        return;
    }

    if (todayMinutes === 0) {
        await sendNotification("📚 Study Reminder", "You haven't studied today!");
    }

    if (streak >= 3 && todayMinutes === 0) {
        await sendNotification("🔥 Streak Alert", "Your streak is at risk!");
    }

    if (todayMinutes > 0 && streak > 0) {
        await sendNotification("✅ Good job!", `You've studied ${todayMinutes} min today.`);
    }
}


// -----------------------------
// TEST BUTTON
// FIX: also made async, awaits sendNotification
// -----------------------------
async function testNotification() {
    console.log("🧪 testNotification clicked");
    await sendNotification("🧪 Test Notification", "If you see this, it works!");
}

console.log("JS loaded ✅");