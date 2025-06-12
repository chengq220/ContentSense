chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    // Query the URL of the current active/focused tab
    if(message == "get_url"){
        chrome.tabs.query({ active: true, currentWindow: true}, (tab) => {
            sendResponse({url: tab[0].url});
        })
    }
    return true;
});