// Handle form submission
document.getElementById("submit-button").addEventListener("click", async () => {
    const courseName = document.getElementById("course-name").value;
    const preferredTime = document.getElementById("preferred-time").value;
    const preferredDate = document.getElementById("preferred-date").value;
    const room = document.getElementById("room").value;

    // Validate form fields
    if (!courseName || !preferredTime || !preferredDate || !room) {
        alert("Please fill in all fields!");
        return;
    }

    // Log the data being submitted
    console.log("Submitting data:", {
        course_name: courseName,
        preferred_time: preferredTime,
        preferred_date: preferredDate,
        room: room,
    });

    try {
        const response = await fetch("/generate_schedule", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                course_name: courseName,
                preferred_time: preferredTime,
                preferred_date: preferredDate,
                room: room,
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const schedule = await response.json();

        // Update text schedule
        const scheduleDiv = document.getElementById("schedule-output");
        scheduleDiv.innerHTML = "<h3>Generated Schedule:</h3>";
        schedule.forEach((item) => {
            scheduleDiv.innerHTML += `<p>${item.course} in ${item.room} on ${item.date} at ${item.time}</p>`;
        });

        // Refresh calendar
        console.log("Refreshing calendar...");
        if (window.calendar) {
            window.calendar.refetchEvents();
            // Optional: Navigate to the date of the newly added event
            window.calendar.gotoDate(schedule[0].date); // Assumes schedule[0] is the latest
        } else {
            console.error("Calendar not initialized!");
        }

        // Clear form
        document.getElementById("professor-form").reset();
    } catch (error) {
        console.error("Error generating schedule:", error);
    }
});

// Initialize FullCalendar
document.addEventListener("DOMContentLoaded", function () {
    const calendarEl = document.getElementById("calendar");

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "timeGridWeek",
        initialDate: new Date().toISOString().split('T')[0],  // Set initial date to today
        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "dayGridMonth,timeGridWeek,timeGridDay"
        },
        slotMinTime: "08:00:00",
        slotMaxTime: "20:00:00",
        timeZone: 'local',  // Align with server's timezone
        events: async function (fetchInfo, successCallback, failureCallback) {
            try {
                console.log("Fetching calendar events...");
                const response = await fetch("/generate_schedule");
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const events = await response.json();
                console.log("Raw events from server:", events);

                // Format events for FullCalendar
                const formattedEvents = events.map(event => ({
                    title: event.title,
                    start: event.start,
                    end: event.end,
                    allDay: event.allDay
                }));

                console.log("Formatted events:", formattedEvents);
                successCallback(formattedEvents);
            } catch (error) {
                console.error("Calendar fetch error:", error);
                failureCallback(error);
            }
        }
    });

    calendar.render();
    window.calendar = calendar;
    console.log("Calendar initialized:", window.calendar !== undefined);
});
