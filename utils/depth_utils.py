import torch
import cv2
import numpy as np
import os
import sys

# MiDaS 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models', 'midas'))

from models.midas.dpt_depth import DPTDepthModel
from models.midas.transforms import Resize, NormalizeImage, PrepareForNet
from torchvision.transforms import Compose

def estimate_depth(image, model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 모델 로드
    model = DPTDepthModel(
        path=model_path,
        backbone="vitb_rn50_384",
        non_negative=True
    )
    model.eval()
    model.to(device)

    # 전처리
    transform = Compose([
        Resize(
            width=384,
            height=384,
            resize_target=None,
            keep_aspect_ratio=True,
            ensure_multiple_of=32,
            resize_method="minimal",
            image_interpolation_method=cv2.INTER_CUBIC,
        ),
        NormalizeImage(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
        PrepareForNet()
    ])

    input_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) / 255.0
    input_transformed = transform({"image": input_rgb})["image"]
    sample = torch.from_numpy(input_transformed).unsqueeze(0).to(device)

    # 추론
    with torch.no_grad():
        prediction = model.forward(sample)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=image.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze().cpu().numpy()
        prediction = cv2.bilateralFilter(prediction.astype(np.float32), d=9, sigmaColor=0.1, sigmaSpace=5)

    return prediction
