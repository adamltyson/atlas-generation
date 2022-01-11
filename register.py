import imio
import fire
import os
from datetime import datetime

from brainreg.utils import preprocess
from brainreg.backend.niftyreg.paths import NiftyRegPaths
from brainreg.backend.niftyreg.registration import BrainRegistration
from brainreg.backend.niftyreg.parameters import RegistrationParams
from brainreg.backend.niftyreg.utils import save_nii

image_voxel_sizes = (10, 10, 10)
atlas_voxel_sizes = (25, 25, 25)

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

    niftyreg_paths = NiftyRegPaths(output_directory)

    im1_raw_path = os.path.join(output_directory, "im1.nii")
    im2_raw_path = os.path.join(output_directory, "im2.nii")

    im1 = load_preprocess_save(
        im1_path, scaling, im1_raw_path, niftyreg_paths.downsampled_filtered
    )
    im2 = load_preprocess_save(
        im2_path, scaling, im2_raw_path, niftyreg_paths.brain_filtered
    )

    registration_params = RegistrationParams()

    brain_reg = BrainRegistration(
        niftyreg_paths,
        registration_params,
        n_processes=n_processes,
    )

    brain_reg.register_affine()
    brain_reg.register_freeform()

    os.rename(
        niftyreg_paths.control_point_file_path,
        niftyreg_paths.inverse_control_point_file_path,
    )
    brain_reg.transform_to_standard_space(
        im2_raw_path,
        niftyreg_paths.freeform_registered_atlas_brain_path,
    )

    print("Finished. Total time taken: %s", datetime.now() - start_time)


def main():
    fire.Fire(register_two_images)


if __name__ == "__main__":
    main()
