import csv
from faker import Faker
import random

# Initialize Faker
faker = Faker()

# Number of rows to generate
num_rows = 100000

# Generate data
data = []
for i in range(1, num_rows + 1):
    row = {
        'id': i,
        'first_name': faker.first_name(),
        'last_name': faker.last_name(),
        'city': faker.city(),
        'occupation': faker.job(),
        'salary': random.randint(850, 3500)
    }
    data.append(row)

# Save to CSV using csv module
with open('user_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'first_name', 'last_name', 'city', 'occupation', 'salary']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"Generated {num_rows} rows of user data and saved to user_data.csv")
print("Sample rows:")
for row in data[:5]:
    print(row)