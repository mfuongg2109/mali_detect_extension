// Maintain a list of whitelisted URLs
const whitelist = new Set();

// Handle messages from content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "checkUrl") {
        const url = message.url;

        // Use your logic to determine if the URL is malicious
        fetch("http://192.168.1.53:5000/check-url", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ url }),
        })
            .then((response) => response.json())
            .then((data) => {
                const isMalicious = data.isMalicious;
                sendResponse({ isMalicious });
            })
            .catch((error) => {
                console.error("Error checking URL:", error);
                sendResponse({ isMalicious: false });
            });

        return true; // Keep the message channel open for asynchronous response
    } else if (message.action === "setWhitelisted") {
        // Add the URL to the whitelist
        console.log("Whitelisting URL:", message.url);
        whitelist.add(message.url);
        sendResponse(true);
    } else if (message.action === "isWhitelisted") {
        // Check if the URL is in the whitelist
        const isWhitelisted = whitelist.has(message.url);
        console.log("Checking whitelist for URL:", message.url, "->", isWhitelisted);
        sendResponse(isWhitelisted);
    }
});
