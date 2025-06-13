const setContent = response => {
    document.getElementById('title').textContent = response.title;
    document.getElementById('content').textContent = response.content.length;
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