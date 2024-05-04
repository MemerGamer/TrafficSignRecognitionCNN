#!/bin/python

# This python organiser is made for the dataset/Road-Sign-Detection-in-Real-Time-v3i-tensorflow
# So that I can organise the data to my dataset/final_data folder with my own structure

import os
import shutil
import csv
import concurrent.futures
import uuid


# Hardcoded mapping between temp_road_sign_dataset and final_dataset folders
folder_mapping = {
    "barrier_ahead": "barrier_ahead",
    "cattle": "cattle",
    "caution": "caution",
    "cycle_crossing": "bicycles_crossing",
    "dangerous_dip": "dangerous_dip",
    "eating_place": "eating_place",
    "falling_rocks": "falling_rocks",
    "ferry": "ferry",
    "first_aid_post": "first_aid_post",
    "give_way": "give_way",
    "horn_prohibited": "no_horn",
    "hospital": "hospital",
    "hump": "hump",
    "left_hair_pin_bend": "left_hair_pin_bend",
    "left_hand_curve": "left_hand_curve",
    "left_reverse_bend": "left_reverse_bend",
    "light_refreshment": "light_refreshment",
    "men_at_work": "under_construction",
    "narrow_bridge": "narrow_bridge",
    "narrow_road_ahead": "narrow_road_ahead",
    "no_parking": "no_parking",
    "no_stopping": "no_stopping",
    "no_thorough_road": "no_thorough_road",
    "no_thorough_sideroad": "no_thorough_sideroad",
    "parking_lot_cars": "parking_lot_cars",
    "parking_lot_cycle": "parking_lot_cycle",
    "parking_lot_scooter_and_motorcycle": "parking_lot_scooter_and_motorcycle",
    "parking_this_side": "parking_this_side",
    "pedestrian_crossing": "zebra_crossing",
    "pedestrian_prohibited": "pedestrian_prohibited",
    "petrol_pump_gas_station": "petrol_pump_gas_station",
    "public_telephone": "public_telephone",
    "resting_place": "resting_place",
    "right_hair_pin_bend": "right_hair_pin_bend",
    "right_hand_curve": "right_hand_curve",
    "right_reverse_bend": "right_reverse_bend",
    "road_wideness_ahead": "road_wideness_ahead",
    "round_about": "roundabout_mandatory",
    "school_ahead": "children_crossing",
    "slippery_road": "slippery_road",
    "speed_limit_100_": "speed_limit_100kmh",
    "speed_limit_10_": "speed_limit_10kmh",
    "speed_limit_110_": "speed_limit_110kmh",
    "speed_limit_120_": "speed_limit_120kmh",
    "speed_limit_130_": "speed_limit_130kmh",
    "speed_limit_140_": "speed_limit_140kmh",
    "speed_limit_150_": "speed_limit_150kmh",
    "speed_limit_15_": "speed_limit_15kmh",
    "speed_limit_160_": "speed_limit_160kmh",
    "speed_limit_20_": "speed_limit_20kmh",
    "speed_limit_25_": "speed_limit_25kmh",
    "speed_limit_3": "speed_limit_3kmh",
    "speed_limit_30": "speed_limit_30kmh",
    "speed_limit_35_": "speed_limit_35kmh",
    "speed_limit_40_": "speed_limit_40kmh",
    "speed_limit_45_": "speed_limit_45kmh",
    "speed_limit_48_": "speed_limit_48kmh",
    "speed_limit_50_": "speed_limit_50kmh",
    "speed_limit_55_": "speed_limit_55kmh",
    "speed_limit_5_": "speed_limit_5kmh",
    "speed_limit_60_": "speed_limit_60kmh",
    "speed_limit_65_": "speed_limit_65kmh",
    "speed_limit_70_": "speed_limit_70kmh",
    "speed_limit_75_": "speed_limit_75kmh",
    "speed_limit_80_": "speed_limit_80kmh",
    "speed_limit_8_": "speed_limit_8kmh",
    "speed_limit_90_": "speed_limit_90kmh",
    "steep_ascent": "steep_ascent",
    "steep_desecnt": "steep_descent",
    "stop": "stop",
    "straight_prohibitor_no_entry": "dont_go_straight",
    "walking": "walking",
}


def copy_images(src_folder, dst_folder):
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    for image_file in os.listdir(src_folder):
        src_path = os.path.join(src_folder, image_file)
        file_name, file_ext = os.path.splitext(image_file)
        unique_file_name = f"{file_name}_{str(uuid.uuid4())}{file_ext}"
        dst_path = os.path.join(dst_folder, unique_file_name)
        shutil.copy(src_path, dst_path)


def process_folder(temp_folder, final_dataset_path):
    if temp_folder in folder_mapping:
        final_folder = folder_mapping[temp_folder]
        src_folder = os.path.join("dataset", "temp_road_sign_dataset", temp_folder)
        dst_folder = os.path.join(final_dataset_path, final_folder)
        copy_images(src_folder, dst_folder)
    else:
        src_folder = os.path.join("dataset", "temp_road_sign_dataset", temp_folder)
        dst_folder = os.path.join(final_dataset_path, temp_folder)
        copy_images(src_folder, dst_folder)


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

    rows.sort(key=lambda x: x[0])  # Sort rows by folder name

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

    print(f"Created info.csv: {info_csv_path}")


def main():
    temp_dataset_path = "dataset/temp_road_sign_dataset"
    final_dataset_path = "dataset/final_dataset"
    num_threads = 6  # Specify the number of threads to use

    print("Image processing started...")
    print("Opening temp_info.csv...")
    with open(temp_dataset_path + "/temp_info.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        temp_folders = [row[0] for row in reader]

    print("Copying images...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for temp_folder in temp_folders:
            future = executor.submit(process_folder, temp_folder, final_dataset_path)
            futures.append(future)

        concurrent.futures.wait(futures)

    create_info_csv(final_dataset_path)
    print("Image processing completed.")


if __name__ == "__main__":
    main()
