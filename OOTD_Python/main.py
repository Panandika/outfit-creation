import pandas as pd
import json

# Function to load the category mapping from a text file
def load_category_mapping(file_path):
    mapping = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' ')
            if len(parts) == 2:
                mapping[int(parts[0])] = parts[1]
    return mapping

# Function to check if an outfit matches the specified criteria
def is_valid_outfit(outfit, outfit_type, category_mapping):
    required_items = outfit_type.get('required', [])
    optional_items = outfit_type.get('optional', [])
    items_in_outfit = set(category_mapping.get(id, '') for id in outfit['item_categoryid'].tolist())

    if not all(item in items_in_outfit for item in required_items):
        return False

    optional_count = sum(item in items_in_outfit for item in optional_items)
    return optional_count > 0

# Function to load and process each JSON file
def load_and_process_json(file_path, category_mapping):
    with open(file_path) as f:
        data = json.load(f)
    outfits = pd.json_normalize(data, 'items', ['set_id', 'set_url'],
                                record_prefix='item_')
    return process_outfits(outfits, category_mapping)

# Function to process outfits
def process_outfits(outfits, category_mapping):
    valid_outfits = []

    for set_id, outfit in outfits.groupby('set_id'):
        print(f"Processing outfit with set_id: {set_id}")
        categories = [category_mapping.get(id, '') for id in outfit['item_categoryid'].tolist()]
        print(f"Categories in outfit: {categories}")

        if is_valid_outfit(outfit, outfit_type_1, category_mapping):
            print("Valid outfit found (Type 1)")
            valid_outfits.append(outfit)
        elif is_valid_outfit(outfit, outfit_type_2, category_mapping):
            print("Valid outfit found (Type 2)")
            valid_outfits.append(outfit)
        else:
            print("Invalid outfit")

    if not valid_outfits:
        print("No valid outfits found")
        return pd.DataFrame()
    else:
        return pd.concat(valid_outfits).reset_index(drop=True)


# Load the category mapping
category_mapping = load_category_mapping('C:/Berkas Kuliah/SEMESTER 5/Bangkit/Project Plan/OOTD_Python/polyvore/category_id.txt')

# Define your outfit types using actual category names
outfit_type_1 = {'required': ['Dresses', 'Shoes', 'Bags'], 'optional': ['Outerwear']}
outfit_type_2 = {'required': ['Tops', 'Pants'], 'optional': ['Pullover', 'Outerwear']}

# File paths for the JSON files
train_file_path = 'C:/Berkas Kuliah/SEMESTER 5/Bangkit/Project Plan/OOTD_Python/polyvore/train_no_dup.json'
test_file_path = 'C:/Berkas Kuliah/SEMESTER 5/Bangkit/Project Plan/OOTD_Python/polyvore/test_no_dup.json'
valid_file_path = 'C:/Berkas Kuliah/SEMESTER 5/Bangkit/Project Plan/OOTD_Python/polyvore/valid_no_dup.json'

# Process each dataset
filtered_train_outfits = load_and_process_json(train_file_path, category_mapping)
filtered_test_outfits = load_and_process_json(test_file_path, category_mapping)
filtered_valid_outfits = load_and_process_json(valid_file_path, category_mapping)

# Save the datasets
filtered_train_outfits.to_csv('filtered_train_outfits.csv', index=False)
filtered_test_outfits.to_csv('filtered_test_outfits.csv', index=False)
filtered_valid_outfits.to_csv('filtered_valid_outfits.csv', index=False)
