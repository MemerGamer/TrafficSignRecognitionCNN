#!/bin/python
import os
import csv


def create_info_csv(final_dataset_path):
    info_csv_path = os.path.join(final_dataset_path, "info.csv")
    rows = []

    for folder_name in os.listdir(final_dataset_path):
        folder_path = os.path.join(final_dataset_path, folder_name)
        if os.path.isdir(folder_path):
            num_images = len(os.listdir(folder_path))
            keywords = folder_name.split("_")
            row = [folder_name, num_images] + keywords
            rows.append(row)

    rows.sort(
        key=lambda x: x[1], reverse=True
    )  # Sort rows by number of images in descending order

    with open(info_csv_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Folder Name",
                "Number of Images",
                "Keyword1",
                "Keyword2",
                "Keyword3",
                "Keyword4",
                "Keyword5",
                "Keyword6",
                "Keyword7",
            ]
        )
        writer.writerows(rows)

    print(f"Updated info.csv: {info_csv_path}")


def main():
    final_dataset_path = "dataset/final_dataset"
    create_info_csv(final_dataset_path)


if __name__ == "__main__":
    main()
