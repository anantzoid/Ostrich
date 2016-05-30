function loaderPlaceholder(flag, className, text='') {
    if (flag) {
        $(className).html('<img class="order-loader" src="/static/img/loading.gif" />');  
    } else {
        $(className).text(text);  
    }
}

module.exports = loaderPlaceholder;
