import imio
import fire
import os
from datetime import datetime
from pathlib import Path
from brainreg.utils import preprocess

from brainreg.backend.niftyreg.utils import save_nii
from utils import register_affine, register_freeform

image_voxel_sizes = (10, 10, 10)
atlas_voxel_sizes = (10, 10, 10)

scaling_rounding_decimals = 5
n_processes = 8


def load_preprocess_save(
    image_path, scaling, nii_filepath, filtered_nii_filepath
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


def register_two_images(im1_path: str, im2_path: str, output_directory: str):
    start_time = datetime.now()

    scaling = []
    for idx, vox_size in enumerate(image_voxel_sizes):
        scaling.append(
            round(
                float(image_voxel_sizes[idx]) / float(atlas_voxel_sizes[idx]),
                scaling_rounding_decimals,
            )
        )

    Path(output_directory).mkdir(exist_ok=True)

    im1_raw_path = os.path.join(output_directory, "im1.nii")
    im2_raw_path = os.path.join(output_directory, "im2.nii")

    im1_filtered_path = os.path.join(output_directory, "im1_filtered.nii")
    im2_filtered_path = os.path.join(output_directory, "im2_filtered.nii")
    affine_reg_image_path = os.path.join(
        output_directory, "affine_registered.nii"
    )
    freeform_reg_image_path = os.path.join(
        output_directory, "freeform_registered.nii"
    )
    affine_transform_path = os.path.join(output_directory, "affine.txt")
    control_point_file = os.path.join(output_directory, "control_point.nii")

    load_preprocess_save(im1_path, scaling, im1_raw_path, im1_filtered_path)
    load_preprocess_save(im2_path, scaling, im2_raw_path, im2_filtered_path)

    register_affine(
        im1_filtered_path,
        im2_filtered_path,
        affine_reg_image_path,
        affine_transform_path,
    )

    register_freeform(
        im1_filtered_path,
        im2_filtered_path,
        freeform_reg_image_path,
        affine_transform_path,
        control_point_file,
    )

    print("Finished. Total time taken: %s", datetime.now() - start_time)


def main():
    fire.Fire(register_two_images)


if __name__ == "__main__":
    main()
