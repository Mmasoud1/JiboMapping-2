import os
import pandas as pd

def combine_csv_files(input_folder, output_csv, output_excel, parent_folder):
    try:
        # Get all CSV file paths from the input folder
        csv_files = [
            os.path.join(input_folder, f)
            for f in os.listdir(input_folder)
            if f.endswith('.csv')
        ]
        
        # Sort files by timestamp extracted from the filenames
        csv_files.sort(
            key=lambda x: pd.to_datetime(
                os.path.basename(x).split('_')[1].replace('.csv', ''),
                format='%Y-%m-%d-%H-%M-%S'
            )
        )

        # Combine all CSV files into one DataFrame
        combined_df = pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True)

        # Save the combined DataFrame to CSV
        combined_df.to_csv(output_csv, index=False)
        print(f"Combined CSV saved to {output_csv}")

        # Save the combined DataFrame to Excel
        combined_df.to_excel(output_excel, index=False)
        print(f"Combined Excel saved to {output_excel}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def combine_csv_files_for_all_subjects(base_folder):
    try:
        # Get all subfolders in the base folder
        subfolders = [
            f for f in os.listdir(base_folder)
            if os.path.isdir(os.path.join(base_folder, f)) and f.endswith('-converted')
        ]

        parent_folder_name = os.path.basename(base_folder)

        for subfolder in subfolders:
            # Extract subject name from the folder name
            subject = subfolder.split('-converted')[0]

            # Define the input folder, output CSV path, and output Excel path
            input_folder = os.path.join(base_folder, subfolder)
            output_csv = os.path.join(base_folder, f"combined_{subject}.csv")
            output_excel = os.path.join(
                base_folder, f"combined_{subject}-{parent_folder_name}.xlsx"
            )

            # Combine CSV files in the current subfolder
            print(f"Processing folder: {subfolder}")
            combine_csv_files(input_folder, output_csv, output_excel, parent_folder_name)
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Base folder containing subject subfolders
base_folder = "../Subjects/converted-subjects"  # Replace with the path to your folder

combine_csv_files_for_all_subjects(base_folder)

