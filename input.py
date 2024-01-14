import pandas as pd

def analyze_employee_schedule(file_path):
    # Read the CSV file using pandas
    df = pd.read_excel(file_path)
    
     # Handling missing or invalid values
    df = df.dropna(subset=['Time', 'Time Out'])  # Drop rows with missing 'Time' or 'Time Out'

    # Convert 'Time' and 'Time Out' columns to datetime objects
    df['Time'] = pd.to_datetime(df['Time'])
    df['Time Out'] = pd.to_datetime(df['Time Out'])
    df['Timecard Hours (as Time)'] = pd.to_timedelta(df['Timecard Hours (as Time)'], errors='coerce')
    # Sort the dataframe by 'Employee Name' and 'Time' for better analysis
    df = df.sort_values(by=['Employee Name', 'Time'])

    # Initialize variables to store results
    consecutive_7_days = set()
    less_than_10_hours = set()
    more_than_14_hours = set()

    # Iterate through each employee's schedule
    for name, group in df.groupby('Employee Name'):
        shifts = group['Time']
        time_diff = shifts.diff().fillna(pd.Timedelta(seconds=0))
        

        # Check for employees who have worked for 7 consecutive days
        if any((time_diff > pd.Timedelta(days=0)) & (time_diff <= pd.Timedelta(days=1)).rolling(window=7).sum() == 7):
            consecutive_7_days.add(name)

        # Check for employees with less than 10 hours between shifts but greater than 1 hour
        if any((time_diff > pd.Timedelta(hours=1)) & (time_diff < pd.Timedelta(hours=10))):
            less_than_10_hours.add(name)
            
        if any((df['Timecard Hours (as Time)']) > pd.Timedelta(hours=14)):
            more_than_14_hours.add(name)

    # Display the results
    print("Employees who have worked for 7 consecutive days:", consecutive_7_days)
    print("Employees with less than 10 hours between shifts but greater than 1 hour:", less_than_10_hours)
    print("Employees who have worked for more than 14 hours in a single shift:", more_than_14_hours)
    
    with open("output.txt", "w") as output_file:
        output_file.write("Employees who have worked for 7 consecutive days:\n")
        output_file.write(str(consecutive_7_days) + "\n\n")

        output_file.write("Employees with less than 10 hours between shifts but greater than 1 hour:\n")
        output_file.write(str(less_than_10_hours) + "\n\n")

        output_file.write("Employees who have worked for more than 14 hours in a single shift:\n")
        output_file.write(str(more_than_14_hours))



analyze_employee_schedule("Assignment_Timecard.xlsx")
