import numpy as np
import cv2

def apply_parallax(image, depth_map, shift_x=20):
    h, w = image.shape[:2]

    # 깊이 정규화: 0 ~ 1
    depth_norm = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())

    # 깊이에 따라 픽셀 이동량 계산 (깊을수록 덜 이동)
    flow_map = np.zeros((h, w, 2), dtype=np.float32)
    flow_map[..., 0] = shift_x * (1 - depth_norm)   # x축 이동만 적용
    flow_map[..., 1] = 0                            # y축은 그대로

    # 원래 좌표 계산
    grid_x, grid_y = np.meshgrid(np.arange(w), np.arange(h))
    map_x = (grid_x + flow_map[..., 0]).astype(np.float32)
    map_y = (grid_y + flow_map[..., 1]).astype(np.float32)

    # 리매핑
    shifted = cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return shifted
