from imlib.general.system import (
    safe_execute_command,
    SafeExecuteCommandError,
)
from brainreg.backend.niftyreg.niftyreg_binaries import (
    get_niftyreg_binaries,
    get_binary,
)
from brainreg.backend.niftyreg.registration import (
    RegistrationError,
    TransformationError,
)

"""
From https://github.com/brainglobe/brainreg
"""


def prepare_affine_reg_cmd(
    floating_image,
    reference_image,
    affine_reg_image_path,
    affine_transform_path,
):

    cmd = "{} {} -flo {} -ref {} -aff {} -res {}".format(
        __get_binary("affine"),
        "-ln 6 -lp 5",
        '"' + str(floating_image) + '"',
        '"' + str(reference_image) + '"',
        '"' + str(affine_transform_path) + '"',
        '"' + str(affine_reg_image_path) + '"',
    )

    return cmd


def prepare_freeform_reg_cmd(
    floating_image,
    reference_image,
    freeform_reg_image_path,
    affine_transform_path,
    control_point_file,
):

    cmd = "{} {} -aff {} -flo {} -ref {} -cpp {} -res {}".format(
        __get_binary("freeform"),
        "-ln 6 -lp 4 -sx -10 -be 0.95 -smooR -1.0 "
        "-smooF -1.0 --rbn 128 --fbn 128",
        '"' + str(affine_transform_path) + '"',
        '"' + str(floating_image) + '"',
        '"' + str(reference_image) + '"',
        '"' + str(control_point_file) + '"',
        '"' + str(freeform_reg_image_path) + '"',
    )
    return cmd


def register_freeform(
    floating_image,
    reference_image,
    freeform_reg_image_path,
    affine_transform_path,
    control_point_file,
):
    """
    Performs freeform (elastic) registration of the average brain of the
    atlas to the sample brain using nifty_reg reg_f3d

    :return:
    :raises RegistrationError: If any error was detected during
        registration.
    """
    try:
        safe_execute_command(
            prepare_freeform_reg_cmd(
                floating_image,
                reference_image,
                freeform_reg_image_path,
                affine_transform_path,
                control_point_file,
            )
        )
    except SafeExecuteCommandError as err:
        raise RegistrationError("Freeform registration failed; {}".format(err))


def register_affine(
    floating_image,
    reference_image,
    affine_reg_image_path,
    affine_transform_path,
):
    """
    Performs affine registration of the average brain of the atlas to the
    sample using nifty_reg reg_aladin

    :return:
    :raises RegistrationError: If any error was detected during
        registration.
    """
    try:
        safe_execute_command(
            prepare_affine_reg_cmd(
                floating_image,
                reference_image,
                affine_reg_image_path,
                affine_transform_path,
            )
        )
    except SafeExecuteCommandError as err:
        raise RegistrationError("Affine registration failed; {}".format(err))


def transform_raw_data(
    floating_image_path,
    reference_image_path,
    dest_img_path,
    control_point_file_path,
):
    """
    Transform raw data to another space
    """

    try:
        safe_execute_command(
            prepare_transformation_command(
                floating_image_path,
                reference_image_path,
                dest_img_path,
                control_point_file_path,
            ),
        )
    except SafeExecuteCommandError as err:
        raise TransformationError(
            "Reverse transformation failed; {}".format(err)
        )


def prepare_transformation_command(
    floating_image_path,
    reference_image_path,
    dest_img_path,
    control_point_file_path,
):
    cmd = "{} {} -cpp {} -flo {} -ref {} -res {}".format(
        __get_binary("segmentation"),
        "-inter 0",
        '"' + str(control_point_file_path) + '"',
        '"' + str(floating_image_path) + '"',
        '"' + str(reference_image_path) + '"',
        '"' + str(dest_img_path) + '"',
    )
    return cmd


def __get_binary(program_type):
    """
    Get the path to the registration (from nifty_reg) program
    based on the type

    :param str program_type:
    :return: The program path
    :rtype: str
    """

    program_names = {
        "affine": "reg_aladin",
        "freeform": "reg_f3d",
        "segmentation": "reg_resample",
        "transform": "reg_transform",
    }
    program_name = program_names[program_type]
    nifty_reg_binaries_folder = get_niftyreg_binaries()

    program_path = get_binary(nifty_reg_binaries_folder, program_name)

    return '"' + program_path + '"'
