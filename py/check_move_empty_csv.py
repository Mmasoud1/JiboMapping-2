"""
Description:
This script processes a parent folder containing multiple subject folders (e.g., c000, c001).
Each subject folder contains subfolders, which may include two CSV files:
- storybook_command.csv
- storybook_event.csv.

The script:
1. Checks if the CSV files are empty or missing in each subfolder.
2. Moves subfolders with empty/missing CSV files into a new folder called `empty-{subject}`.
3. Creates a log file `empty-{subject}.txt` for each subject with details of moved subfolders.
4. Creates a global log file `empty-{parent_folder}.txt` summarizing all subjects and subfolders processed.
5. Calculates the total number of remaining subfolders in all subjects after processing.

How to Use:
1. Place this script in the directory or provide the absolute path to the parent folder.
2. Run the script:
   $ python <script_name>.py
3. Enter the path to the parent folder when prompted.

Example:
Parent Folder: Subjects/kipp_stations
Subjects: c000, c001
Output:
- Logs in `empty-{subject}` folders (e.g., empty-c000/empty-c000.txt).
- A global log file: `empty-kipp_stations.txt` in the parent folder.
- Total remaining subfolders count in the console and global log.
"""



import os
import shutil
import pandas as pd


def is_csv_empty(file_path):
    """
    Check if a CSV file is empty (contains no rows, ignoring headers) or is completely empty.
    """
    with open(file_path, 'r') as f:
        content = f.read().strip()  # Remove any leading/trailing whitespace or newlines

    if not content:  # File is empty or contains only whitespace
        return True
    else:
        return False


def check_and_move_empty_folders_for_subject(subject_folder, parent_folder, global_log):
    """
    Check a single subject folder for empty CSV files and move subfolders with empty files
    to a new folder called 'empty-{subject}'.
    Write the results to a text file named empty-{subject}.txt and append the contents to the global log file.
    """
    subject_name = os.path.basename(subject_folder)
    empty_folder = os.path.join(parent_folder, f"empty-{subject_name}")
    os.makedirs(empty_folder, exist_ok=True)

    # Create the log file
    log_file_path = os.path.join(empty_folder, f"empty-{subject_name}.txt")
    with open(log_file_path, 'w') as log_file:
        log_file.write(f"Parent Folder: {parent_folder}\n")
        log_file.write(f"Subject: {subject_name}\n\n")
        log_file.write("Subfolders with empty CSV files:\n")

        for subfolder in os.listdir(subject_folder):
            subfolder_path = os.path.join(subject_folder, subfolder)

            if os.path.isdir(subfolder_path):
                command_file = os.path.join(subfolder_path, "storybook_command.csv")
                event_file = os.path.join(subfolder_path, "storybook_event.csv")

                move_subfolder = False
                empty_files = []

                # Check if `storybook_command.csv` is empty
                if os.path.isfile(command_file):
                    if is_csv_empty(command_file):
                        empty_files.append("storybook_command.csv")
                        move_subfolder = True
                else:
                    empty_files.append("Missing: storybook_command.csv")

                # Check if `storybook_event.csv` is empty
                if os.path.isfile(event_file):
                    if is_csv_empty(event_file):
                        empty_files.append("storybook_event.csv")
                        move_subfolder = True
                else:
                    empty_files.append("Missing: storybook_event.csv")

                if move_subfolder:
                    shutil.move(subfolder_path, empty_folder)
                    log_file.write(f"- {subfolder}: {', '.join(empty_files)}\n")

        # Add the contents of the subject log to the global log
        with open(log_file_path, 'r') as subject_log:
            global_log.write(subject_log.read())
            global_log.write("\n")

    # Count remaining subfolders in the subject
    remaining_subfolders = len([d for d in os.listdir(subject_folder) if os.path.isdir(os.path.join(subject_folder, d))])
    return remaining_subfolders


def check_all_subjects_in_parent_folder(parent_folder):
    """
    Navigate through all subject folders in the parent folder and check for empty CSV files
    in each subject.
    Create a global log file for the entire parent folder.
    """
    parent_name = os.path.basename(parent_folder)
    global_log_path = os.path.join(parent_folder, f"empty-{parent_name}.txt")

    total_remaining_subfolders = 0

    with open(global_log_path, 'w') as global_log:
        global_log.write(f"Global Log for Parent Folder: {parent_folder}\n")
        global_log.write("=" * 50 + "\n\n")

        for subject_folder in os.listdir(parent_folder):
            subject_path = os.path.join(parent_folder, subject_folder)

            if os.path.isdir(subject_path):  # Only process directories
                print(f"Processing subject: {subject_folder}")
                remaining_subfolders = check_and_move_empty_folders_for_subject(subject_path, parent_folder, global_log)
                total_remaining_subfolders += remaining_subfolders

        # Append total remaining subfolders to the global log
        global_log.write("\n" + "=" * 50 + "\n")
        global_log.write(f"Total Remaining Subfolders in All Subjects: {total_remaining_subfolders}\n")

    print(f"Global log written to {global_log_path}")
    print(f"Total Remaining Subfolders: {total_remaining_subfolders}")


if __name__ == "__main__":
    # Specify the path to the parent folder containing subjects
    parent_folder_path = input("Enter the path to the parent folder: ").strip()

    if os.path.exists(parent_folder_path) and os.path.isdir(parent_folder_path):
        check_all_subjects_in_parent_folder(parent_folder_path)
    else:
        print("Invalid folder path. Please check and try again.")

