## image_processing_JPG_streamlit:
# Streamlit Image Processing App

This Streamlit app allows users to enhance JPG/JPEG images using various image processing techniques. 
Users can upload an image, adjust parameters using interactive sliders, and download the enhanced image 
in both JPG and PNG formats.


## Table of Contents
- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- Bilateral filter strength adjustment
- Color saturation control
- CLAHE clip limit tuning
- Sharpening kernel size customization
- Real-time preview of processed image
- Download processed image in JPEG or PNG format

## Dependencies
Ensure you have the following dependencies installed:
- [Streamlit](https://streamlit.io/)
- [Pillow (PIL)](https://pillow.readthedocs.io/)
- [NumPy](https://numpy.org/)
- [ImageIO](https://pypi.org/project/imageio/)
- [OpenCV](https://docs.opencv.org/)

You can install them using the provided `requirements.txt` file.

## Installation

1. Clone the repository:

   git clone https://github.com/happifocus/image_processing_JPG_streamlit.git
   cd image_processing_JPG_streamlit

2. Install dependencies:

   pip install -r requirements.txt

## Usage

Run the app using the following command:

   streamlit run img_app.py

Visit the provided URL in your web browser to access the app.

## Contributing

Feel free to contribute to the project. You can open issues for bugs or feature requests and submit pull requests.

## Licence

This project is licensed under the MIT License.
