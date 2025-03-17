import requests
import pandas as pd
import time

# API Endpoint
URL = "https://api.slingacademy.com/v1/sample-data/files/employees.json"

# Function to fetch employee data 
def fetch_emp_data():
    for _ in range(3):  # Retry up to 3 times
        try:
            response = requests.get(URL, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data if isinstance(data, list) else []  #  list
            else:
                print(f"Error: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

        time.sleep(3) 
    return None

#  normalize data
def process_emp_data():
    data = fetch_emp_data()
    if not data:
        print("Failed to retrieve employee data.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(data)

    
    required_columns = [
        "first_name", "last_name", "email", "phone", "gender",
        "age", "job_title", "years_of_experience", "salary", "department"
    ]
    
    
    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    #  Add "Full Name" column
    df["Full Name"] = df["first_name"].fillna('') + " " + df["last_name"].fillna('')

    df.drop(columns=["first_name", "last_name"], inplace=True)

    # Assign "designation" based on years of experience
    def get_designation(exp):
        if pd.isna(exp): 
            return "Unknown"
        if exp < 3: 
            return "System Engineer"
        elif 3 <= exp <= 5: 
            return "Data Engineer"
        elif 5 < exp <= 10: 
            return "Senior Data Engineer"
        else: 
            return "Lead"

    df["Designation"] = df["years_of_experience"].apply(get_designation)

    #  Mark invalid phone numbers
    df["phone"] = df["phone"].astype(str).apply(lambda x: "Invalid Number" if "x" in x else x)

    # Convert data types (handling missing values)
    df = df.astype({
        "Full Name": "string",
        "email": "string",
        "phone": "string",
        "gender": "string",
        "age": "Int64",  
        "job_title": "string",
        "years_of_experience": "Int64",
        "salary": "Int64",
        "department": "string"
    })

    columns = df.columns.tolist()
    if "id" in columns and "Full Name" in columns:
        columns.remove("Full Name")
        id = columns.index("id") + 1
        columns.insert(id, "Full Name")
        df = df[columns]

    # Save to CSV
    df.to_csv("emp.csv", index=False)
    print("Data successfully saved to emp.csv")

# Run the scraper
process_emp_data()


import pandas as pd

df = pd.read_csv("emp.csv")
print(df)  # Prints table in the console
