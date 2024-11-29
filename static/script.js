document.getElementById("submit-button").addEventListener("click", async () => {
    const courseName = document.getElementById("course-name").value;
    const preferredTime = document.getElementById("preferred-time").value;
    const room = document.getElementById("room").value;

    // Check for valid input
    if (!courseName || !preferredTime || !room) {
        alert("Please fill in all fields!");
        return;
    }

    try {
        // Send the data to the backend via POST request
        const response = await fetch("/generate_schedule", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                course_name: courseName,
                preferred_time: preferredTime,
                room: room,
            }),
        });

        // Handle the response from the backend
        const schedule = await response.json();
        const scheduleDiv = document.getElementById("schedule-output");
        scheduleDiv.innerHTML = "<h3>Generated Schedule:</h3>";
        schedule.forEach((item) => {
            scheduleDiv.innerHTML += `<p>${item.course} in ${item.room} at ${item.time}</p>`;
        });
    } catch (error) {
        console.error("Error generating schedule:", error);
    }
});
