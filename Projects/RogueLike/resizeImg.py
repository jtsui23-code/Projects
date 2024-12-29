import os
from PIL import Image

def resize_images_in_directory(input_dir, output_dir, target_size=(16, 16)):
    """
    Resize all images in a directory to a target size and save them to an output directory.
    
    Args:
        input_dir (str): Path to directory containing the original images
        output_dir (str): Path to directory where resized images will be saved
        target_size (tuple): Desired width and height in pixels, defaults to (16, 16)
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Supported image formats
    valid_formats = ['.png', '.jpg', '.jpeg', '.bmp']
    
    # Track progress
    processed = 0
    errors = 0
    
    # Process each file in the input directory
    for filename in os.listdir(input_dir):
        # Check if file is an image
        if any(filename.lower().endswith(fmt) for fmt in valid_formats):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            try:
                # Open and resize the image
                with Image.open(input_path) as img:
                    # Use LANCZOS resampling for better quality
                    resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
                    
                    # Preserve original image mode and transparency
                    resized_img = resized_img.convert(img.mode)
                    
                    # Save the resized image
                    resized_img.save(output_path, quality=95, optimize=True)
                
                processed += 1
                print(f"Resized: {filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                errors += 1
    
    return processed, errors

# Example usage
if __name__ == "__main__":
    # Set your input and output directories
    input_directory = "Media/Assets/tiles/newGrass"  # Change this to your input directory path
    output_directory = "tiles/newGrass_16x16"  # Change this to your output directory path
    
    print("Starting image resizing...")
    processed, errors = resize_images_in_directory(input_directory, output_directory)
    print(f"\nCompleted! Processed {processed} images with {errors} errors.")