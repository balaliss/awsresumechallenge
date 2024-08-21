async function updateVisitorCount() {
    try {
        const response = await fetch('https://lw5xvpwn9k.execute-api.us-east-1.amazonaws.com/prod/count');
        const data = await response.json(); // Assuming the response is already a JSON object
        console.log("Raw response data:", data);  // Log the raw response
        if (data.body) {
            const parsedData = JSON.parse(data.body); // Parse if necessary
            document.getElementById('visitorCount').innerText = `Visitor Count: ${parsedData.visitor_count}`;
        } else {
            document.getElementById('visitorCount').innerText = `Visitor Count: ${data.visitor_count}`;
        }
    } catch (error) {
        console.error("Error fetching visitor count:", error);
        document.getElementById('visitorCount').innerText = "Visitor Count: Error";
    }
}

window.onload = updateVisitorCount;
