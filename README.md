# atlas-generation
**WIP**

Scripts to help generate novel 3D anatomical reference atlases from existing whole-organ data.

Aim is to include:
* Generation of template, reference images from N datasets
* Annotation of anatomical subdivisions
* Generation of metadata (region hierarchy etc)
* Packaging for the [BrainGlobe Atlas API](https://github.com/brainglobe/bg-atlasapi)
* Napari plugin for the above in a single graphical environment

## Current scripts:
### `register.py` - Register N images to a single reference image
Usage:
```bash
 python atlas-generation/register.py path/to/image_list.csv /path/to/reference_image.tiff /path/to/output_directory
```

Where `image_list.csv` is a simple list of image paths, e.g.:

|                      |
|----------------------|
| /path/to/image1.tiff |
| /path/to/image2.tiff |
| /path/to/image3.tiff |
| /path/to/image4.tiff |

All images must be the same resolution and orientation (`.tiff` and `.nii` supported).
Default pixel size is 10um isotropic, but this can be changed by setting the 
`--image_voxel_sizes` flag. 

The final template resolution will be 10um isotropic, but this can be changed by setting the 
`--atlas_voxel_sizes` flag. 

