import imio
from brainreg.utils import preprocess
from brainreg.backend.niftyreg.utils import save_nii


def load_preprocess_save(
    image_path,
    scaling,
    nii_filepath,
    filtered_nii_filepath,
    atlas_voxel_sizes,
):
    image = imio.load_any(
        image_path,
        scaling[1],
        scaling[2],
        scaling[0],
    )
    save_nii(image, atlas_voxel_sizes, nii_filepath)

    image = preprocess.filter_image(image)
    save_nii(image, atlas_voxel_sizes, filtered_nii_filepath)

    return image
