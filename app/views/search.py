from app import webapp
from app.models import Search , Utils
from flask import request, jsonify
import json


'''
    Generic search call
    @params
        q: search query
        page: the page number of search results (default 0)
        type: type of search: {default: free(all fields), category, isbn}

    @response
        List of search result objects(ES)
'''
@webapp.route('/search')
def searchString():
    response = {'status': 'False'}

    query = Utils.getParam(request.args, 'q') 
    page = int(Utils.getParam(request.args, 'page', var_type='int', default=1))
    search_type = Utils.getParam(request.args, 'type', default='free')

    if not query:
        return jsonify(response), webapp.config['HTTP_STATUS_CODE_DATA_MISSING']

    search = Search(query)
    if search_type == 'free':
        results = search.basicSearch(page=page-1)
    elif search_type == 'category':
        results = search.categorySearch(page=page-1)
    elif search_type == 'isbn':
        results = search.isbnSearch(page=page-1)
    elif search_type == 'custom':
        results = search.customQuery()
        return results

    return jsonify(results)

@webapp.route('/getCategories')
def getCategories():
    categories = Search.getSearchCategories()
    return json.dumps(categories)

@webapp.route('/searchFail', methods=['GET'])
def searchFail():
    user_id = Utils.getParam(request.args, 'user_id', 'int')
    q = Utils.getParam(request.args, 'q')
    q_type = Utils.getParam(request.args,'type')
    
    Search.reportFail(user_id, q, q_type)
    return jsonify(status='true')

