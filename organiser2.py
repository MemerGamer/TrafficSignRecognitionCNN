#!/bin/python

# This python organiser is made for the dataset/30kmh-traffic-sign and dataset/60kmh-traffic-sign
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


def process_folder(src_folder, dst_folder):
    create_folder(dst_folder)

    num_copied = 0

    # Copy images from the source folder to the destination folder with new UUID names
    for image_file in os.listdir(src_folder):
        src_path = os.path.join(src_folder, image_file)
        dst_path = os.path.join(dst_folder, str(uuid.uuid4()) + ".jpg")

        # Check if the destination file already exists
        if not os.path.exists(dst_path):
            shutil.copy(src_path, dst_path)
            num_copied += 1

    print(f"Copied {num_copied} new images to {dst_folder}")

    return num_copied


def update_csv_file(final_dataset_path, folder_name, num_images):
    csv_file = os.path.join(final_dataset_path, "info.csv")

    # Read the existing CSV data
    rows = []
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Find the row with the matching folder name and update the number of images
    for row in rows:
        if row[0] == folder_name:
            row[1] = str(int(row[1]) + num_images)
            break

    # Write the updated data back to the CSV file
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"Updated CSV file: {csv_file}")


def main():
    dataset_path = "dataset"
    final_dataset_path = os.path.join(dataset_path, "final_dataset")
    num_threads = 2  # Specify the number of threads to use

    # Create a list of tuples containing the source and destination folders
    folders = [
        ("30kmh-traffic-sign", "speed_limit_30kmh"),
        ("60kmh-traffic-sign", "speed_limit_60kmh"),
    ]

    # Use a ThreadPoolExecutor to process folders concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for src_folder_name, dst_folder_name in folders:
            src_folder = os.path.join(dataset_path, src_folder_name)
            dst_folder = os.path.join(final_dataset_path, dst_folder_name)
            future = executor.submit(process_folder, src_folder, dst_folder)
            futures.append((dst_folder_name, future))

        # Retrieve the results and update the CSV file
        for dst_folder_name, future in futures:
            num_copied = future.result()
            update_csv_file(final_dataset_path, dst_folder_name, num_copied)

    print("Dataset processing completed.")


if __name__ == "__main__":
    main()
