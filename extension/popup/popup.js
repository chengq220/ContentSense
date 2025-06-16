const setContent = response => {
    console.log(response)
    document.getElementById('title').textContent = response.title;
    document.getElementById('violation').textContent = response.res.violation;
    document.getElementById('safety').textContent = response.res.level;
};

function retrieveData(){
    chrome.runtime.sendMessage(
        {type: "loadingContent"},
        setContent);
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", retrieveData);
} else {
    retrieveData();
}

// retrieveData();
// chrome.runtime.onInstalled.addListener(() => {