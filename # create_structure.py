# create_structure.py
import os

# Define the base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Create directories
directories = [
    'earthquake_analysis',
    'data'
]

for directory in directories:
    dir_path = os.path.join(base_dir, directory)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")

# Create __init__.py in earthquake_analysis
init_file = os.path.join(base_dir, 'earthquake_analysis', '__init__.py')
if not os.path.exists(init_file):
    with open(init_file, 'w') as f:
        pass
    print(f"Created file: {init_file}")

print("\nDirectory structure created successfully!")