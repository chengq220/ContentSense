// // Background has access to the extension chrome/tab api and talks to the popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if(message.type == "loadingContent"){
        chrome.tabs.query({ active: true, currentWindow: true}, (tab) => {
            const title = tab[0].title;
            const id = tab[0].id;
            chrome.storage.local.get('content').then((data) => {
                payload = {
                    "content": data.content
                }
                fetch("http://localhost:8000/pred", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(payload)
                })
                .then(res => res.json())
                .then(dat => {
                    // console.log("processing data");
                    checkSafety(id, dat.level);
                    sendResponse({title: title, res: dat});
                })
                .catch(err => {
                    console.error("Fetch error:", err);
                    sendResponse({ title: title, res: null, error: true });
                });
            });
        });
        return true;
    }
    if(message.type == "contentReady"){
        chrome.storage.local.set({content : message.data}, function(response){});
    };
    if(message.type == "proceed"){
        chrome.tabs.query({ active: true, currentWindow: true}, (tab) => {
           chrome.tabs.sendMessage(tab[0].id, {type: "proceed"}, function(response) {});  
        });
    }
});

function checkSafety(id, level) {
    if(level == "Not safe"){
        chrome.tabs.sendMessage(id, {type: "notSafeSetup"}, function(response) {});  
    }
}
