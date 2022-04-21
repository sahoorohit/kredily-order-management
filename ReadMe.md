Steps to deploy on heroku: 

1. Create a heroku app, and change the allowed host in `settings.py`
2. Create PostgresDB `heroku addons:create heroku-postgresql:hobby-dev`
3. Deploy this branch `git push heroku heroku-master:master`
4. Run the migrations
    - `heroku run bash`
    - `python manage.py migrate`
5. Create SuperUser for admin access
    - `python manage.py createsuperuser`
6. Populate dummy products data
    - `python manage.py shell`
    - `from setup import populate_products`
    - `populate_products()`
7. Use the postman collection provided, to test the APIs
    - Note: Change the `host_url` variable in the collection