@webapp.route('/recommended', methods=['GET'])
def recommended():
    return json.dumps([
        {
            "author": "Sir Arthur Conan Doyle",
            "categories": [
                "Others"
                ],
            "img_large": None,
            "img_small": "http://img5a.flixcart.com/image/book/4/0/4/the-adventures-of-sherlock-holmes-400x400-imaddpw4j3zhy69z.jpeg",
            "isbn_10": [
                "9380703406"
                ],
            "isbn_13": [
                "9789380703404"
                ],
            "item_id": 1399,
            "item_name": "The Adventures of Sherlock Holmes (English)",
            "language": "English",
            "num_ratings": 0,
            "price": 125,
            "ratings": None
            },
        {
            "author": "Peter Thiel, Blake Masters",
            "categories": [
                "Business & Management",
                "Entrepreneurship",
                "Strategy, Economics"
                ],
            "img_large": None,
            "img_small": "http://ecx.images-amazon.com/images/I/41puRJbtwkL.jpg",
            "isbn_10": [
                "0804139296"
                ],
            "isbn_13": [
                "9780804139298"
                ],
            "item_id": 1487,
            "item_name": "Zero to One: Notes on Startups, or How to Build the Future",
            "language": "English",
            "num_ratings": 0,
            "price": 1311,
            "ratings": None
            },
        {
            "author": "Gregory David Roberts",
            "categories": [
                "Fiction"
                ],
            "img_large": None,
            "img_small": "images/books/565aefff2cdb8136aade1851/1/0.jpg",
            "isbn_10": [
                "0312330529"
                ],
            "isbn_13": [
                "9780312330521"
                ],
            "item_id": 245,
            "item_name": "Shantaram: A Novel",
            "language": "English",
            "num_ratings": 0,
            "price": 1813,
            "ratings": None
            },
        {
                "author": "Ben Horowitz",
                "categories": [
                    "Business & Management"
                    ],
                "img_large": None,
                "img_small": "http://ecx.images-amazon.com/images/I/51slqM2g3jL.jpg",
                "isbn_10": [
                    "0062273205"
                    ],
                "isbn_13": [
                    "9780062273208"
                    ],
                "item_id": 1861,
                "item_name": "The Hard Thing about Hard Thing: Building a Business When There are No Easy Answers",
                "language": "English",
                "num_ratings": 0,
                "price": 461,
                "ratings": None
                },
        {
                "author": "J.K. Rowling",
                "categories": [],
                "img_large": None,
                "img_small": "images/books/565adc3c2cdb81335fda8012/1/0.jpg",
                "isbn_10": [
                    "1408865270"
                    ],
                "isbn_13": [
                    "9781408865279"
                    ],
                "item_id": 194,
                "item_name": "Harry Potter and the Philosopher's Stone Adult Hardcover (Harry Potter 1 Adult Edition)",
                "language": "English",
                "num_ratings": 0,
                "price": 1330,
                "ratings": None
                },
        {
                "author": "J. R. R. Tolkien",
                "categories": [
                    "Others"
                    ],
                "img_large": None,
                "img_small": "http://img5a.flixcart.com/image/book/0/8/2/hobbit-in-only-400x400-imadguudh5znsggr.jpeg",
                "isbn_10": [
                    "0007511086"
                    ],
                "isbn_13": [
                    "9780007511082"
                    ],
                "item_id": 1704,
                "item_name": "Hobbit In Only (English)",
                "language": "English",
                "num_ratings": 0,
                "price": 319,
                "ratings": None
                },
        {
                "author": "Frank Miller, David Mazzucchelli",
                "categories": [],
                "img_large": None,
                "img_small": "images/books/565ad70d2cdb8131edff18bb/1/0.jpg",
                "isbn_10": [
                    "1401207529"
                    ],
                "isbn_13": [
                    "9781401207526"
                    ],
                "item_id": 1193,
                "item_name": "Batman: Year One",
                "language": "English",
                "num_ratings": 0,
                "price": 544,
                "ratings": None
                },
        {
                "author": "Sidney Sheldon",
                "categories": [
                    "Others"
                    ],
                "img_large": None,
                "img_small": "http://ecx.images-amazon.com/images/I/51NAXKupi4L.jpg",
                "isbn_10": [
                    "0007837070"
                    ],
                "isbn_13": [
                    "9780007837076"
                    ],
                "item_id": 1703,
                "item_name": "Sidney Sheldon - The Best Laid Plans",
                "language": "English",
                "num_ratings": 0,
                "price": 275,
                "ratings": None
                },
        {
                "author": "Stephen King",
                "categories": [
                    "Fiction",
                    "Horror"
                    ],
                "img_large": None,
                "img_small": "http://ecx.images-amazon.com/images/I/51Kf%2BjjhR0L.jpg",
                "isbn_10": [
                    "1444720724"
                    ],
                "isbn_13": [
                    "9781444720723"
                    ],
                "item_id": 1531,
                "item_name": "The Shining",
                "language": "English",
                "num_ratings": 0,
                "price": 240,
                "ratings": None
                },
        {
                "author": "ESPN Cricinfo",
                "categories": [],
                "img_large": None,
                "img_small": "images/books/566605132cdb816282eb24bc/1/0.jpg",
                "isbn_10": [
                    "9381810788"
                    ],
                "isbn_13": [
                    "9789381810781"
                    ],
                "item_id": 243,
                "item_name": "Rahul Dravid: Timeless Steel (Anthology)",
                "language": "English",
                "num_ratings": 0,
                "price": 0,
                "ratings": None
                }
        ])

