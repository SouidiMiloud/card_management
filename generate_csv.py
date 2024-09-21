import csv

# Define the filename for the CSV file
filename = 'example_data.csv'

# Define the column headers
columns = [
    'country', 'description', 'price', 'exp_date', 'name', 'address', 'city', 
    'state', 'email', 'phone', 'dob', 'ssn', 'ip', 'bank_name', 'base', 
    'card_bin', 'status', 'level', 'credit_debit', 'card_zip', 'ua', 'refundable'
]

# Example data to fill in the CSV file
data = [
    ['USA', 'High-quality credit card', 100.00, '2025-12-31', 'John Doe', '123 Main St', 
     'New York', 'NY', 'johndoe@example.com', '123-456-7890', '1990-01-01', '123-45-6789', 
     '192.168.1.1', 'Bank of America', 'Gold', '123456', 'Active', 'Platinum', 'Credit', 
     '10001', 'Mozilla/5.0', 'Yes'],
    
    ['Canada', 'Virtual credit card', 80.00, '2024-11-30', 'Jane Smith', '456 Maple Ave', 
     'Toronto', 'ON', 'janesmith@example.ca', '987-654-3210', '1985-02-14', '987-65-4321', 
     '192.168.1.2', 'TD Bank', 'Silver', '654321', 'Active', 'Gold', 'Debit', 
     'M5H 2N2', 'Mozilla/5.0', 'No'],
    
    ['UK', 'Premium bank account', 150.00, '2023-10-15', 'Alice Johnson', '789 Oak Blvd', 
     'London', 'LDN', 'alicejohnson@example.co.uk', '555-555-5555', '1970-03-20', '456-78-9012', 
     '192.168.1.3', 'HSBC', 'Platinum', '789012', 'Inactive', 'Gold', 'Credit', 
     'EC1A 1BB', 'Mozilla/5.0', 'Yes'],
    
    ['Germany', 'Exclusive credit line', 200.00, '2026-09-25', 'Max Müller', '321 Elm Str', 
     'Berlin', 'BE', 'maxmuller@example.de', '030-123456', '1992-04-18', '321-98-7654', 
     '192.168.1.4', 'Deutsche Bank', 'Diamond', '890123', 'Active', 'Platinum', 'Credit', 
     '10115', 'Mozilla/5.0', 'Yes'],
    
    ['Australia', 'Basic checking account', 50.00, '2025-05-10', 'David Brown', '654 Pine Rd', 
     'Sydney', 'NSW', 'davidbrown@example.au', '0412-345-678', '1988-07-07', '210-12-3456', 
     '192.168.1.5', 'ANZ Bank', 'Basic', '567890', 'Active', 'Silver', 'Debit', 
     '2000', 'Mozilla/5.0', 'No'],
    
    ['France', 'Luxury savings account', 300.00, '2024-03-05', 'Claire Dubois', '987 Cedar Ct', 
     'Paris', 'PA', 'clairedubois@example.fr', '06-12345678', '1995-08-30', '789-01-2345', 
     '192.168.1.6', 'BNP Paribas', 'Elite', '345678', 'Inactive', 'Gold', 'Credit', 
     '75001', 'Mozilla/5.0', 'Yes']
]

# Write data to the CSV file
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(columns)  # Write the column headers
    writer.writerows(data)    # Write the example rows

print(f"CSV file '{filename}' has been created with example data.")
