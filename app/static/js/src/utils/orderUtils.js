import loaderPlaceholder from './loader'; 

let OrderUtils = {
    placeOrder(order_data, hideOrderModal, showAppModal) {
        let className = '.place-order';
        order_data.ref = 'web';
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
                OrderUtils.handleError(jqXHR, '.order-error-msg');
                loaderPlaceholder(false, className, 'Place the Order'); 
            })
        });
    },
    fetchAreas() {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: '/fetchAreas',
                success:((response) => {
                    resolve(response);
                })
            });
        });
    },
    addAddress(address, hideModal) {
        let className=".confirm-address";
        $.ajax({
            url: '/addAddress',
            type: 'POST',
            data: {
                address: JSON.stringify(address),
                'ref': 'web'    
            },
            beforeSend: () => { loaderPlaceholder(true, className); },
            success:((response) => {
                //TODO store permanently
                let props = JSON.parse(store.props);
                props.user.address.push(response);
                window.renderApp(props);
                hideModal();
            }),
            error: ((jqXHR) => {
                OrderUtils.handleError(jqXHR, '.address-error-msg');
                loaderPlaceholder(false, className, 'Add Address'); 
            })
        });
    },
    handleError(jqXHR, className) {
        let error = "Something went wrong. Please contact us.";
        if (jqXHR.status >= 400 && jqXHR.status <= 460) {
            let error_msg = JSON.parse(jqXHR.responseText);
            error = error_msg.hasOwnProperty('message') ? error_msg.message : error;
        }
        $(className).text(error).slideDown('slow');
    }
}

export default OrderUtils;
