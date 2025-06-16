
// the function for clicking a button
const btn = document.getElementById("continue-btn");
btn.addEventListener("click", () => {
    chrome.runtime.sendMessage({ type: "proceed" }, () => {
    if (chrome.runtime.lastError) {
        console.error("Runtime error:", chrome.runtime.lastError.message);
    } else {
        console.log("Message sent successfully");
    }});
});