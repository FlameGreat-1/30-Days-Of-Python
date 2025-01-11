import os
import nbformat

# Define the base path
base_path = '/storage/emulated/0/30-days-of-python'

# Create a 'notebooks' folder
notebooks_path = os.path.join(base_path, 'notebooks')
os.makedirs(notebooks_path, exist_ok=True)

# Create folders, notebook files, and Documentation folders for each day
for day in range(1, 31):
    # Create day folder
    day_folder = os.path.join(notebooks_path, f'day_{day:02d}')
    os.makedirs(day_folder, exist_ok=True)
    
    # Create an empty notebook
    notebook_path = os.path.join(day_folder, f'day_{day:02d}_challenge.ipynb')
    
    # Create a notebook with a markdown cell
    nb = nbformat.v4.new_notebook()
    text = f"# Day {day} Challenge\n\n## Topics:\n\n## Exercises:\n\n## Notes:"
    nb['cells'] = [nbformat.v4.new_markdown_cell(text)]
    
    # Write the notebook to a file
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    
    # Create Documentation folder
    documentation_folder = os.path.join(day_folder, 'Documentation')
    os.makedirs(documentation_folder, exist_ok=True)

print("Folder structure, notebook files, and Documentation folders created successfully!")