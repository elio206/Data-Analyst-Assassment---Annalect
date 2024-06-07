import pandas as pd

# Define file paths
input_file_path = "C:/Users/User/Desktop/Elio's File/Data Analyst Assessment - Annalect/Elio's Assessment/Part 2 – Data Cleaning and Manipulation/Digital Performance Data.xlsx"
# Output_file_path is specified each time : we have 3
# Output_file_path_1 : for the Merged Data ( combining sheet 1 and sheet 2)
# Output_file_path_2 : for the Merged Cleaned Slipted Data ( Merged Data + Spliting "campaign" + Cleaned)
# Output_file_path_3 : for the Final Data to visualize it ( Digital Performance data - Elio Bou serhal)

#################################################################################################
### QUESTION 1-1: Write a commented Python code to read data from the provided files 
### QUETION 1-2: Join the two raw data files in “Digital Performance Data” by idenƟfying 
#                  the join type and column to unify them into one dataset
#################################################################################################



##### ANSWER : Question 1-1: READ THE 2 DATA SETS
# Step 1:Import 1st Data sheet: Raw Data 1
# Step 2:Import 2nd Data Sheet : Raw Data
##### ANSWER : Question 1-1: READ THE 2 DATA SETS
# Read the data from the Excel file for the first sheet
df1 = pd.read_excel(input_file_path, sheet_name="Raw Data 1")
print("\nFirst DataFrame (df1):")
print(df1.head())

# Read the data from the Excel file for the second sheet
df2 = pd.read_excel(input_file_path, sheet_name="Raw Data")
print("\nSecond DataFrame (df2):")
print(df2.head())



### ANSWER : Question 1-2: JOIN THE 2 DATA SETS
# step 1:Merge the two tables based on "Date" and "Campaign" columns using "Outer join" to select them all.
# step 2: Check the Merged data set (Remove Duplicates and work with the cleaned merged new data)
# step 3: Save the merged dataframe to a new Excel file
##### ANSWER : Question 1-2: JOIN THE 2 DATA SETS
# Merge the two tables based on "Date" and "Campaign" columns using "Outer join"
merged_df = pd.merge(df1, df2, on=["Date", "Campaign"], how="outer")

# Drop duplicate rows based on all columns
merged_df.drop_duplicates(inplace=True)

# Reset the index after dropping duplicates
merged_df.reset_index(drop=True, inplace=True)
print("Merged DataFrame without duplicates:")
print(merged_df.head())

# Save the merged dataframe to a new Excel file
output_file_path_2 = "C:/Users/User/Desktop/Elio's File/Data Analyst Assessment - Annalect/Elio's Assessment/Part 2 – Data Cleaning and Manipulation/Merged Data.xlsx"
merged_df.to_excel(output_file_path_2, index=False)
print(f"Cleaned data exported to {output_file_path_2}")







#################################################################################################
### QUESTION 2: Advise on a simple quality assurance method to demonstrate the validity of the joined dataset. 
# Step 1: Check for missing values in the Merged Data (for rows)
# Step 2: Check for missing Columns in the Merged Data (for columns)
# Step 3: Check for type and Uniquness in the Merged Data (for rows)
# Step 4: Check for type and Uniquness in the Merged Data (for columns)
#################################################################################################

##### ANSWER : Question 2: Simple quality assurance method
# Check for missing values in the Merged Data #
null_values = merged_df.isnull().sum()
if null_values.any():
    print("Null values found in the merged dataset:")
    print(null_values)
else:
    print("No null values found in the merged dataset.")

# Check for missing columns in the Merged Data
expected_columns = ['Date', 'Campaign', 'Installs', 'Sessions', 'Sign-Ups', 'Spends', 'Impressions', 'Clicks']
missing_columns = [col for col in expected_columns if col not in merged_df.columns]
if missing_columns:
    print("Missing columns in the merged dataset:", missing_columns)
else:
    print("All expected columns are present in the merged dataset.")

# Check for duplicate rows in the Merged Data
duplicate_rows = merged_df.duplicated().sum()
if duplicate_rows:
    print("Duplicate rows found in the merged dataset:", duplicate_rows)
else:
    print("No duplicate rows found in the merged dataset.")

# Check data types and unique values for each column
for col in merged_df.columns: 
    print("Column:", col)
    print("Data type:", merged_df[col].dtype)
    print("Unique values:", merged_df[col].unique())
    print()







###########################################################################################################
# QUESTION 3: Create six new columns, each representing a dimension available in the taxonomy. Use the 
#             split method to extract the dimensions from the appropriate column.
# Step 1: Create six new columns by splitting the "Campaign" column Define a function to split and pad/truncate the results
# Step 2: Apply the function to the 'Campaign' column
# Step 3: Assign the split columns back to the original dataframe
# Step 4: Drop the original 'Campaign' column
# Step 5: Save the updated DataFrame to a new Excel file #



##### ANSWER : Question 3: Create six new columns by splitting the "Campaign" column
# Define a function to split and pad/truncate the results #
def split_and_adjust(campaign):
    parts = campaign.split('_')
    if len(parts) == 6:
        return parts
    elif len(parts) < 6:
        return parts + [None] * (6 - len(parts))
    else:
        return parts[:6]

# Apply the function to the 'Campaign' column
split_columns = merged_df['Campaign'].apply(split_and_adjust)
split_df = pd.DataFrame(split_columns.tolist(), columns=['Channel', 'Platform', 'Destination', 'Market', 'Objective', 'ProductType'])