@webapp.route('/mostSearched', methods=['GET'])
def mostSearched():
    return json.dumps([
        {
            "author": "J. R. R. Tolkien",
            "categories": [
                "Others"
                ],
            "img_large": None,
            "img_small": "http://img5a.flixcart.com/image/book/0/8/2/hobbit-in-only-400x400-imadguudh5znsggr.jpeg",
            "isbn_10": [
                "0007511086"
                ],
            "isbn_13": [
                "9780007511082"
                ],
            "item_id": 1704,
            "item_name": "Hobbit In Only (English)",
            "language": "English",
            "num_ratings": 0,
            "price": 319,
            "ratings": None
            },
        {
            "author": "Frank Miller, David Mazzucchelli",
            "categories": [],
            "img_large": None,
            "img_small": "images/books/565ad70d2cdb8131edff18bb/1/0.jpg",
            "isbn_10": [
                "1401207529"
                ],
            "isbn_13": [
                "9781401207526"
                ],
            "item_id": 1193,
            "item_name": "Batman: Year One",
            "language": "English",
            "num_ratings": 0,
            "price": 544,
            "ratings": None
            },
        {
            "author": "Ben Horowitz",
            "categories": [
                "Business & Management"
                ],
            "img_large": None,
            "img_small": "http://ecx.images-amazon.com/images/I/51slqM2g3jL.jpg",
            "isbn_10": [
                "0062273205"
                ],
            "isbn_13": [
                "9780062273208"
                ],
            "item_id": 1861,
            "item_name": "The Hard Thing about Hard Thing: Building a Business When There are No Easy Answers",
            "language": "English",
            "num_ratings": 0,
            "price": 461,
            "ratings": None
            },
        {
                "author": "Sir Arthur Conan Doyle",
                "categories": [
                    "Others"
                    ],
                "img_large": None,
                "img_small": "http://img5a.flixcart.com/image/book/4/0/4/the-adventures-of-sherlock-holmes-400x400-imaddpw4j3zhy69z.jpeg",
                "isbn_10": [
                    "9380703406"
                    ],
                "isbn_13": [
                    "9789380703404"
                    ],
                "item_id": 1399,
                "item_name": "The Adventures of Sherlock Holmes (English)",
                "language": "English",
                "num_ratings": 0,
                "price": 125,
                "ratings": None
                },
        {
                "author": "Peter Thiel, Blake Masters",
                "categories": [
                    "Business & Management",
                    "Entrepreneurship",
                    "Strategy, Economics"
                    ],
                "img_large": None,
                "img_small": "http://ecx.images-amazon.com/images/I/41puRJbtwkL.jpg",
                "isbn_10": [
                    "0804139296"
                    ],
                "isbn_13": [
                    "9780804139298"
                    ],
                "item_id": 1487,
                "item_name": "Zero to One: Notes on Startups, or How to Build the Future",
                "language": "English",
                "num_ratings": 0,
                "price": 1311,
                "ratings": None
                },
        {
                "author": "Gregory David Roberts",
                "categories": [
                    "Fiction"
                    ],
                "img_large": None,
                "img_small": "images/books/565aefff2cdb8136aade1851/1/0.jpg",
                "isbn_10": [
                    "0312330529"
                    ],
                "isbn_13": [
                    "9780312330521"
                    ],
                "item_id": 245,
                "item_name": "Shantaram: A Novel",
                "language": "English",
                "num_ratings": 0,
                "price": 1813,
                "ratings": None
                },
        {
                "author": "J.K. Rowling",
                "categories": [],
                "img_large": None,
                "img_small": "images/books/565adc3c2cdb81335fda8012/1/0.jpg",
                "isbn_10": [
                    "1408865270"
                    ],
                "isbn_13": [
                    "9781408865279"
                    ],
                "item_id": 194,
                "item_name": "Harry Potter and the Philosopher's Stone Adult Hardcover (Harry Potter 1 Adult Edition)",
                "language": "English",
                "num_ratings": 0,
                "price": 1330,
                "ratings": None
                },
        {
                "author": "Sidney Sheldon",
                "categories": [
                    "Others"
                    ],
                "img_large": None,
                "img_small": "http://ecx.images-amazon.com/images/I/51NAXKupi4L.jpg",
                "isbn_10": [
                    "0007837070"
                    ],
                "isbn_13": [
                    "9780007837076"
                    ],
                "item_id": 1703,
                "item_name": "Sidney Sheldon - The Best Laid Plans",
                "language": "English",
                "num_ratings": 0,
                "price": 275,
                "ratings": None
                },
        {
                "author": "Stephen King",
                "categories": [
                    "Fiction",
                    "Horror"
                    ],
                "img_large": None,
                "img_small": "http://ecx.images-amazon.com/images/I/51Kf%2BjjhR0L.jpg",
                "isbn_10": [
                    "1444720724"
                    ],
                "isbn_13": [
                    "9781444720723"
                    ],
                "item_id": 1531,
                "item_name": "The Shining",
                "language": "English",
                "num_ratings": 0,
                "price": 240,
                "ratings": None
                },
        {
                "author": "ESPN Cricinfo",
                "categories": [],
                "img_large": None,
                "img_small": "images/books/566605132cdb816282eb24bc/1/0.jpg",
                "isbn_10": [
                    "9381810788"
                    ],
                "isbn_13": [
                    "9789381810781"
                    ],
                "item_id": 243,
                "item_name": "Rahul Dravid: Timeless Steel (Anthology)",
                "language": "English",
                "num_ratings": 0,
                "price": 0,
                "ratings": None
                }
        ])
