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
            error: (() => {
                // TODO error message on modal
                loaderPlaceholder(false, className, 'Add Address'); 
            })
        });
    }
}

export default OrderUtils;
