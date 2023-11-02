import PyPhenom as ppi
import math
import time
import csv
from datetime import datetime

def read_csv_file(file_path):
    # Open the CSV file
    with open(file_path, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        # Read the contents of the CSV file
        csv_contents = list(csv_reader)

    return csv_contents

#Convert csv data into matrix
def csv_to_matrix(csv_file):
    matrix = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row = [int(item) for item in row]  # Convert each item to an integer
            matrix.append(row)
    return matrix

# Usage

data = read_csv_file("data11.csv")

csv_path = 'data11.csv'
matrix = csv_to_matrix(csv_path)
size = len(matrix)

#IMPORTANT: x-coordinates = matrix[i][0], y-coordinates = matrix[i][1]

#This is the part where we access the x and y positions!

for i in range(size):
    print(f"{matrix[i][0],matrix[i][1]}") #This is only for demo purposes