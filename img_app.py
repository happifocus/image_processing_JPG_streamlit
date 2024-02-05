# Import libraries
import streamlit as st
from io import BytesIO
from PIL import Image
import numpy as np
import imageio
import os
import cv2

## Preset: Change colors of all slider elements using CSS custom styles
# Set background of min/max values transparent
ColorMinMax = st.markdown(''' <style> div.stSlider > div[data-baseweb = "slider"] > div[data-testid="stTickBar"] > div {
            background: rgb(1 1 1 / 0%); } </style>''', unsafe_allow_html = True)

# Set color for cursor
Slider_Cursor = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
            background-color: rgb(40, 225, 51); box-shadow: rgb(22 130 30 / 100%) 0px 0px 0px 0.2rem;} </style>''', unsafe_allow_html = True)

# Set color for slider number
Slider_Number = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div > div
                                        { color: rgb(138, 148, 143); } </style>''', unsafe_allow_html = True)
            
# Set color shading for slider
col = f''' <style> div.stSlider > div[data-baseweb = "slider"] > div > div {{
            background: linear-gradient(to left, rgb(40, 225, 51) 0%, 
                                        rgb(22, 130, 30) 30%, 
                                        rgba(40, 225, 51, 0.25) 70%, 
                                        rgba(22, 130, 30, 0.25) 100%); }} </style>'''
# Apply color shading on slider
ColorSlider = st.markdown(col, unsafe_allow_html = True)



## 1. Function to process the uploaded image with user-defined parameters
def process_image(input_image, bilateral_strength, clahe_clip_limit, sharpening_kernel_size, saturation_factor):
    
    # Convert PIL Image to NumPy array
    input_image_np = np.array(input_image)

    # Split PIL image into its individual color channels
    blue, green, red = cv2.split(input_image_np)
  
    # Apply bilateral blur filter to each color channel with user-defined 'bilateral_strength'
    blue_blur = cv2.bilateralFilter(blue, d=bilateral_strength, sigmaColor=55, sigmaSpace=55)
    green_blur = cv2.bilateralFilter(green, d=bilateral_strength, sigmaColor=55, sigmaSpace=55)
    red_blur = cv2.bilateralFilter(red, d=bilateral_strength, sigmaColor=55, sigmaSpace=55)

    # Create CLAHE object with user-defined clip limit
    clahe = cv2.createCLAHE(clipLimit=clahe_clip_limit, tileGridSize=(3, 3))
 
    # Adjust histogram and contrast for each color channel using CLAHE
    blue_eq = clahe.apply(blue_blur)
    green_eq = clahe.apply(green_blur)
    red_eq = clahe.apply(red_blur)

    # Merge the color channels back into a single RGB image
    output_img = cv2.merge((blue_eq, green_eq, red_eq))

    # Color saturation: convert image from BGR color space to HSV (Hue, Saturation, Value) color space
    hsv_image = cv2.cvtColor(output_img, cv2.COLOR_BGR2HSV)

    # Multiply the saturation channel by user-defined 'saturation_factor'
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor, 1, 254).astype(np.uint8)

    # Convert image back to BGR color space
    result_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    # Create user-defined 'sharpening_kernel_size'
    kernel = np.ones((sharpening_kernel_size, sharpening_kernel_size), np.float32) * -1
    kernel[sharpening_kernel_size//2, sharpening_kernel_size//2] = sharpening_kernel_size**2

    # Apply sharpening kernel to image using filter2D
    processed_image = cv2.filter2D(result_image, -1, kernel)

    return Image.fromarray(processed_image)

   


## 2. Main function to run the Streamlit App
def main():
    # Set title for the App
    st.markdown("## :blue[Image Processing: Enhance JPG/JPEG Images]")
    
    # Draw a dividing line
    st.divider()

    # Step 1: # Step 1: upload image file as jpg/jpeg, include label
    uploaded_file = st.file_uploader(" #### :camera: :violet[1. Upload Image] ", type=["JPG", "JPEG"])

    if uploaded_file is not None:
        # Display uploaded image with label
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Draw a dividing line
        st.divider()

        # Set subtitle and short explanation
        st.write("#### :crystal_ball: :violet[2. Apply Image Filter]")
        st.write("The processed image is shown with a preset of parameters. Use the sliders to explore the effects of image filters, or to \
                 refine the adjustment. - When you are happy with the result, download the processed image.")


        # Step 2: Slider customization with live updates
        # create 2 columns to distribute sliders
        col1, col2 = st.columns(2)

        # Column 1: create sliders for Bilateral Filter and Saturation
        bilateral_strength = col1.slider("###### :heavy_check_mark: :blue[Bilateral Filter Strength] (preset = 5)", min_value=0, max_value=15, value=5, key='bilateral')
        saturation_factor = col1.slider("###### :heavy_check_mark: :blue[Color Saturation] (preset = 1.1)", min_value=0.0, max_value=2.0, step=0.05, value=1.1, key='saturation')
        # Column 2: create sliders for CLAHE and Sharpening
        clahe_clip_limit = col2.slider("###### :heavy_check_mark: :blue[CLAHE Clip Limit] (preset = 0.35)", min_value=0.1, max_value=3.0, value=0.35, step=0.05, key='clahe')
        sharpening_kernel_size = col2.slider("###### :heavy_check_mark: :blue[Sharpening Kernel Size] (preset = 3)", min_value=1, max_value=9, step=2, value=3, key='sharpen')
        
        
        # Step 3: Live Preview of Image Processing
        if uploaded_file is not None:
            # Read uploaded image
            image = Image.open(uploaded_file)
            
            # Process image with updated parameters
            processed_image_pil = process_image(image, bilateral_strength, clahe_clip_limit, sharpening_kernel_size, saturation_factor)

            # Display resulting image dynamically
            st.image(processed_image_pil, caption="Processed Image", use_column_width=True)

            # Get filename and extension using os.path
            original_name, original_extension = os.path.splitext(uploaded_file.name)

            # Construct file names for processed images
            processed_image_name_jpeg = f"{original_name}_processed.jpg"
            processed_image_name_png = f"{original_name}_processed.png"

            # Draw a dividing line
            st.divider()

            # Download message
            st.caption("Preparing Download... Please wait.")

            # Save processed image in JPEG format in-memory
            jpeg_buffer = BytesIO()
            processed_image_pil.save(jpeg_buffer, format="JPEG")
            jpeg_data = jpeg_buffer.getvalue()

            # Save processed image in PNG format in-memory using imageio
            png_buffer = BytesIO()
            imageio.imwrite(png_buffer, np.array(processed_image_pil), format='PNG')
            png_data = png_buffer.getvalue()

            
            # Step 4: Download Buttons
            # write subtitle and download information
            st.markdown(f"#### :floppy_disk: :violet[3. Download Processed Image] ")
            st.write('Download image in compressed :file_folder: :violet[JPG] or losless :file_folder: :violet[PNG] file format:')
            
            # Provide download buttons for both formats
            # create 2 columns to distribute download buttons
            col1, col2 = st.columns(2)
            # place download button for jpeg file in column 1
            with col1:
                st.download_button(
                    label=f":file_folder: :violet[JPG] ({processed_image_name_jpeg})",
                    data=jpeg_data,
                    file_name=processed_image_name_jpeg,
                    key="processed_image_download_jpeg",
                )
             # place download button for png file in column 2
            with col2:
                st.download_button(
                    label=f":file_folder: :violet[PNG] ({processed_image_name_png})",
                    data=png_data,
                    file_name=processed_image_name_png,
                    key="processed_image_download_png",
                )
# run main function
if __name__ == "__main__":
    main()
