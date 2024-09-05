import click
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.environ.get('API_URL') 

@click.group()
def cmd():
    """Inventory Management System"""
    pass

@click.command()
def getproducts():
    """List all Products"""
    response = requests.get(f"{API_URL}/add-get-products")
    if response.status_code == 200:
        products = response.json().get('data', [])
        for product in products:
            click.echo(product)
    else:
        click.echo(f"Error: {response.json().get('message')}")

@click.command()
@click.option('--name', required=True, help='Name of the product.')
@click.option('--category', required=True, help='Category of the product.')
@click.option('--price', required=True, help='Price of the product.')
@click.option('--quantity', required=True, help='Quantity of the product.')
def addproduct(name, category, price, quantity):
    """Add new product"""
    data = {
        "name": name,
        "category": category,
        "price": price,
        "quantity": quantity
    }
    response = requests.post(f"{API_URL}/add-get-products", json=data)
    click.echo(response.json().get('message'))
    
@click.command()
@click.argument('product_id', type=int)
@click.option('--name', help='New name of the product.')
@click.option('--category', help='New category of the product.')
@click.option('--price', type=float, help='New price of the product.')
@click.option('--quantity', type=int, help='New quantity of the product.')
def updateproduct(product_id, name, category, price, quantity):
    """Update an existing product."""
    data = {}
    if name:
        data['name'] = name
    if category:
        data['category'] = category
    if price:
        data['price'] = price
    if quantity:
        data['quantity'] = quantity
    
    response = requests.put(f"{API_URL}/update-delete-product/{product_id}", json=data)
    click.echo(response.json().get('message'))
    
@click.command()
@click.argument('product_id', type=int)
def deleteproduct(product_id):
    """Delete a product"""
    response = requests.delete(f"{API_URL}/update-delete-product/{product_id}")
    click.echo(response.json().get('message'))
    
@click.command()
@click.option('--product_id', required=True, type=int, help='ID of the product.')
@click.option('--quantity', required=True, type=int, help='Quantity of the product sold.')
@click.option('--price', required=True, type=float, help='Price of the product sold.')
@click.option('--customer_id', required=True, type=int, help='ID of the customer.')
def sale(product_id, quantity, price, customer_id):
    """Record a sale."""
    """python3 -m app.cli record_sale --product_id 1 --quantity 5 --price 10.0 --customer_id 1
"""
    data = {
        "product_id": product_id,
        "quantity": quantity,
        "price": price,
        "customer_id": customer_id
    }
    response = requests.post(f"{API_URL}/sales", json=data)
    click.echo(response.json().get('message'))

@click.command()
@click.option('--product_id', required=True, type=int, help='ID of the product.')
@click.option('--quantity', required=True, type=int, help='Quantity of the product returned.')
@click.option('--price', required=True, type=float, help='Price of the product returned.')
@click.option('--reason', required=True, help='Reason for the return.')
def returnsale(product_id, quantity, price, reason):
    """Record a return."""
    data = {
        "product_id": product_id,
        "quantity": quantity,
        "price": price,
        "reason": reason
    }
    response = requests.post(f"{API_URL}/returns", json=data)
    click.echo(response.json().get('message'))

@click.command()
@click.option('--sale_ids', required=True, multiple=True, type=int, help='IDs of the sales to include in the invoice.')
def generateinvoice(sale_ids):
    """Generate an invoice."""
    data = {
        "sale_ids": list(sale_ids)
    }
    response = requests.post(f"{API_URL}/invoices/generate", json=data)
    if response.status_code == 200:
        with open('invoice.pdf', 'wb') as f:
            f.write(response.content)
        click.echo('Invoice generated successfully and saved as invoice.pdf')
    else:
        click.echo(response.json().get('message'))

cmd.add_command(getproducts)
cmd.add_command(addproduct)
cmd.add_command(updateproduct)
cmd.add_command(deleteproduct)
cmd.add_command(sale)
cmd.add_command(returnsale)
cmd.add_command(generateinvoice)

if __name__ == '__main__':
    cmd()