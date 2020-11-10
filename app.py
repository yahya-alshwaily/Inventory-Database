from peewee import *
import datetime, os, sys, csv
from collections import OrderedDict

db = SqliteDatabase('inventory.db')

def initialize():
	db.connect()
	db.create_tables(([Products]), safe=True)

class Products(Model):
	product_id = IntegerField(unique=True, primary_key=True)
	product_name = TextField(unique=True)
	product_quantity = IntegerField(default=0)
	product_price = IntegerField(default=0)
	date_updated = DateTimeField(default=datetime.datetime.now)
	
	class Meta:
		database = db

def import_data():
	
	with open('inventory.csv') as csvfile:
		products_reader = csv.DictReader(csvfile, delimiter=',')
		products = list(products_reader)
	
		for product in products:
			product['product_price'] = product['product_price'][1:]
			product['product_price'] = float(product['product_price'])*100
			product['product_price'] = int(product['product_price'])
			product['date_updated'] = datetime.datetime.strptime(product['date_updated'], '%m/%d/%Y')
			
			try:
				Products.create(
					product_name=product['product_name'],
					product_quantity=product['product_quantity'],
					product_price=product['product_price'],
					date_updated=product['date_updated'],
				)
			except IntegrityError:
				product_record = Products.get(product_name=product['product_name'])
				product_record.product_name=product['product_name']
				product_record.save


def menu_choice():
	"""shows the menu and gets back a user-chosen item from the menu"""
	
	choice = None
	while choice != 'q'.lower().strip():
		print('Enter "q" to quit')
		
		for key, value in menu.items():
			print(f'{key}) {value.__doc__}')
			
		choice = input('Action: ').lower().strip()
		if choice in menu:
			menu[choice]()
		
		elif choice not in menu:
			print("Please enter one of the choices")
			continue
			
			
def clear():
	os.system('cls' if os.name =='nt' else 'clear')

	
def add_entry():
	"""Adds an entry to the products database"""
	
	product_name = input("Enter the product's name: ")
	while True:
		try:
			product_quantity = int(input("Enter the product's quantity: "))
			product_price = float(input("Enter the product's price: $ "))
			product_price = product_price*100
		except ValueError:
			print("Please Enter a valid value")
			continue
		break
	
	confirmation = input("Are you sure you want to save the product to the product's list?[y/n] ")
	if confirmation == 'y'.lower().strip():
		try:
			Products.create(product_name=product_name,
							product_quantity=product_quantity,
							product_price=product_price,
						    date_updated=datetime.datetime.now())
		except IntegrityError:
			product_record = Products.get(product_name=product_name)
			product_record.product_quantity=product_quantity
			product_record.product_price=product_price
			product_record.save
			
	clear()
	
	
def view_entry():
	"""shows an entry by it's product ID"""
	
	select_product = int(input('\nSelect the product number for more details: '))
	all_products = Products.select().order_by(Products.product_id)
	
	num_products = []
	for product in all_products:
		num_products.append(product.product_id)
		
	for product in all_products:
		if product.product_id == select_product:
			print(f'\n{product.product_id}) {product.product_name}\n')
	
	if str(select_product) not in str(product.product_id):
		print(f"Please Enter a value from 1 to {max(num_products)}")
			
	main_menu = input('Press Enter to go back to main-menu')
	clear()

	
def backup_entries():
	"""backs up all entries to the database"""
	
	with open('inventory_backup.csv', 'w') as csvfile:
		
		all_products = Products.select().order_by(Products.product_id)
		inventory_keeper = csv.DictWriter(csvfile, fieldnames= ['product_id', 'product_name', 'product_quantity', 'product_price', 'date_updated'])
		inventory_keeper.writeheader()
		for product in all_products:
			inventory_keeper.writerow({
					'product_name': f'{product.product_name}',
					'product_quantity': f'{product.product_quantity}',
					'product_price': f'{product.product_price}',
					'date_updated': "{}".format(product.date_updated.date().strftime("%m/%d/%Y")) })
			
	print("Back-Up complete!")
	main_menu = input('Press Enter to go back to main menu')
	clear()
	
				
menu = OrderedDict([
		('a', add_entry),
		('v', view_entry),
		('b', backup_entries)])
				
if __name__=='__main__':
	initialize()
	import_data()
	menu_choice()