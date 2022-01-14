from pathlib import Path


class ReferencePaths:
    def __init__(self, output_directory):
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(exist_ok=True)
        self.reference_raw_path = self.output_directory / "reference_raw.nii"
        self.reference_filtered_path = (
            self.output_directory / "reference_filtered.nii"
        )


class ImagePaths:
    def __init__(self, image_path, output_directory):
        self.image_path = Path(image_path)
        self.image_dir = output_directory / self.image_path.stem
        self.image_dir.mkdir(exist_ok=True)
        self.image_raw_path = self.image_dir / (
            self.image_path.stem + "_raw.nii"
        )
        self.image_filtered_path = self.image_dir / (
            self.image_path.stem + "_filtered.nii"
        )
        self.transformed_raw_path = self.image_dir / (
            self.image_path.stem + "_transformed.nii"
        )

        self.affine_reg_image_path = self.image_dir / (
            self.image_path.stem + "_affine.nii"
        )
        self.freeform_reg_image_path = self.image_dir / (
            self.image_path.stem + "_freeform.nii"
        )

        self.affine_transform_path = self.image_dir / "affine.txt"
        self.control_point_file = self.image_dir / "control_point.nii"
