async function getFingerprint() {
    const fp = await FingerprintJS.load();
    const result = await fp.get();
    return result.visitorId;   // a unique string identifying this browser/device
}

async function checkIn() {
    const statusDiv = document.getElementById("status");
    const sessionId = document.getElementById("sessionId").value;

    if (!sessionId) {
        statusDiv.className = "fail";
        statusDiv.innerText = "Please enter a session ID.";
        return;
    }

    statusDiv.className = "";
    statusDiv.innerText = "Checking in...";

    const fingerprint = await getFingerprint();

    const res = await fetch("/student/checkin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, fingerprint: fingerprint }),
    });

    const data = await res.json();

    if (data.status === "accepted") {
        statusDiv.className = "ok";
        statusDiv.innerText = "✅ Attendance marked present!";
    } else {
        statusDiv.className = "fail";
        statusDiv.innerText = "❌ Rejected: " + data.reason;
    }
}
