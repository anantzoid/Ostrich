![Logo](app/static/img/watermark.png)

# Ostrich: E-commerce rental platform

Ostrich was built as a physical book rental platform which enables users to order books to their doorstep, track the delivery status, rate, review and return books. The complete e-commerce ecosystem surrounds the core feature providing the users with an end-to-end experience via strategic and timely push notification and mailers, Google authentication, automated updation of items and inventory and user behaviour tracking to understand preferences to name a few. 

The architecture is written in a simple and generic manner and can be customized to suit various business solutions. 

<br>
![Homepage](app/static/img/homepage_ss.png)
<br><br>

## Tech Stack

- [Flask](http://flask.pocoo.org/): Backend, api and rendering initial pages
- [ReactJS] (https://facebook.github.io/react/): Frontend (built using [Webpack] (https://webpack.github.io/))
- [Python-React] (https://github.com/markfinger/python-react/tree/master/examples/frontend-rendering-with-webpack): Bridge between Flask and React
- [Celery](http://www.celeryproject.org/): Crons, Automation, Crawling
- [Redis](https://redis.io/): Caching via Memcached, Broker for Celery
- [Mongodb](https://www.mongodb.com/): Backup & Logging
- [MySQL](https://www.mysql.com/)
- [Elasticsearch] (https://www.elastic.co/)
- [Apache Server] (https://httpd.apache.org/)
- [NodeJS server] (https://nodejs.org/en/)
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
To manage independenly running tasks like Celery schedulers, node servers etc., [Supervisor] (http://supervisord.org/) can be setup.

5. ### Mixpanel
Tracking has been setup to keep a counter of views on different activities by the user. All that needs to be done is save the Mixpanel credentials in the config file.

6. ### Arbor: B2B model
Apart from serving the consumers directly, Ostrich also had a B2B business model where organizations would signup and have a stocked book rack placed in their lobby. The people working over there could access a different interface and search and borrow books from the stock free of charge. The accesspoint is `/arbor` but I still need to work on the other parts of the B2B ecosystem to prepare for public release.

<br>

## API endpoints
The API endpoints cater to various user and admin facing features that correpond to both the web and mobile app. Relevant information is cached within API calls. The following is a non-exhaustive list highlighting some of the relevant ones:

### Search
- [Search String] ()
- [Report Search fail] ()
- [Categories] ()
- [Most Searched items] ()
- [Related/Recommended Items] ()

### Orders
- [Order/Rent Item] ()
- [Lend Item] ()
- [Order Details] ()
- [Order Status] ()
- [Time Slots for delivery] ()

### User
- [Signup] ()
- [User Details] ()
- [Edit Details] ()
- [Add Address] ()
- [Get Delivery areas] ()
- [Validate Delivery area] ()
- [Order History] ()
- [Wishlist Items] ()
- [Referral Code] ()
- [Reviews] ()
- [Delete User] ()
- [Mass notification to user groups] ()

### Admin
- [Inventory detail] ()
- [All Orders] ()
- [Update Order Status] ()
- [Crawl] ()
- [Send push notification] ()


## Other Goodies

### Design Pattern

### Python-React


### Responsive
The CSS has been written in a fully responsive manner to support all kinds of media resolutions.

![Responsive](app/static/img/responsive_homepage.gif)

<br>
### Mentions
Ostrich appeared in a [local lifestlye blog] (https://lbb.in/bangalore/ostrich-app-forlending-and-borrowing-books/) eons ago.


### Supporting apps and dashboards

- Admin Dashboard
	- Track and update orders
	- Crawl and add items
	- Monitor user activity
	- Control homepage and app content
- Slack app
- Android app
- Arbor (Business Solution)

I'm still working on refining the docs and make them easily installable on any machine. Contributions are welcome.