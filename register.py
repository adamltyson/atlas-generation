import imio
import fire
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


def register_two_images(im1_path: str, im2_path: str, output_directory: str):

    scaling = []
    for idx, vox_size in enumerate(image_voxel_sizes):
        scaling.append(
            round(
                float(image_voxel_sizes[idx]) / float(atlas_voxel_sizes[idx]),
                scaling_rounding_decimals,
            )
        )

    start_time = datetime.now()

    def load_preprocess(image_path, scaling):
        image = imio.load_any(
            image_path,
            scaling[1],
            scaling[2],
            scaling[0],
        )
        image = preprocess.filter_image(image)

        return image

    im1 = load_preprocess(im1_path, scaling)
    im2 = load_preprocess(im2_path, scaling)

    niftyreg_paths = NiftyRegPaths(output_directory)

    save_nii(im2, atlas_voxel_sizes, niftyreg_paths.brain_filtered)
    save_nii(im1, atlas_voxel_sizes, niftyreg_paths.downsampled_filtered)

    registration_params = RegistrationParams()

    brain_reg = BrainRegistration(
        niftyreg_paths,
        registration_params,
        n_processes=n_processes,
    )

    brain_reg.register_affine()
    brain_reg.register_freeform()

    print("Finished. Total time taken: %s", datetime.now() - start_time)


def main():
    fire.Fire(register_two_images)


if __name__ == "__main__":
    main()
