

let OrderUtils = {
    placeOrder(order_data, hideOrderModal, showAppModal) {
        $.ajax({
            type: 'POST',
            url: '/order',
            data: order_data,
            success:((response) => {
                if (response.hasOwnProperty('order_id')) {
                    hideOrderModal();
                    showAppModal('Order Placed Successfully');
                }
            }),
            error: ((jqXHR) => {
                let error = JSON.parse(jqXHR.responseText);
                // TODO show error
                console.log(error);
            })
        });
    }
}

export default OrderUtils;
