const setContent = response => {
    document.getElementById('url_link').textContent = response.url;
    document.getElementById('content').textContent = response.content.length;
};

function retrieveData(){
    chrome.tabs.query({active: true, currentWindow: true}, tabs => {
        chrome.runtime.sendMessage(
            {type: "loadingContent"},
            setContent);
    });
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", retrieveData);
} else {
    retrieveData();
}