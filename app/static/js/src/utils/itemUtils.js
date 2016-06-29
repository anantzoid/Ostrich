import React from 'react';

let ItemUtils = {
    getRatings(item_ratings) {
        let ratings = null;
        if(item_ratings) { 
            ratings = Array.apply(null, Array(parseInt(item_ratings))).map((_, i) => {
                return <span className="glyphicon glyphicon-star" aria-hidden="true"></span>;
            });
            if (ratings.length < item_ratings) {
                ratings.push(<span className="glyphicon glyphicon-star star-half" aria-hidden="true"></span>);
            }
        }
        return ratings;
    },
    getCategories(item_categories) {
        let categories = item_categories.map((category, i) => {
            let key = 'category-'+category.category_id;
            let last_el = item_categories.length-1 !== i ? ', ': ''; 
            return <span className="category-tag" key={key}><a href={category.slug_url}>{category.category_name}</a>{last_el}</span>;
        });
        return categories;
    }
}
export default ItemUtils;
