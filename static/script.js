// Handle form submission
document.getElementById("submit-button").addEventListener("click", async () => {
    const courseName = document.getElementById("course-name").value;
    const preferredTime = document.getElementById("preferred-time").value;
    const preferredDate = document.getElementById("preferred-date").value;
    // const room = document.getElementById("room").value; // Removed Room field
    const examLength = document.getElementById("exam-length").value;

    // Validate form fields
    if (!courseName || !preferredTime || !preferredDate || !examLength) { // Removed room validation
        alert("Please fill in all fields!");
        return;
    }

    // Log the data being submitted
    console.log("Submitting data:", {
        course_name: courseName,
        preferred_time: preferredTime,
        preferred_date: preferredDate,
        // room: room, // Removed Room field
        exam_length: examLength
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
                // room: room, // Removed Room field
                exam_length: examLength
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const schedule = await response.json();

        // Update text schedule
        const scheduleDiv = document.getElementById("schedule-output");
        scheduleDiv.innerHTML = "<h3>Generated Schedule:</h3>";

        if (schedule.length > 0) {
            scheduleDiv.innerHTML += `
                <table class="schedule-table">
                    <thead>
                        <tr>
                            <th>Course</th>
                            <!-- <th>Room</th> --> <!-- Removed Room column -->
                            <th>Date</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${schedule.map(item => `
                            <tr>
                                <td>${item.course}</td>
                                <!-- <td>${item.room}</td> --> <!-- Removed Room field -->
                                <td>${item.date}</td>
                                <td>${item.time}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        } else {
            scheduleDiv.innerHTML += "<p>No schedule generated yet.</p>";
        }

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

// Add event listener for the "Optimize Schedule" button
document.getElementById("optimize-button").addEventListener("click", async () => {
    try {
        const response = await fetch("/optimize_schedule", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const optimizedSchedule = await response.json();

        // Update optimized schedule similarly
        const scheduleDiv = document.getElementById("schedule-output");
        scheduleDiv.innerHTML = "<h3>Optimized Schedule:</h3>";

        if (optimizedSchedule.length > 0) {
            scheduleDiv.innerHTML += `
                <table class="schedule-table">
                    <thead>
                        <tr>
                            <th>Course</th>
                            <!-- <th>Room</th> --> <!-- Removed Room column -->
                            <th>Date</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${optimizedSchedule.map(item => `
                            <tr>
                                <td>${item.course}</td>
                                <!-- <td>${item.room}</td> --> <!-- Removed Room field -->
                                <td>${item.date}</td>
                                <td>${item.time}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        } else {
            scheduleDiv.innerHTML += "<p>No optimized schedule available.</p>";
        }

        // Refresh calendar
        if (window.calendar) {
            window.calendar.refetchEvents();
        }
    } catch (error) {
        console.error("Error optimizing schedule:", error);
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
                const response = await fetch("/get_schedule");
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const events = await response.json();
                console.log("Raw events from server:", events);

                // Ensure events have required fields
                const formattedEvents = events.map(event => ({
                    title: event.title || "No Title",
                    start: event.start,
                    end: event.end || event.start,  // If end is missing, set to start
                    allDay: event.allDay || false
                }));

                console.log("Formatted events:", formattedEvents);
                successCallback(formattedEvents);
            } catch (error) {
                console.error("Calendar fetch error:", error);
                failureCallback(error);
            }
        },
        height: 'auto',  // Set minimum height for the calendar
    });

    calendar.render();
    window.calendar = calendar;
    console.log("Calendar initialized:", window.calendar !== undefined);
});

// Smooth scrolling for navigation links
document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
