# Synthetic Credit Card Image Generator

## Overview

This project generates synthetic images of credit cards for training machine learning models, specifically using the YOLOv8 object detection model. The images are generated using a Blender file that runs a Python script to create realistic scenes with varied conditions. The generated images are of size 800x800 in JPG format and are accompanied by the necessary annotation files for YOLOv8 and Hugging Face.

## Features

- **Credit card 3D Model**: Uses a 3D model of a credit card for the front and the back.
- **Randomized Text**: Text on the card is randomly generated using Python.
- **Scene Variation**: Each rendered image has randomized conditions, including background, lighting, and camera position.
- **Annotation Files**: Generates annotation files compatible with YOLOv8 and Hugging Face in JSONL format.
- **Card Background**: Generates different types of images to dress the credit card.

# Annotations

## YOLOv8

The annotation files for YOLOv8 are generated as per the YOLOv8 dataset requirements. Each image will have a corresponding .txt file with the bounding box coordinates.

## Hugging Face

The annotation files for Hugging Face are generated in JSONL format as per the Hugging Face image dataset documentation.

# Links

Here are some useful links:

- [Project site](http://localhost:3000/visionCardDocs/#/)
- [Android demo](https://github.com/bytesWright/creditCardDetectionAndroidDemo)
- [Data set](https://huggingface.co/datasets/bytesWright/creditCardDetectionDS)
- [Models](https://huggingface.co/bytesWright/creditCardDetection)

# Contributions

We welcome contributions from the community. If you plan to use these components or modified versions in a product, research project, or any other initiative that adds value, please notify us. This helps us maintain a record of users and allows us to acknowledge your contributions on our website.

# Contact

For any inquiries or further information, please contact us at bytesWright@isdavid.com.
