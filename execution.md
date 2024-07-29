# How to Run the Data Set Generation

In the Blender file, several scripts are available for rendering different aspects of the credit card dataset. Below is a detailed list of these scripts:

1. **Render-Data-Set**
   - **Purpose**: The primary script for generating the complete dataset.
   - **Function**: Orchestrates comprehensive rendering of the dataset, including both front and back views under diverse scenarios.

2. **Render-Back**
   - **Purpose**: Test the rendering results for the back of a credit card.
   - **Function**: Generates synthetic images to simulate various designs and conditions on the back of credit cards.

3. **Render-Front**
   - **Purpose**: Test the rendering results for the front of a credit card.
   - **Function**: Produces synthetic images showcasing different front designs and scenarios.

4. **Render-Post-Validation**
   - **Purpose**: Generates images of real credit cards for model validation post-training.
   - **Function**: Used by QA to assess the accuracy of the model.
   - **Note**: This script requires further development to be integrated into the training process.
