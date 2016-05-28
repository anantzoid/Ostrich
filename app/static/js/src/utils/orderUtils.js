

let OrderUtils = {
    placeOrder(order_data, hideOrderModal, showAppModal) {
        $.ajax({
            type: 'POST',
            url: '/order',
            data: order_data,
            beforeSend: () => { OrderUtils.orderLoader(true); },
            success:((response) => {
                if (response.hasOwnProperty('order_id')) {
                    hideOrderModal();
                    showAppModal('Order Placed Successfully');
                }
            }),
            error: ((jqXHR) => {
                let error = JSON.parse(jqXHR.responseText);
                // TODO show error if appropriate code, else generic msg
                // remove loading
                console.log(error);
                OrderUtils.orderLoader(false); 
            })
        });
    },
    orderLoader(flag) {
        // TODO replace with loder
        if (flag) {
           $('.place-order').text('<img class="order-loader" src="/static/img/loading.gif" />');  
        } else {
           $('.place-order').text('Place the Order');  
        }
    }
}

export default OrderUtils;
