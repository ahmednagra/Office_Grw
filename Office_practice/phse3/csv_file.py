import csv

# 'r'	It opens a file for reading only.
# 'w'	It opens a file for writing. If the file exists, it overwrites it, otherwise, it creates a new file.
# 'a'	It opens a file for appending only. If the file doesn't exist, it creates the file.
# 'x'	It creates a new file. If the file exists, it fails.
# '+'	It opens a file for updating.


with open('Books.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        print(', '.join(row))

# Writing data into csv
#
data = [
    ['Title', 'Price'],
    ['Topology', '23'],
    ['c++', '22']
]
# Open the CSV file in write mode
with open('Books.csv', 'a', newline='') as file:
    # Create a CSV writer object
    writer = csv.writer(file)

    # Write the data to the CSV file
    for row in data:
        writer.writerow(row)
