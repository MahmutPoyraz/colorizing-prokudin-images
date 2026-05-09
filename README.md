Colorizing Prokudin-Gorskii Glass Plate Images

*******************************************************************************

Introduction

A Python-based image processing pipeline that reconstructs full-color photographs from the early 20th-century glass plate negatives of Russian photographer Sergei Prokudin-Gorskii. The system splits tri-channel monochrome exposures into their Blue, Green, and Red components, aligns them using pixel-level similarity metrics, and composites them into a single high-fidelity colour image.


*******************************************************************************

Background


Between 1909 and 1915, Prokudin-Gorskii photographed the Russian Empire by capturing each scene three times in rapid succession through separate Blue, Green, and Red filters onto a single glass plate. His intention was for these three exposures to be projected simultaneously and produce a colour image. Because the camera moved slightly between each exposure, the three channels are spatially misaligned. This project reconstructs his original vision algorithmically, aligning the channels with sub-pixel precision and producing colour images from negatives that are over a century old.


*******************************************************************************

How It Works

The pipeline processes each input image through four sequential stages:

1. Splitting — The tri-channel glass plate negative is divided horizontally into three equal segments corresponding to the Blue (top), Green (middle), and Red (bottom) exposures.

2. Preprocessing — Each channel is normalised to a floating-point range and prepared for alignment. Edge regions containing scanning artifacts and black borders are identified for exclusion from metric computation.

3. Alignment — Using the Blue channel as a spatial reference, the Green and Red channels are aligned via an exhaustive search over a displacement parameter space. Alignment quality is measured using the Sum of Squared Differences (SSD) metric. To prevent border artifacts from corrupting the similarity score, a 20% centre crop is used during metric computation.

4. Merging and Enhancement — The aligned channels are merged into a single RGB image. A 7% border crop is applied to the final composite to remove edge artifacts introduced by the alignment shifts.


*******************************************************************************

Alignment Metric

The system uses SSD (Sum of Squared Differences) as its primary alignment metric. For two image patches I₁ and I₂, SSD is defined as:

SSD(u, v) = Σ (I₁(x, y) − I₂(x − u, y − v))²

The displacement (u, v) that minimises this value corresponds to the optimal alignment. SSD was chosen for its computational efficiency, numerical stability, and consistent performance across the range of lighting conditions present in the Prokudin-Gorskii collection.

A key empirical finding from processing the full dataset: the Red channel displacement is consistently approximately twice that of the Green channel. This directly reflects the physical layout of the glass plate — Blue (top), Green (middle), Red (bottom) — with the Red frame being furthest from the Blue reference point.

*******************************************************************************

Project Structure


colorizing-prokudin-images/
│
├── code/
│   ├── main.py              # Entry point — orchestrates the full pipeline
│   ├── alignment.py         # SSD and NCC metrics, exhaustive search alignment
│   ├── enhancement.py       # Border cropping and image enhancement
│   └── utils.py             # Image loading, normalisation, channel splitting
│
├── data/                    # Place input glass plate images here (.jpg or .tif)
│
├── results/                 # Processed outputs saved here automatically
│
├── MahmutPoyrazProjectML.pdf   # Full technical report
└── README.md


*******************************************************************************

Installation


git clone https://github.com/MahmutPoyraz/colorizing-prokudin-images.git

cd colorizing-prokudin-images

pip install numpy opencv-python matplotlib scikit-image pillow

*******************************************************************************

Usage

Place your input glass plate images in the data/ folder. The system accepts .jpg, .jpeg, .png, .tif, and .tiff files.

python code/main.py

The pipeline will process every image found in data/ and save three output files per image to the results/ folder:
filename_unaligned.jpg — Raw channel merge with no alignment applied
filename_aligned.jpg — Channel-aligned composite
filename_enhanced.jpg — Final output with border crop applied

An alignment report table is printed to the console on completion, showing the Green and Red displacement vectors for every processed image.


The data/ folder contains a set of sample Prokudin-Gorskii glass plate negatives from the Library of Congress collection, ready to process out of the box. The results/ folder contains the corresponding processed outputs for reference. To process your own images, simply add them to the data/ folder and run the pipeline.


*******************************************************************************


Sample Results

The input image below shows a typical Prokudin-Gorskii glass plate negative: three vertically stacked monochrome exposures of the same scene captured through Blue, Green, and Red filters respectively.

StageDescriptionInputRaw tri-channel glass plate negativeUnalignedChannels merged without correction — colour fringing visibleAlignedChannels shifted into registration — colour fringing eliminatedEnhancedBorder artifacts removed — final colour composite

Across the 29-image test dataset, the alignment algorithm consistently produced accurate results. The average Green channel displacement was approximately (5, 1) pixels and the average Red channel displacement approximately (11, 1) pixels, confirming the expected 2:1 displacement ratio arising from the physical plate geometry.



*******************************************************************************


Technical Challenges

Scanning Artifacts and Border Noise
Raw glass plate scans contain significant black borders and edge artifacts from the digitisation process. These regions caused the SSD metric to converge on incorrect local minima during alignment. Resolved by restricting metric computation to the central 80% of each channel, excluding edge regions entirely.
Temporal Displacement and Motion Artifacts
Because Prokudin-Gorskii captured the three exposures sequentially rather than simultaneously, any movement in the scene between exposures — including subjects, foliage, or water — introduces channel-level inconsistencies that no alignment algorithm can fully resolve. These cases are visible in the output as localised colour fringing on moving elements.


*******************************************************************************


Technical Report

A detailed project report covering the theoretical background, metric selection rationale, full alignment parameter results across the dataset, and experimental analysis is available in MahmutPoyrazProjectML.pdf.



*******************************************************************************

License

This project was developed for educational purposes as part of a Computer Vision course at Ostim Technical University. Feel free to use, adapt, or build upon it with attribution.
