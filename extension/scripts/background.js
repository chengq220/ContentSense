// // Background has access to the extension chrome/tab api and talks to the popup

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if(message.type == "loadingContent"){
        chrome.tabs.query({ active: true, currentWindow: true}, (tab) => {
            const title = tab[0].title ;
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
                .then(dat => sendResponse({title: title, res: dat}))
                .catch(err => {
                    console.error("Fetch error:", err);
                    sendResponse({ title: title, res: null, error: true });
                });
            });
        });
    }
    if(message.type == "contentReady"){
        chrome.storage.local.set({content : message.data}).then(() => console.log("Content saved"));
    };

    return true;
});


// Background has access to the extension chrome/tab api and talks to the popup

// chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
//     // console.log("query is listening");
//     // Query the URL of the current active/focused tab
//     if(message.type == "loadingContent"){
//         chrome.tabs.query({ active: true, currentWindow: true}, (tab) => {
//             title = tab[0].title ;
//             chrome.storage.local.get('content').then((data) => {
//                 sendResponse({title: title, content: data.content});
//             });
//         });
//     }
//     if(message.type == "contentReady"){
//         chrome.storage.local.set({content : message.data}).then(() => console.log("Content saved"));
//     };

//     return true;
// });