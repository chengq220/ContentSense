chrome.runtime.sendMessage('get_url', (response) => {
    if(chrome.runtime.lastError){
        console.error("Error:", chrome.runtime.lastError.message);
    }else{
        console.log('received data', response);
    }
});

function get_content(){
    try{
        var text = document.documentElement.innerText;
        const processText = text.match(/[^?!.]*[?!.]/g);
        processText.shift();
        if(processText.length > 0){
            console.log(processText[0]);

            console.log('text extracted');
        }else{
            console.log("text not extracted");
        }
    }catch(error){
        console.error("Error: Unable to get text from the page");
    }
    
}

get_content();