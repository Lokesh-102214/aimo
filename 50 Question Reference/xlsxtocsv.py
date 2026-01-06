import pandas as pd

def convert_xlsx_to_csv(xlsx_file, csv_file):
    try:
        # Read the Excel file
        df = pd.read_excel(xlsx_file)
        
        # Write to CSV
        df.to_csv(csv_file, index=False)
        print(f"Successfully converted {xlsx_file} to {csv_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Replace these filenames with your actual files
    input_excel = "20 IMO Questions.xlsx" 
    output_csv = "20 IMO Questions.csv"
    convert_xlsx_to_csv(input_excel, output_csv)