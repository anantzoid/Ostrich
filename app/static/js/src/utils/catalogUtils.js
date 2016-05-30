import loaderPlaceholder from './loader'; 

let CatalogUtils = {
    loadMore(page) {
 loaderPlaceholder(true,  '.load-more'); 
        return new Promise((resolve, reject) => {
            let className = '.load-more';
            let params = window.location.search;
            params = params.replace(/page=\d*/,'');
            $.ajax({
                url: '/search' + params,
                data: {
                    page: page,
                    ref: 'web'
                },
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
