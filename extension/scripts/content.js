chrome.runtime.sendMessage('get_url', (response) => {
    if(chrome.runtime.lastError){
        console.error("Error:", chrome.runtime.lastError.message);
    }else{
        console.log('received data', response);
    }
});
