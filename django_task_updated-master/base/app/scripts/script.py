from django.db import connection
from app.models import Client_model, Project_model
from django.contrib.auth.models import User
from pprint import pprint
import sqlparse


def run():
	def run():
		# Use select_related to join with the User model
		clients = Client_model.objects.select_related('created_by').all()

		# Get the raw SQL query for the queryset
		raw_sql = str(clients.query)

		# Format the SQL query using sqlparse
		formatted_sql = sqlparse.format(raw_sql, reindent=True, keyword_case='upper')

		# Print the formatted SQL query
		print("SQL Query with JOIN:")
		print(formatted_sql)

		# Print details of each client along with the related user
		for client in clients:
			print(f"Client Name: {client.client_name}, Created By: {client.created_by.username}")

	# Call the run function to execute the script
	run()