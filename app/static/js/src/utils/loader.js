function loaderPlaceholder(flag, className, text='') {
    if (flag) {
        $(className).html('<img class="order-loader" src="'+store.cdn + 'loading.gif" />');  
    } else {
        $(className).text(text);  
    }
}

function loaderOverlay(flag, className, text='') {
    if (flag) {
        $(className).append('<div class="loader-overlay"><img class="inner-loader-img" src= "'+store.cdn + 'loading.gif"/></div>');  
    } else {
        $('.loader-overlay').remove();  
    }
}

module.exports = {
    loaderPlaceholder: loaderPlaceholder,
    loaderOverlay: loaderOverlay
};
