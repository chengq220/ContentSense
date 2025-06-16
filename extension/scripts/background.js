// // Background has access to the extension chrome/tab api and talks to the popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if(message.type == "loadingContent"){
        chrome.storage.local.get('content').then((data) => {
            sendResponse(data.content);
        });
        return true;
    }
    if(message.type == "contentReady"){
        chrome.tabs.query({ active: true, currentWindow: true}, (tab) => {
            const title = tab[0].title;
            const id = tab[0].id;
            payload = {
                "content": message.data
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
                var cont = {
                    title : title, 
                    res: dat
                }
                chrome.storage.local.set({content : cont}, function(response){});
                checkSafety(id, dat.level);
            })
            .catch(err => {
                console.error("Fetch error:", err);
            });
        });
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
