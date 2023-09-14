import os
import argparse

import SimpleITK as sitk
import numpy as np

import os
import argparse

import SimpleITK as sitk
import numpy as np

def segment_structures(img):
    """
    Computes segmentation of structures in ultrasound images.

    input US image
    output segmentation label map
    """
    sigma_over_spacing = img.GetSpacing()[0]

    erode_filter = sitk.BinaryErodeImageFilter()
    erode_filter.SetKernelRadius(12)

    dilate_filter = sitk.BinaryDilateImageFilter()
    dilate_filter.SetKernelRadius(2)

    gaussian_filter = sitk.SmoothingRecursiveGaussianImageFilter()
    gaussian_filter.SetSigma(sigma_over_spacing*1.5)
    

    segmentation_img = sitk.Median(img)
    segmentation_img = sitk.LaplacianSharpening(segmentation_img)
    segmentation_img = sitk.Median(segmentation_img)
    segmentation_img = sitk.LaplacianSharpening(segmentation_img)
    segmentation_img = sitk.Median(segmentation_img)
    segmentation_img = sitk.LaplacianSharpening(segmentation_img)
    segmentation_img = sitk.Median(segmentation_img)
    segmentation_img = sitk.LaplacianSharpening(segmentation_img)
    smooth_img = gaussian_filter.Execute(segmentation_img)
    segmentation_img = sitk.LaplacianSharpening(segmentation_img)
    segmentation_img = sitk.LaplacianSharpening(segmentation_img)
    segmentation_img = sitk.LaplacianSharpening(segmentation_img)
    segmentation_img = sitk.LaplacianSharpening(segmentation_img)
    segmentation_img = sitk.LaplacianSharpening(segmentation_img)
    segmentation_img = sitk.LaplacianSharpening(segmentation_img)
    segmentation_img = sitk.LaplacianSharpening(segmentation_img)
    segmentation_img = sitk.Normalize(smooth_img)
    segmentation_img = sitk.Cast(segmentation_img, sitk.sitkFloat32)
    sitk.WriteImage(segmentation_img, 'Z:/work2/manske/temp/seedpointfix/test.nii')

    grad_img = sitk.GradientMagnitude(segmentation_img)
    sitk.WriteImage(grad_img, 'Z:/work2/manske/temp/seedpointfix/grad_init.nii')
    grad_img = sitk.BinaryThreshold(grad_img, 0.2, 999)
    sitk.WriteImage(grad_img, 'Z:/work2/manske/temp/seedpointfix/grad_thresh.nii')
    grad_img = dilate_filter.Execute(grad_img)
    sitk.WriteImage(grad_img, 'Z:/work2/manske/temp/seedpointfix/grad.nii')

    thresh_img = sitk.BinaryThreshold(segmentation_img, -0.1, 1.3)
    sitk.WriteImage(thresh_img, 'Z:/work2/manske/temp/seedpointfix/thresh1.nii')

    thresh_img = thresh_img-grad_img
    thresh_img = thresh_img == 1

    thresh_img = erode_filter.Execute(thresh_img)
    dilate_filter.SetKernelRadius(8)
    thresh_img = dilate_filter.Execute(thresh_img)
    sitk.WriteImage(thresh_img, 'Z:/work2/manske/temp/seedpointfix/thresh.nii')

    # seed = segmentation_img*0
    # seed[62, 312, 318] = 1
    # seed = sitk.BinaryDilate(sitk.Cast(seed, sitk.sitkUInt8), (6, 6, 6))

    erode_filter.SetKernelRadius(2)
    thresh_img = erode_filter.Execute(thresh_img)

    connected_filter = sitk.ConnectedThresholdImageFilter()
    connected_filter.SetLower(1)
    connected_filter.SetUpper(1)
    connected_filter.SetSeedList([[62, 312, 318]])
    connected_filter.SetReplaceValue(1)

    init_seg = connected_filter.Execute(thresh_img)
    sitk.WriteImage(init_seg, 'Z:/work2/manske/temp/seedpointfix/thresh.nii')

    distance_filter = sitk.SignedMaurerDistanceMapImageFilter()
    distance_filter.SetInsideIsPositive(True)
    distance_filter.SetUseImageSpacing(False)
    distance_filter.SetBackgroundValue(0)
    distance_img = distance_filter.Execute(init_seg)
    distance_img.SetSpacing([1,1,1])
    feature_img = sitk.GradientMagnitude(segmentation_img)
    feature_img.SetSpacing([1,1,1])

    print("Applying level set filter")
    ls_filter = sitk.ThresholdSegmentationLevelSetImageFilter()
    ls_filter.SetLowerThreshold(-9999)
    ls_filter.SetUpperThreshold(0.25)
    ls_filter.SetMaximumRMSError(0.002)
    ls_filter.SetNumberOfIterations(500)
    ls_filter.SetCurvatureScaling(1)
    ls_filter.SetPropagationScaling(1)
    ls_filter.SetReverseExpansionDirection(True)
    ls_img = ls_filter.Execute(distance_img, feature_img)

    ls_img.SetSpacing(img.GetSpacing())
    sitk.WriteImage(ls_img, 'Z:/work2/manske/temp/seedpointfix/levelset.nii')

    output_img = ls_img>-4
    
    return output_img

def main():
    """
    main function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=str, help="Path to input image (nii or mha)")
    parser.add_argument("output_segmentation_path", type=str, help="Path and file name to store output segmentation. \
                        Acceptable formats are (nii, mha)")

    args = parser.parse_args()
    input_path = args.input_path
    output_path = args.output_segmentation_path

    input_image = sitk.ReadImage(input_path)
    segmentation = segment_structures(input_image)
    sitk.WriteImage(segmentation, output_path)

if __name__ == '__main__':
    main()