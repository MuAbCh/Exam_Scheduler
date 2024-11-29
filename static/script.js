document.getElementById("generate-btn").addEventListener("click", async () => {
    const response = await fetch("/generate_schedule");
    const schedule = await response.json();

    const scheduleDiv = document.getElementById("schedule");
    scheduleDiv.innerHTML = "<h2>Optimized Schedule</h2>";
    schedule.forEach(item => {
        scheduleDiv.innerHTML += `<p>${item.course} in ${item.room} at ${item.time}</p>`;
    });
});
