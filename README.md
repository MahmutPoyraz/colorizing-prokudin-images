Prokudin-Gorskii Color Spaces Project
****************************************************************************

This project assignment is a study based on the method discovered by the famous chemist and photographer Sergey Prokudin-Gorskii, born in Russia on January 30, 1863, to create high-quality, full-color images by aligning the red, green, and blue channels. The 3-channel images provided as input to this project go through the following stages respectively:

1-) Splitting
2-) Preprocessing - Cleaning Operations
3-) Alignment
4-) Merging 


The project supports .jpg and .tif extension files. These files undergo different processes due to their dimensions. Since .jpg files contain smaller images, a single-scale search is used, whereas an image pyramid approach is utilized for .tif files which contain larger images.


****************************************************************************



Folder Structure:

ComputerVision
|
|
|-->code
|     |-->main.py (Main file)
|     |-->utils.py
|     |-->alignment.py
|     |-->enhancement.py
|
|-->data
|     |
|     |-->rgb 3-channel images with .jpg or .tif extensions
|
|-->results
|      |
|      |-->colorized and quality-enhanced target images
|
|-->MahmutPoyrazProkudinReport.pdf
|
|-->README.txt



*******************************************************************************



Preparation Phase:

To keep the file size as small as possible, this project is submitted without the virtual environment files, although one was used during the development process. If you want to set up a virtual environment or install the required libraries for the project, you can use the guide below.

I- Creating a Virtual Environment:
python -m venv prokudin_env 

II- Activating the Virtual Environment
source prokudin_env/bin/activate  
# Windows: prokudin_env\Scripts\activate 

III- Installing Required Libraries
pip install numpy opencv-python matplotlib scikit-image pillow


*******************************************************************************


Executing the Program:

After completing the necessary installations, the next step is to run the program. The following command can be used to execute the script: 
python code/main.py

To minimize the submitted file size, the initial states of the data and results folders are empty. The inputs provided will be processed, and the outputs will be saved to the results folder. Please place the necessary inputs for the program into the data folder before running.


*******************************************************************************


Project Developer:

Name: Mahmut
Surname: Poyraz
Department: Bilgisayar Mühendisliği 


*******************************************************************************


BEST REGARDS
