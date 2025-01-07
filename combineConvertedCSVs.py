import os
import pandas as pd

def combine_csv_files(input_folder, output_file):
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

        # Save the combined DataFrame to the output file
        combined_df.to_csv(output_file, index=False)
        print(f"Combined CSV saved to {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Define the folder containing CSV files and the output file path
input_folder = "Subjects/c024-converted-with-ASR-NoDuplicate"  # Replace with the path to your folder
output_file = "Subjects/combined_c024_w_ASR_NoDuplicate_ouputs.csv"       # Replace with the desired output filename

combine_csv_files(input_folder, output_file)

