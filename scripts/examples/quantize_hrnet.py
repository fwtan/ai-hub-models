# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
"""
This is a sample script showing how to take a AIMET model zoo model without
pre-computed activations, and compute those activations using QAIHM.

This script assumes the model is added to QAIHM, but is missing quantization parameters.
"""
import argparse
from pathlib import Path

import torch

from qai_hub_models.datasets.coco import CocoDataset
from qai_hub_models.models.hrnet_pose.app import HRNetPoseApp
from qai_hub_models.models.hrnet_pose_quantized.model import HRNetPoseQuantizable


# Create custom data loader for this model that does the preprocessing
class HRNetCocoDataset(CocoDataset):
    def __init__(self, preprocess_lambda, target_image_size=640):
        super().__init__(target_image_size)
        self.preprocess_lambda = preprocess_lambda

    def __getitem__(self, item):
        image, _ = super(CocoDataset, self).__getitem__(item)
        _, _, x = self.preprocess_lambda(image)
        return x


if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num-iter", type=int, default=50, help="Number of batches to use."
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory where encodings should be stored. Defaults to ./build.",
    )
    parser.add_argument(
        "--output-name",
        type=str,
        default=None,
        help="Encodings filename. Defaults to <model_name>_encodings.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Manual seed to ensure reproducibility for quantization.",
    )
    args = parser.parse_args()
    torch.manual_seed(args.seed)

    model = HRNetPoseQuantizable.from_pretrained(aimet_encodings=None)
    app = HRNetPoseApp(model)

    # Initialize Data Loader
    dataset = HRNetCocoDataset(app.preprocess_input)

    # TODO(10491) Add metrics computation here

    # Quantize activations
    model.quantize(dataset, args.num_iter)

    # Export encodings
    output_path = args.output_dir or str(Path() / "build")
    output_name = args.output_name or "hrnet_pose_quantized_encodings"
    model.quant_sim.save_encodings_to_json(output_path, output_name)
