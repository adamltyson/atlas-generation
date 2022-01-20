def calculate_scaling(
    image_voxel_sizes, atlas_voxel_sizes, scaling_rounding_decimals=5
):
    scaling = []
    for idx, vox_size in enumerate(image_voxel_sizes):
        scaling.append(
            round(
                float(image_voxel_sizes[idx]) / float(atlas_voxel_sizes[idx]),
                scaling_rounding_decimals,
            )
        )
    return scaling
