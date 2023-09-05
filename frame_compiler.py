import SimpleITK
import os
import argparse

def compile_frames(frames_path):
    """
    compiles frames in input directory into one single sitk image.

    input: path to frames directory
    output: compiled image
    """

    for frame in os.listdir(frames_path):
        print(frame)

def main():
    """
    main function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("frames_path", type=str, help="Path to directory containing each individual \
                        frame in an acceptable image format (jpeg, hpg, png, tif, dcm , nii, mha, aim).")
    parser.add_argument("output_path", type=str, help="Path and file name to store output in. \
                        Acceptable formats are (nii, mha)")

    args = parser.parse_args()
    frames_path = args.frames_path
    output_path = args.output_path

    compiled_img = compile_frames(frames_path)
    sitk.WriteImage(compiled_img, output_path)

if __name__ == '__main__':
    main()