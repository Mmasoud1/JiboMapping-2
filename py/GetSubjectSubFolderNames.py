import os

def save_subfolder_names_to_file(parent_folder, output_file):
    try:
        # Get all subfolder names in the specified folder
        subfolders = [name for name in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, name))]
        
        # Write the subfolder names to the text file
        with open(output_file, 'w') as file:
            for subfolder in subfolders:
                file.write(subfolder + '\n')
        
        print(f"Subfolder names saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the parent folder and output text file
parent_folder = "Subjects/c024"   # Name of the parent folder
output_file = "Subjects/c024_subfolderNames.txt"  # Output text file name

save_subfolder_names_to_file(parent_folder, output_file)

