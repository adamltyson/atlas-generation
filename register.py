import fire
import pandas as pd
from datetime import datetime

from paths import ReferencePaths, ImagePaths
from utils.misc import calculate_scaling
from utils.image import load_preprocess_save
from utils.registration import (
    register_affine,
    register_freeform,
    transform_raw_data,
)


def register_two_images(
    floating_images: str,
    reference_image: str,
    output_directory: str,
    image_voxel_sizes=(10, 10, 10),
    atlas_voxel_sizes=(25, 25, 25),
):
    start_time = datetime.now()
    scaling = calculate_scaling(image_voxel_sizes, atlas_voxel_sizes)

    reference_paths = ReferencePaths(output_directory)

    print("Loading and filtering reference image")
    load_preprocess_save(
        reference_image,
        scaling,
        reference_paths.reference_raw_path,
        reference_paths.reference_filtered_path,
        atlas_voxel_sizes,
    )

    image_list = list(pd.read_csv(floating_images, header=None)[0])

    for image_path in image_list:
        image_paths = ImagePaths(image_path, reference_paths.output_directory)
        print(f"Loading and filtering: {image_paths.image_path}")
        load_preprocess_save(
            image_paths.image_path,
            scaling,
            image_paths.image_raw_path,
            image_paths.image_filtered_path,
            atlas_voxel_sizes,
        )

        print("Running affine registration")
        register_affine(
            image_paths.image_filtered_path,
            reference_paths.reference_filtered_path,
            image_paths.affine_reg_image_path,
            image_paths.affine_transform_path,
        )

        print("Running freeform registration")
        register_freeform(
            image_paths.image_filtered_path,
            reference_paths.reference_filtered_path,
            image_paths.freeform_reg_image_path,
            image_paths.affine_transform_path,
            image_paths.control_point_file,
        )

        print("Transforming raw data to reference space")
        transform_raw_data(
            image_paths.image_raw_path,
            reference_paths.reference_raw_path,
            image_paths.transformed_raw_path,
            image_paths.control_point_file,
        )

    print("Finished. Total time taken: %s", datetime.now() - start_time)


def main():
    fire.Fire(register_two_images)


if __name__ == "__main__":
    main()
