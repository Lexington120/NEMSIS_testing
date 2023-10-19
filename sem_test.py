import pandas as pd
import random

# Load the Excel file
file_path = "data.xlsx"
sheet_name = "Sheet1"  # Change to the appropriate sheet name if needed
column_name = "C"     # Change to the column name you want to extract

# Read the Excel file into a DataFrame
df = pd.read_excel(file_path)
# print(df)

# Get the number of rows in the DataFrame
num_rows = df.shape[0]
# print(num_rows)

# Choose 10 random row indices
random_indices = random.sample(range(num_rows), 10)
# print(random_indices)

# selected_text = df.iloc[random_indices, column_name].tolist()
selected_text = df.iloc[(random_indices,2)]
print(selected_text)
print(type(selected_text))

# convert series to list
data_list = list(selected_text)
print(data_list)


# # Extract text from the specified column (column C) for the selected rows
# selected_text = df.iloc[random_indices, column_name].tolist()

# # Print the extracted text
# for text in selected_text:
#     print(text)
