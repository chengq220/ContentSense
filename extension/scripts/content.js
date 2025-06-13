// Content have access to the DOM/the page information like innerHTML etc.
function get_content(){
    try{
        var text = document.documentElement.innerText;
        const processText = text.match(/[^?!.]*[?!.]/g) || [];  
        if(processText.length > 0){
            processText.shift();
        }
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


if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", sendContent);
} else {
    sendContent();
}