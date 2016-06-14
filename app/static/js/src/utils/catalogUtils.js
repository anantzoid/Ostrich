import { loaderPlaceholder } from './loader'; 

let CatalogUtils = {
    loadMore(page) {
        return new Promise((resolve, reject) => {
            let className = '.load-more';
            let params = {};
            window.location.search.substr(1).split('&').forEach(function(param) {
                let _ = param.split('=');
                params[_[0]] = _[1];
            });
            //NOTE only handled for category
            if (!params.hasOwnProperty('q')) {
                let page_type = window.location.pathname.split("/");
                params['type'] = page_type[2];
                params['q'] = page_type[3].replace(/\w\S*/g, ((txt) => {
                    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
                }));
            }
            params.page = page;
            params.ref = 'web';
            $.ajax({
                url: '/search',
                data: params,
                beforeSend: () => { loaderPlaceholder(true, className); },
                success: ((response) => {
                    try {
                        response = JSON.parse(response);
                    } catch(exception) {
                        response = response;
                    }
                    loaderPlaceholder(false, className, 'Load More');
                    resolve(response);
                }),
                error: (() => {
                    loaderPlaceholder(false, className, 'Load More');
                    reject();
                })  
            });  
        });
    }
}
export default CatalogUtils;