# Assign the split columns back to the original dataframe
merged_df[['Channel', 'Platform', 'Destination', 'Market', 'Objective', 'ProductType']] = split_df

# Drop the original 'Campaign' column
merged_df.drop(columns=['Campaign'], inplace=True)

# Display the updated dataframe
print("Updated DataFrame with split 'Campaign' column:")
print(merged_df.head())

# Save the updated DataFrame to a new Excel file
output_file_path_3 = "C:/Users/User/Desktop/Elio's File/Data Analyst Assessment - Annalect/Elio's Assessment/Part 2 – Data Cleaning and Manipulation/Merged_Cleaned_Splited Data.xlsx"
merged_df.to_excel(output_file_path_3, index=False)
print(f"Cleaned data exported to {output_file_path_3}")








############################################################################################################
# QUESTION 4:  Extend the script to create two addiƟonal columns, "Start Date" and "End Date," that capture 
#              the start and end dates for each campaign based on the relevant columns in the dataset. 
# Step 1: Converting the values in the 'Date' column to datetime format
# Step 2: Group by 'Campaigns' and aggregate to find the sum of "clicks, Installs" and mean of "sign-ups"
# Step 3: Calculate the Cost per Mile percentage (CPM)
############################################################################################################


##### ANSWER : Question 4: Create 'Start Date' and 'End Date' columns
# Step 1: Converting the values in the 'Date' column to datetime format
merged_df['Date'] = pd.to_datetime(merged_df['Date'])

# Step 2: Group by 'Market', 'Channel', 'Platform', 'Destination', 'Objective', 'ProductType' and aggregate
df_aggregated = merged_df.groupby(['Market', 'Channel', 'Platform', 'Destination', 'Objective', 'ProductType']).agg({
    'Date': ['min', 'max'],
    'Spends': 'sum',
    'Impressions': 'sum',
    'Clicks': 'sum',
    'Installs': 'sum',
    'Sign-Ups': 'mean'
}).reset_index()

# Step 3: Calculate the Cost per Mile (CPM)
df_aggregated['CPM'] = (df_aggregated[('Spends', 'sum')] / df_aggregated[('Impressions', 'sum')]) * 1000

# Step 4: Flatten the MultiIndex columns
df_aggregated.columns = ['Market', 'Channel', 'Platform', 'Destination', 'Objective', 'ProductType', 'Start Date', 'End Date', 'Total Spends', 'Total Impressions', 'Total Clicks', 'Total Installs', 'Average Sign-Ups', 'CPM']

# Display the aggregated dataframe
print("Aggregated DataFrame with 'Start Date' and 'End Date' columns:")
print(df_aggregated.head())

# Save the aggregated DataFrame to a new Excel file
output_file_path_4 = "C:/Users/User/Desktop/Elio's File/Data Analyst Assessment - Annalect/Elio's Assessment/Part 2 – Data Cleaning and Manipulation/Merged_Cleaned_Splited_Aggregated Data.xlsx"
df_aggregated.to_excel(output_file_path_4, index=False)
print(f"Aggregated data exported to {output_file_path_4}")








############################################################################################################
###############################################################################################################
# QUESTION 6: Save the file as CSV under the following name “Cleaned Digital Performance Data – {Your Name}”
###############################################################################################################
### ANSWER : Saving the cleaned Merged data 
output_file_path_5 = "C:/Users/User/Desktop/Elio's File/Data Analyst Assessment - Annalect/Elio's Assessment/Part 2 – Data Cleaning and Manipulation/Cleaned Digital Performance Data – Elio Bou Serhal.xlsx"
df_aggregated.to_excel(output_file_path_5,index=False)
print(f"Aggregated data exported to {output_file_path_5}")












###############################################################################################################
#### QUESTION 5:Using a SQL library (such as pandasql) in Python, execute an SQL query on the data to:
##  a. IdenƟfy and display the campaigns with the highest and lowest Cost per Mille (CPM).
##  b. Calculate the total Spends for each product type.
##  c. Determine the average daily sign-ups in each market.

###############################################################################################################
## ANSWER:5-1 Identify and display the campaigns with the highest and lowest Cost per Mille (CPM): 
from pandasql import sqldf

# Define the SQL query to identify the campaigns with highest and lowest CPM
sql_query_a = """
SELECT *
FROM df_aggregated
WHERE CPM = (SELECT MAX(CPM) FROM df_aggregated) OR CPM = (SELECT MIN(CPM) FROM df_aggregated);
"""
# Execute the SQL query
result_a = sqldf(sql_query_a, globals())
print("Campaigns with highest and lowest CPM:")
print(result_a)


###############################################
## ANSWER:5-2 Calculate the total Spends for each product type:
# Define the SQL query to calculate total Spends for each product type
# Define the SQL query to calculate total Spends for each product type
sql_query_b = """
SELECT ProductType, SUM(`Total Spends`) AS Total_Spends
FROM df_aggregated
GROUP BY ProductType;
"""
# Execute the SQL query
result_b = sqldf(sql_query_b, globals())
print("\nTotal Spends for each product type:")
print(result_b)



###############################################
# ANSWER:5-3 Determine the average daily sign-ups in each market:
# Define the SQL query to determine average daily sign-ups in each market
sql_query_c = """
SELECT Market, AVG(`Average Sign-Ups`) AS Avg_Daily_SignUps
FROM df_aggregated
GROUP BY Market;
"""
# Execute the SQL query
result_c = sqldf(sql_query_c, globals())
print("\nAverage daily sign-ups in each market:")
print(result_c)














