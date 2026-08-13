const API_BASE_URL = "";


async function reconcile() {

    const driverId =
        document.getElementById("driverId").value;

    const summaryDate =
        document.getElementById("summaryDate").value;

    const errorMessage =
        document.getElementById("errorMessage");

    const resultCard =
        document.getElementById("resultCard");

    const exceptionCard =
        document.getElementById("exceptionCard");

    errorMessage.textContent = "";

    resultCard.classList.add("hidden");
    exceptionCard.classList.add("hidden");

    if (!driverId || !summaryDate) {

        errorMessage.textContent =
            "Please enter both driver ID and date.";

        return;
    }

    try {

        const response = await fetch(
            `${API_BASE_URL}/reconcile/${driverId}/${summaryDate}`,
            {
                method: "POST"
            }
        );

        if (!response.ok) {

            const errorData = await response.json();

            throw new Error(
                errorData.detail || "Reconciliation failed."
            );
        }

        const data = await response.json();

        displayResult(data);

        await loadExceptions(
            driverId,
            summaryDate
        );

    } catch (error) {

        errorMessage.textContent =
            error.message;

    }
}


function displayResult(data) {

    document.getElementById("summaryId").textContent =
        data.id;

    document.getElementById("resultDriverId").textContent =
        data.driver_id;

    document.getElementById("resultDate").textContent =
        data.summary_date;

    document.getElementById("hoursOnDuty").textContent =
        data.hours_on_duty ?? "-";

    document.getElementById("tripsCompleted").textContent =
        data.trips_completed ?? "-";

    document.getElementById("distanceKm").textContent =
        data.distance_km !== null
            ? `${data.distance_km} km`
            : "-";

    const statusElement =
        document.getElementById("status");

    statusElement.textContent =
        data.status;

    statusElement.className = "";

    if (data.status === "RESOLVED") {

        statusElement.style.color = "green";

    } else if (
        data.status === "RESOLVED_WITH_FLAGS"
    ) {

        statusElement.style.color = "orange";

    } else if (
        data.status === "REVIEW_REQUIRED"
    ) {

        statusElement.style.color = "red";
    }

    document
        .getElementById("resultCard")
        .classList.remove("hidden");
}


async function loadExceptions(
    driverId,
    summaryDate
) {

    try {

        const response = await fetch(
            `${API_BASE_URL}/exceptions/driver/${driverId}`
        );

        if (!response.ok) {
            return;
        }

        const exceptions = await response.json();

        const matchingExceptions =
            exceptions.filter(
                exception =>
                    exception.exception_date === summaryDate
            );

        const exceptionCard =
            document.getElementById("exceptionCard");

        const exceptionList =
            document.getElementById("exceptionList");

        exceptionList.innerHTML = "";

        if (matchingExceptions.length === 0) {

            exceptionList.innerHTML =
                "<p>No exceptions found.</p>";

            exceptionCard.classList.remove("hidden");

            return;
        }

        matchingExceptions.forEach(
            exception => {

                const div =
                    document.createElement("div");

                div.className = "exception";

                div.innerHTML = `
                    <div class="reason">
                        ${exception.reason_code}
                    </div>

                    <div class="severity">
                        Severity: ${exception.severity}
                    </div>

                    <div>
                        ${exception.message}
                    </div>
                `;

                exceptionList.appendChild(div);
            }
        );

        exceptionCard.classList.remove("hidden");

    } catch (error) {

        console.error(
            "Could not load exceptions:",
            error
        );
    }
}