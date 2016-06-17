import { loaderPlaceholder } from './loader';

let FeedbackUtils = {
    submit(data) {
        return new Promise((resolve, reject) => {
            let className = ".feedback-submit"; 
            $.ajax({
                url: '/feedback',
                type: 'POST',
                data: data,
                beforeSend: () => { loaderPlaceholder(true, className); },
                success: ((response) => {
                    loaderPlaceholder(false, className, 'Submit');
                    resolve(response);
                }),
                error:(() => {
                    loaderPlaceholder(false, className, 'Submit');
                    reject();
                })
            });
        });
    },
    validateEmail(email) {
        let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    },
    toggleModal() {
        store.props.feedback_form = !store.props.feedback_form;
        window.renderApp(store.props);
    }
}
export default FeedbackUtils;
