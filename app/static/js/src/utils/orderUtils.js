import loaderPlaceholder from './loader'; 

let OrderUtils = {
    placeOrder(order_data, hideOrderModal, showAppModal) {
        let className = '.place-order';
        $.ajax({
            type: 'POST',
            url: '/order',
            data: order_data,
            beforeSend: () => { loaderPlaceholder(true, className); },
            success:((response) => {
                if (response.hasOwnProperty('order_id')) {
                    hideOrderModal();
                    showAppModal();
                }
            }),
            error: ((jqXHR) => {
                let error = JSON.parse(jqXHR.responseText);
                // TODO show error if appropriate code, else generic msg
                // remove loading
                console.log(error);
                loaderPlaceholder(false, className, 'Place the Order'); 
            })
        });
    },
}

export default OrderUtils;
