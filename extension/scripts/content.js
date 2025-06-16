// Content have access to the DOM/the page information like innerHTML etc.
function get_content(){
    try{
        var text = document.documentElement.innerText;
        var processText = text.match(/[^?!.]*[?!.]/g) || [];  
        if(processText.length > 0){
            processText.shift();
        }
        processText = processText.filter((text, idx) => text.length > 15 && idx % 2 == 0)
        return processText;
    }
    catch(error){
        console.error("Error: ", error);
        return null;
    }   
}

function sendContent(){
    const content = get_content();
    chrome.runtime.sendMessage({ type: "contentReady", data: content });
};

// When DOM finishes loading, set the content to storage
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", sendContent);
} else {
    sendContent();
}

//Once the content have been processed in the backend, display this block if 
//there's safety hazard
const block = chrome.runtime.getURL("block/block.html")
const iframe = document.createElement("iframe");

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if(request.type == "notSafeSetup"){
        iframe.src = block;
        iframe.style.position = "fixed";
        iframe.style.top = "0";
        iframe.style.left = "0";
        iframe.style.width = "100vw";
        iframe.style.height = "100vh";
        iframe.style.border = "none";
        iframe.style.zIndex = "9999";
        iframe.style.display = "block";

        if(!document.body.contains(iframe)){
            document.body.appendChild(iframe);
        }
    }

    if(request.type == "proceed"){
        console.log("proceed to close iframe")
        iframe.style.display = "none";
    }

    return true;
});
