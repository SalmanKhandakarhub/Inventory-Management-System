# Install Required
pip install Flask Flask-SQLAlchemy Flask-Migrate mysqlclient python-dotenv reportlab requests pandas pytest
pip install -U click (use for making command line in flask)


# Database migrations
flask --app webapp db init
flask --app webapp db migrate -m "db migrations"
flask --app webapp db upgrade


# Create a folder for saveing pdf file
Folder name :- Invoices

# Command line
## Show all Product :- 
    $python3 -m webapp.cmd getproducts
## Add product:- 
    $python3 -m webapp.cmd addproduct --name "<product name>" --category "<category name>" --price <amount> --quantity <number of quantity>
## Delete product:- 
    $python3 -m webapp.cmd deleteproduct <product_id>
## Sales:- 
    $python3 -m webapp.cmd sale --product_id <product_id> --quantity <number of quantity> --price <amount> --customer_id 1
## Return:- 
    $python3 -m webapp.cmd returnsale --product_id <product_id> --quantity <number of quantity> --price <amount> --reason "<commant>"
## Invoice generate
    $python3 -m webapp.cmd generateinvoice --sale_ids <sale id>
