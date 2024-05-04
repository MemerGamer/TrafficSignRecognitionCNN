#!/bin/python

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


def load_category_names(file_path):
    category_names = {}
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            category, category_name = row
            category_names[int(category)] = category_name
    return category_names


def process_image(
    image_file, category, category_names, images_folder, final_dataset_path
):
    category_name = category_names.get(category)

    if category_name:
        src_path = os.path.join(images_folder, image_file)
        dst_folder = os.path.join(final_dataset_path, category_name)
        create_folder(dst_folder)

        dst_path = os.path.join(dst_folder, str(uuid.uuid4()) + ".png")
        shutil.copy(src_path, dst_path)


def process_images(
    images_folder, annotations_file, category_names, final_dataset_path, num_threads
):
    with open(annotations_file, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for row in reader:
                image_file, _, _, _, _, _, _, category = row
                category = int(category)
                future = executor.submit(
                    process_image,
                    image_file,
                    category,
                    category_names,
                    images_folder,
                    final_dataset_path,
                )
                futures.append(future)

            concurrent.futures.wait(futures)

    print("Image processing completed.")


def update_csv_file(final_dataset_path):
    csv_file = os.path.join(final_dataset_path, "info.csv")

    # Read the existing CSV data
    rows = []
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Update the number of images for each category
    for row in rows:
        folder_name = row[0]
        folder_path = os.path.join(final_dataset_path, folder_name)
        if os.path.exists(folder_path):
            num_images = len(os.listdir(folder_path))
            row[1] = str(num_images)

    # Write the updated data back to the CSV file
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"Updated CSV file: {csv_file}")


def main():
    dataset_path = "dataset"
    images_folder = os.path.join(dataset_path, "Chinese-Traffic-Signs", "images")
    annotations_file = os.path.join(
        dataset_path, "Chinese-Traffic-Signs", "annotations.csv"
    )
    category_names_file = "annotations_category_names.csv"
    final_dataset_path = os.path.join(dataset_path, "final_dataset")
    num_threads = 4  # Specify the number of threads to use

    category_names = load_category_names(category_names_file)
    process_images(
        images_folder, annotations_file, category_names, final_dataset_path, num_threads
    )
    update_csv_file(final_dataset_path)


if __name__ == "__main__":
    main()
