// Query the URL of the current active/focused tab
const queryURL = async () => {
    let queryOptions = {active:true, lastFocusWindow: true};
    let [tab] = await chrome.tabs.query(queryOptions);
    return tab.url;
}

// Get the text in the HTML
function extractContent(html) {
    return new DOMParser()
        .parseFromString(html, "text/html")
        .documentElement.textContent;
}

// async function test(){
//     console.log("onload called test function");
//     let url = await queryURL();
//     console.log("the tab is ", url);
// }

// test();


chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if(message == "get_url"){
        chrome.tabs.query({ active: true, currentWindow: true}, (tab) => {
            sendResponse({url: tab.url});
        })
    }
    return true;
});