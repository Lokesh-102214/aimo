import pandas as pd
import glob
import os

def combine_csv_files(output_filename="combined.csv"):
    # Get all CSV files in the current directory
    csv_files = glob.glob("*.csv")
    
    # Filter out the output file if it already exists to avoid reading it back in
    if output_filename in csv_files:
        csv_files.remove(output_filename)
        
    if not csv_files:
        print("No CSV files found to combine.")
        return

    print(f"Found {len(csv_files)} CSV files: {csv_files}")

    # List to hold dataframes
    dfs = []

    for filename in csv_files:
        try:
            df = pd.read_csv(filename)
            dfs.append(df)
            print(f"Read {filename} with {len(df)} rows.")
        except Exception as e:
            print(f"Error reading {filename}: {e}")

    if dfs:
        # Concatenate all dataframes
        combined_df = pd.concat(dfs, ignore_index=True)
        
        # Save to new CSV
        combined_df.to_csv(output_filename, index=False)
        print(f"Successfully combined {len(dfs)} files into {output_filename} with {len(combined_df)} total rows.")
        
        
combine_csv_files()# filepath: c:\Users\Lalit\OneDrive\Desktop\projects\kaagle\aimo\50 Question Reference\combine.py