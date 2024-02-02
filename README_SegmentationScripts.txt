QuPath segmentation workflow:
1. Import appropriate jar file, if not already completed
2. Select area to be segmented
3. Load appropriate StarDist cell segmentation groovy file based on pixel size
4. Run stardist_cell_seg_model.pb

**********
Akoya created modified StarDist cell segmentation scripts (groovy files) which were shared with Akoya CODEX customers (aka, "Grady scripts" since Grady Carlson was the author).
- The scripts require 2 other files: (1) the QuPath version-specific jar file and (2) the appropriate protocol buffer (pb) file.  

Jar files are needed to run the StarDist segmentation scripts and are specific to the QuPath version. This folder includes the 2 most recent versions:
- qupath-extension-stardist-0.4.0.jar for QuPath versions 0.4.*
- qupath-extension-stardist-0.5.0.jar for QuPath versions 0.5.*

Groovy files are the operational scripts. The scripts included in this folder differ only in the image pixel size criteria. 
The most commonly used scripts have been renamed to help distinguish which to use when the image metadata isn't available. 
- StarDist cell segmentation_mIHC-Keyence_script_0.37_um_per_pixel.groovy is for 0.37 um/pixel sized images such as mIHC (aka Vectra or Opal) images that have been fused within QuPath or for the older CODEX QPTIFFs generated on the older CODEX-Keyence platform. 
- StarDist cell segmentation_FUSION_script_0.5_um_per_pixel.groovy is for 0.5 um/pixel images such as the newer QPTIFFs that were imaged on the PhenoCycler-Fusion
Other pre-made pixel size scripts in the folder cover 0.25 um/pixel and 0.33 um/pixel for other image formats.

Protocol file
- stardist_cell_seg_model.pb contains the model information for the segmentation

