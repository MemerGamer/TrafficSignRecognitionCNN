#!/bin/python

# This python organiser is made for the dataset/Traffic-Signs-Dataset
# So that I can organise the data to my dataset/final_data folder with my own structure

import os
import shutil
import csv
import uuid
import concurrent.futures


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")


def process_class_folder(
    class_id, class_name, data_folder, test_folder, final_dataset_path
):
    print(f"Processing class: {class_name} (ID: {class_id})")
    data_class_folder = os.path.join(data_folder, class_id)
    test_class_folder = os.path.join(test_folder, class_id)

    # Create the new folder name
    if "unknown" in class_name.lower():
        new_folder_name = "unknown"
    else:
        new_folder_name = (
            class_name.lower()
            .replace(" ", "_")
            .replace("/", "")
            .replace("(", "")
            .replace(")", "")
        )
    new_folder_path = os.path.join(final_dataset_path, new_folder_name)
    create_folder(new_folder_path)

    # Copy images from the DATA folder
    for image_file in os.listdir(data_class_folder):
        src_path = os.path.join(data_class_folder, image_file)
        dst_path = os.path.join(new_folder_path, str(uuid.uuid4()) + ".jpg")
        shutil.copy(src_path, dst_path)

    # Copy images from the TEST folder
    for image_file in os.listdir(test_class_folder):
        src_path = os.path.join(test_class_folder, image_file)
        dst_path = os.path.join(new_folder_path, str(uuid.uuid4()) + ".jpg")
        shutil.copy(src_path, dst_path)

    return new_folder_name, class_name.lower().split()


def create_csv_file(final_dataset_path, folder_info):
    # Create a CSV file to store the folder information
    output_csv = os.path.join(final_dataset_path, "info.csv")
    with open(output_csv, "w", newline="") as file:
        writer = csv.writer(file)

        # Determine the maximum number of keywords
        max_keywords = max(len(info["keywords"]) for info in folder_info.values())

        # Write the header row with dynamic keyword columns
        header = ["Folder Name", "Number of Images"] + [
            f"Keyword{i+1}" for i in range(max_keywords)
        ]
        writer.writerow(header)

        # Sort the folder information by folder name in alphabetical order
        sorted_folder_info = sorted(folder_info.items(), key=lambda x: x[0])

        # Write the folder information to the CSV file
        for folder_name, info in sorted_folder_info:
            num_images = len(os.listdir(os.path.join(final_dataset_path, folder_name)))
            row = [folder_name, num_images] + info["keywords"]
            row += [""] * (
                max_keywords - len(info["keywords"])
            )  # Pad with empty values
            writer.writerow(row)

    print("CSV file created.")


def process_traffic_signs_dataset(dataset_path, final_dataset_path, num_threads):
    labels_file = os.path.join(dataset_path, "labels.csv")
    data_folder = os.path.join(dataset_path, "DATA")
    test_folder = os.path.join(dataset_path, "TEST")

    # Read the labels from the CSV file, skipping the header
    with open(labels_file, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        labels = {row[0]: row[1] for row in reader}

    # Create the final dataset folder if it doesn't exist
    create_folder(final_dataset_path)

    # Create a dictionary to store the folder information
    folder_info = {}

    # Use a ThreadPoolExecutor to process class folders concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for class_id, class_name in labels.items():
            future = executor.submit(
                process_class_folder,
                class_id,
                class_name,
                data_folder,
                test_folder,
                final_dataset_path,
            )
            futures.append(future)

        # Retrieve the results and update the folder information dictionary
        for future in concurrent.futures.as_completed(futures):
            new_folder_name, keywords = future.result()
            if new_folder_name in folder_info:
                folder_info[new_folder_name]["keywords"].extend(keywords)
            else:
                folder_info[new_folder_name] = {"keywords": keywords}

    # Create the CSV file after all folders and images are in place
    create_csv_file(final_dataset_path, folder_info)

    print("Dataset processing completed.")


def main():
    dataset_path = "dataset/Traffic-Signs-Dataset"
    final_dataset_path = "dataset/final_dataset"
    num_threads = 6  # Specify the number of threads to use
    process_traffic_signs_dataset(dataset_path, final_dataset_path, num_threads)


if __name__ == "__main__":
    main()
