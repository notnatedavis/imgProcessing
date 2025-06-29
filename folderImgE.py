# --- folderImgE.py --- #
# encrypts image(s) into .txt files (specific format) within same directory of folder

# notes : I want to clean up comments + prints + format

# --- Imports --- #
import os
import re
from PIL import Image

# Hardcoded variables
VALID_DIRECTORIES = [
    "E:\\", # Windows
    "/run/media/whoshotnate/PERSONAL3", # Linux
    "/Volumes/PERSONAL3", # Mac
    "/Volumes/Macintosh HD/Users/User/Directory" # personal local custom directory
]

# --- Helper Functions --- #

def natural_sort_key(s) :
    # function for natural sorting
    # Ex. ['a10.jpg', 'a2.jpg'] -> ['a2.jpg', 'a10.jpg']
    return [int(part) if part.isdigit() else part.lower() 
            for part in re.split('([0-9]+)', s)]

def value_to_encrypted_string(value) :
    # determine the character based on 10's place
    char = chr(ord('A') + (value // 10))

    # determine the digit  based on the last digit of the value
    digit = str(value%10)

    # combine into encrypted string
    encrypted_str = f"{char}{digit}"

    return encrypted_str

def rgb_to_encrypted_string(r, g, b) :
    # convert each channel to the encrypted string format
    red_str = value_to_encrypted_string(r)
    green_str = value_to_encrypted_string(g)
    blue_str = value_to_encrypted_string(b)

    # combine into final encrypted string
    encrypted_str = f"{red_str}{green_str}{blue_str}"

    return encrypted_str # alt : return f"{red_str}{green_str}{blue_str}"

def encrypt_image_to_text(image_path, output_text_path) :
    # open the image
    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size

    # open the output text file
    with open(output_text_path, 'w') as f :
        for y in range(height) :
            for x in range(width) :
                # get the RGB value of the pixel
                r, g, b = img.getpixel((x, y))

                # convert RGB to encrypted string
                encrypted_pixel = rgb_to_encrypted_string(r, g, b)

                # write the encrypted pixel to the file
                f.write(encrypted_pixel + ' ')

            f.write("\n") # new line after each row of pixels

    os.remove(image_path) # remove original image after encryption
    print(f"Image E&^S to : {output_text_path}")

# --- Main Entry Point --- #

if __name__ == "__main__" :

    # --- 1. Directory Selection --- #

    # filter for existing directories
    existing_dirs = [d for d in VALID_DIRECTORIES if os.path.exists(d)]
    
    if not existing_dirs :
        print("ERROR: No valid directories found from the hardcoded list.")
        exit()

    # directory selection menu
    print("\nAvailable base directories:")
    for i, directory in enumerate(existing_dirs) :
        print(f"{i+1}. {directory}")
    
    try :
        dir_choice = int(input("\nSelect base directory number: ")) - 1
        
        if dir_choice < 0 or dir_choice >= len(existing_dirs):
            raise ValueError
            
        base_dir = existing_dirs[dir_choice]
        
    except ValueError :
        print("Invalid directory selection.")
        exit()

    # --- 2. Folder Selection --- #

    # set of folders to ignore
    IGNORE = {"System Volume Information"}
        
    # get all folders in hardcoded directory
    folders = [f for f in os.listdir(base_dir)
               if os.path.isdir(os.path.join(base_dir, f))
               and not f.startswith('.') # skip .*
               and f not in IGNORE] # skip predefined
    folders.sort(key=natural_sort_key)

    if not folders : 
        print("No folders found in directory.")
        exit()

    # display folder selection menu
    print("Available folders:")
    for i, foldername in enumerate(folders) :
        print(f"{i+1}. {foldername}")
    
    # get user selection
    try :
        selection = selection = int(input("\nEnter folder number to encrypt: ")) - 1

        if selection < 0 or selection >= len(folders) :
            raise ValueError
    
    except ValueError :
        print("Invalid selection.")
        exit()

    # process selected folder
    selected_folder = folders[selection]
    folder_path = os.path.join(base_dir, selected_folder)

    # get all image files in folder
    image_files = [
        f for f in os.listdir(folder_path)
        if not f.startswith('.')
           and f.lower().endswith(('.jpg', '.png', '.bmp'))
    ]

    image_files.sort(key=natural_sort_key) # (natural) sort files
    
    if not image_files :
        print("No images found in selected folder.")
        exit()

    # Process each image
    for img_file in image_files :
        img_path = os.path.join(folder_path, img_file)
        out = os.path.splitext(img_file)[0] + ".txt"

        encrypt_image_to_text(img_path, os.path.join(folder_path, out))
        # print(f"Encrypted and removed: {img_file} -> {output_filename}")
    
    print("\nAll images within folder encrypted")
