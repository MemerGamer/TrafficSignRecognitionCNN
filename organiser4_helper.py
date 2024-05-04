#!/bin/python

# This python organiser is made for the dataset/Road-Sign-Detection-in-Real-Time-v3i-tensorflow
# So that I can organise the data to my dataset/final_data folder with my own structure

import os
import shutil
import csv
import uuid
import concurrent.futures
import re


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")


def process_annotations(annotations_file, temp_dataset_path):
    with open(annotations_file, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            if len(row) == 0:
                continue  # Skip empty lines

            filename, _, _, class_name, _, _, _, _ = row
            class_name = re.sub(r"[^a-zA-Z0-9]+", "_", class_name.lower())

            src_path = os.path.join(os.path.dirname(annotations_file), filename)
            dst_folder = os.path.join(temp_dataset_path, class_name)
            create_folder(dst_folder)

            dst_path = os.path.join(
                dst_folder, str(uuid.uuid4()) + os.path.splitext(filename)[1]
            )
            if not os.path.exists(dst_path):
                shutil.copy(src_path, dst_path)


def process_folder(folder_path, temp_dataset_path):
    annotations_file = os.path.join(folder_path, "_annotations.csv")
    process_annotations(annotations_file, temp_dataset_path)


def create_temp_info_csv(temp_dataset_path):
    temp_info_csv = os.path.join(temp_dataset_path, "temp_info.csv")
    rows = []

    for folder_name in os.listdir(temp_dataset_path):
        folder_path = os.path.join(temp_dataset_path, folder_name)
        if os.path.isdir(folder_path):
            num_images = len(os.listdir(folder_path))
            rows.append([folder_name, num_images])

    # Sort the rows by folder name
    rows.sort(key=lambda x: x[0])

    with open(temp_info_csv, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Folder Name", "Number of Images"])
        writer.writerows(rows)

    print(f"Created temp_info.csv: {temp_info_csv}")


def main():
    dataset_path = "dataset"
    folders = [
        os.path.join(
            dataset_path, "Road-Sign-Detection-in-Real-Time-v3i-tensorflow", "test"
        ),
        os.path.join(
            dataset_path, "Road-Sign-Detection-in-Real-Time-v3i-tensorflow", "train"
        ),
        os.path.join(
            dataset_path, "Road-Sign-Detection-in-Real-Time-v3i-tensorflow", "valid"
        ),
    ]
    temp_dataset_path = "dataset/temp_road_sign_dataset"
    num_threads = 6  # Specify the number of threads to use

    create_folder(temp_dataset_path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for folder_path in folders:
            future = executor.submit(process_folder, folder_path, temp_dataset_path)
            futures.append(future)

        concurrent.futures.wait(futures)

    create_temp_info_csv(temp_dataset_path)
    print("Image processing completed.")


if __name__ == "__main__":
    main()
