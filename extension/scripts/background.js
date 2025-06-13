// Background has access to the extension chrome/tab api and talks to the popup

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    // console.log("query is listening");
    // Query the URL of the current active/focused tab
    if(message.type == "loadingContent"){
        chrome.tabs.query({ active: true, currentWindow: true}, (tab) => {
            url_link = tab[0].url;
            chrome.storage.local.get('content').then((data) => {
                sendResponse({url: url_link, content: data.content});
            });
        });
    }
    if(message.type == "contentReady"){
        chrome.storage.local.set({content : message.data}).then(() => console.log("Content saved"));
    };

    return true;
});
