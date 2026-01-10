import pandas as pd
import glob
import os

def combine_csv_files(output_filename="aimo50Q&A_sources.csv"):
    # Explicit list of files to combine
    files_to_combine = [
        "20 IMO Questions.csv",
        "AIMO 1.csv",
        "AIMO 2.csv",
        "AIMO 3.csv"
    ]
    
    # Filter to ensure files exist before trying to read
    csv_files = [f for f in files_to_combine if os.path.exists(f)]
        
    if not csv_files:
        print("No specified CSV files found to combine.")
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
        
        
combine_csv_files()