![Logo](app/static/img/watermark.png)

# Ostrich: E-commerce rental platform

Ostrich was built as a physical book rental platform which enables users to order books to their doorstep, track the delivery status, rate, review and return books. The complete e-commerce ecosystem surrounds the core feature providing the users with an end-to-end experience via strategic and timely push notification and mailers, Google authentication, automated updation of items and inventory and user behaviour tracking to understand preferences to name a few. 

The architecture follows a lightweight, intuitive design pattern inspired by the beautiful [flamejam](https://github.com/svenstaro/flamejam) project for the backend and [flux](https://facebook.github.io/flux/docs/overview.html) architecture for the React frontend. The platform is written in a simple and generic manner and can be customized to suit various business solutions. 

<br>

![Homepage](app/static/img/screens/homepage_ss.png)

<br>

Scroll to the bottom to checkout more screenshots.

<br><br>

## Tech Stack

- [Flask](http://flask.pocoo.org/): Backend, api and rendering initial pages
- [ReactJS](https://facebook.github.io/react/): Frontend (built using [Webpack] (https://webpack.github.io/))
- [Python-React](https://github.com/markfinger/python-react/tree/master/examples/frontend-rendering-with-webpack): Bridge between Flask and React
- [Celery](http://www.celeryproject.org/): Crons, Automation, Crawling
- [Redis](https://redis.io/): Caching via Memcached, Broker for Celery
- [Mongodb](https://www.mongodb.com/): Backup & Logging
- [MySQL](https://www.mysql.com/)
- [Elasticsearch](https://www.elastic.co/)
- [Apache Server](https://httpd.apache.org/)
- [NodeJS server](https://nodejs.org/en/)
- [AWS](https://aws.amazon.com): EC2, ES, Route 53, S3, CDN, RDS

<br>

## Installation

The installations steps have been tested on a linux machine (Ubuntu) and might vary for other OS in terms of setting up the dependencies.

1. Clone the repo and `cd` into it.
2. Install MySQL.
	
	```
	sudo apt-get install mysql-server	
	sudo apt-get install libmysqlclient-dev
	```

	Create database ostrichdb. Import the sample data dump. One way to do this is:
	
	```
	mysql -u root -p ostrichdb < docs/ostrichdb.sql
	```
3. Install python dependecies	

	```
	xargs -a docs/requirements.txt -n 1 pip install
	```
	As opposed to `pip install -r docs/requirements.txt`, this method skips over errors while installation.

4. Copy the config file.

	```
	cp -R docs/ostrich_conf /etc/ostrich_conf
	```
	Alternatively, you can change the location of the config file in `app/__init__.py` and `app/views/v1/website.py (line 144)`.
	
5. Make appropriate changes in the `ostrich_conf/app_config.cfg.template` file, removing the `.template` extension.

6. Installing frontend components:

	```
	cd app/static/js
	npm install
	npm run pack
	```
7. [Install redis](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04). Follow the steps in the link till *Build and Install Redis*. Then start the redis server.

	```
	redis-server
	```
7. Start the node server

	```
	node render_server.js
	```
8. Start the flask server

	```
	python run.py
	```
<br>

### Optional Setups
The following are other things to setup that application makes use of to provide a richer experience.

1. ### Elasticsearch
Prodcut Searches can be made in two different ways using the same APIs: Elasticsearch and MySQL. This switch can be controlled from the config file. The schema for ES lies in `docs/search_mapping.json` and items can be indexed in ES by calling the `python manage.py indexer`.

2. ### Google Auth
Although there is a manual signup API, the web application uses Google Authentication as it's default signin technique. To enable this, get a `client_id` and paste it in `ostrich_conf/google_client_secrete.json`.

3. ### Celery
Many background tasks run to perform tasks like keeping the db updated (by crawling new listings and updating the existing ones), sending notifications and mails to users for returning the book and upselling products etc. These tasks are run by [Celery](http://www.celeryproject.org/) and can be reviewed in `scheduler.py`.

4. ### Supervisor
To manage independenly running tasks like Celery schedulers, node servers etc., [Supervisor](http://supervisord.org/) can be setup.

5. ### Mixpanel
Tracking has been setup to keep a counter of views on different activities by the user. All that needs to be done is save the Mixpanel credentials in the config file.

6. ### Arbor: B2B model
Apart from serving the consumers directly, Ostrich also had a B2B business model where organizations would signup and have a stocked book rack placed in their lobby. The people working over there could access a different interface and search and borrow books from the stock free of charge. The accesspoint is `/arbor` but I still need to work on the other parts of the B2B ecosystem to prepare for public release.

<br>

## API endpoints
The API endpoints cater to various user and admin facing features that correpond to both the web and mobile app. Relevant information is cached within API calls. The following is a non-exhaustive list highlighting some of the relevant ones:

### Search
- [Search String](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/search.py#L18)
- [Report Search fail](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/search.py#L68)
- [Categories](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/search.py#L59)
- [Most Searched items](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/search.py#L85)
- [Related/Recommended Items](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/search.py#L81)

### Orders
- [Order/Rent Item](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/order.py#L25)
- [Lend Item](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/order.py#L77)
- [Order Details](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/order.py#L97)
- [Order Status](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/order.py#L131)
- [Time Slots for delivery](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/order.py#L196)

### User
- [Signup](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/user.py#L72)
- [User Details](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/user.py#L35)
- [Edit Details](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/user.py#L155)
- [Add Address](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/user.py#L104)
- [Get Delivery areas](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/user.py#L224)
- [Validate Delivery area](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/user.py#L133)
- [Order History](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/user.py#L186)
- [Wishlist Items](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/user.py#L201)
- [Referral Code](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/user.py#L235)
- [Reviews](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/review.py#L6)
- [Delete User](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/user.py#L331)
- [Mass notification to user groups](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/user.py#L338)

### Admin
- [Inventory detail](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/admin.py#L24)
- [All Orders](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/admin.py#L19)
- [Update Order Status](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/admin.py#L72)
- [Crawl](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/admin.py#L95)
- [Send push notification](https://github.com/anantzoid/Ostrich/blob/master/app/views/v1/admin.py#L8)

<br/><br/>

## Bonus Goodies

### SEO by rendering React pages through Flask
We know good SEO is acheived if pages are rendered via server initially. But here lies a challenge since the backend here is Flask, and only Node can render React pages from server side. Hence, with the help of [Python-React](https://github.com/markfinger/python-react), an intermediate Node server is setup that receives payload from flask depending on the url/query and renders the React template to normal string accordingly. This plain string is then passed pack to Flask which returns it to the browser. Of course, there a number of intricacies that needs to be taken care of which I've isolated in this design pattern [here](https://github.com/markfinger/python-react/tree/master/examples/frontend-rendering-with-webpack). Also, note that this mechanism was implemented in Spring 2016 and there might have been considerable developments done in the area since then.


### Responsive
The CSS has been written in a fully responsive manner to support all kinds of media resolutions.

<div style="text-align:center"><img src="/anantzoid/Ostrich/raw/master/app/static/img/screens/responsive_homepage.gif" alt="Responsive" style="width: 255px;"></div>

<br>

### Mentions

Ostrich appeared in a [local lifestyle blog](https://lbb.in/bangalore/ostrich-app-forlending-and-borrowing-books/) eons ago.


### Supporting apps and dashboards

Apart from the main product codebase, Ostrich comprises of a suite of complementing tools consisting of:

- Admin Dashboard
	- Track and update orders
	- Crawl and add items
	- Monitor user activity
	- Control homepage and app content
- Slack app
- Android app
- Arbor (Business Solution)

I'm still working on refining the docs and make them easily installable on any machine. Contributions are welcome.

## Product Preview

### Catalog Page
<div style="text-align:center"><img src="/anantzoid/Ostrich/raw/master/app/static/img/screens/item.png" alt="Item" style="max-width:100%;width: 600px;"></div>

<br/>

### Order Dialog
<div style="text-align:center"><img src="/anantzoid/Ostrich/raw/master/app/static/img/screens/order.png" alt="Order" style="max-width:100%;width: 600px;"></div>

<br/>

### Add address Dialog
<div style="text-align:center"><img src="/anantzoid/Ostrich/raw/master/app/static/img/screens/address.png" alt="Address" style="max-width:100%;width: 600px;"></div>

<br/>

### Responsive Catalog Page
<div style="text-align:center"><img src="/anantzoid/Ostrich/raw/master/app/static/img/screens/responsive_product.gif" alt="Catalog" style="width: 255px;"></div>

