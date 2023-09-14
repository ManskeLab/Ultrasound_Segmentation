import os
import argparse

import SimpleITK as sitk
import numpy as np

def compile_frames(frames_path):
    """
    compiles frames in input directory into one single sitk image.

    input: path to frames directory
    output: compiled image
    """
    compiled_img_arr = None

    for frame in os.listdir(frames_path):
        frame_path = os.path.join(frames_path, frame)
        if os.path.getsize(frame_path) ==  0:
            continue
        frame_img = sitk.ReadImage(frame_path)
        compiled_img_arr = 0*sitk.GetArrayFromImage(frame_img)
        break

    for frame in os.listdir(frames_path):
        frame_path = os.path.join(frames_path, frame)
        if os.path.getsize(frame_path) ==  0:
            continue
        print(frame)
        frame_img = sitk.ReadImage(frame_path)
        frame_arr = np.flip(sitk.GetArrayFromImage(frame_img), axis = 0)
        compiled_img_arr = np.append(compiled_img_arr, frame_arr, axis = 2)

    compiled_img = sitk.GetImageFromArray(compiled_img_arr)
    return compiled_img

def main():
    """
    main function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("frames_path", type=str, help="Path to directory containing each individual \
                        frame in an acceptable image format (jpeg, jpg, png, tif, dcm , nii, mha, aim).")
    parser.add_argument("output_path", type=str, help="Path and file name to store output in. \
                        Acceptable formats are (nii, mha).")

    args = parser.parse_args()
    frames_path = args.frames_path
    output_path = args.output_path

    ext_in= frames_path.split(".")[-1]
    ext_out = output_path.split(".")[-1]

    good_in_ext = ['nii', 'mha', 'jpeg', 'jpg', 'png', 'tif', 'dcm', 'aim']
    good_out_ext = ['nii', 'mha']

    if ext_in not in good_in_ext:
        raise AttributeError("Input must have one of the following file formats:\n \
                             jpeg, jpg, png, tif, dcm , nii, mha, aim")
    if ext_out not in good_out_ext:
        raise AttributeError("Output can only be one of the following file formats:\n \
                             nii, mha")

    compiled_img = compile_frames(frames_path)
    sitk.WriteImage(compiled_img, output_path)

if __name__ == '__main__':
    main()