import os
import cv2
import numpy as np

frame_idx = 0       # 프레임 인덱스 (시간 흐름 기반 자동 이동용)
MAX_SHIFT = 20      # 픽셀 최대 이동량 (시차 효과 최대 크기)

shift_x = int(np.sin(frame_idx / 30) * MAX_SHIFT)

from utils.depth_utils import estimate_depth
from utils.parallax_utils import apply_parallax

IMAGE_PATH = "images/input.jpeg"
MODEL_PATH = "models/midas/dpt_hybrid_384.pt"

image = None
depth = None

# 마우스를 이용해서 수동으로 시차 적용도 가능
# def on_mouse(event, x, y, flags, param):
#    global shift_x
#    if event == cv2.EVENT_MOUSEMOVE:
#        shift_x = (x - param['center']) // 20 

def main():
    global image, depth, shift_x

    if not os.path.exists(IMAGE_PATH):
        print("[ERROR] 입력 이미지가 존재하지 않습니다:", IMAGE_PATH)
        return

    image = cv2.imread(IMAGE_PATH)
    if image is None:
        print("[ERROR] 이미지를 불러올 수 없습니다.")
        return

    print("[INFO] Depth Map 추정 중...")
    depth = estimate_depth(image, MODEL_PATH)       # MiDaS를 통해 깊이 맵 추정

    depth_vis = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cv2.imwrite("images/output.png", depth_vis)

    print("[INFO] Parallax Viewer 실행 중...")
    center_x = image.shape[1] // 2

    cv2.namedWindow("Parallax Viewer")
    # cv2.setMouseCallback("Parallax Viewer", on_mouse, {'center': center_x})

    frame_idx = 0 

    while True:
        shift_x = int(np.sin(frame_idx / 25) * MAX_SHIFT)
        shifted = apply_parallax(image, depth, shift_x=shift_x)     # 시차 효과 적용
        frame_idx += 1
        cv2.imshow("Parallax Viewer", shifted)

        key = cv2.waitKey(10)
        if key == 27:  
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

def apply_parallax(image, depth, shift_x):
    h, w = image.shape[:2]
    output = np.zeros_like(image)
    z_buffer = np.full((h, w), np.inf)          # Z-buffer 초기화 (깊이 비교용)
    mask = np.zeros((h, w), dtype=np.uint8)     # 픽셀 이동 표시용 마스크

    norm_depth = cv2.normalize(depth, None, 0, 1, cv2.NORM_MINMAX)      # 깊이 정규화: 0 ~ 1로 스케일링 (깊이가 클수록 먼 거리)

    x_range = range(w)
    if shift_x < 0:
        x_range = reversed(x_range)     # 왼쪽으로 이동 시, 오른쪽 픽셀부터 처리

    for y in range(h):
        for x in x_range:
            depth_weight = 1 - norm_depth[y, x]
            shift = int(np.clip(shift_x * depth_weight, -30, 30))
            new_x = x + shift

            if 0 <= new_x < w:
                if norm_depth[y, x] < z_buffer[y, new_x]:
                    output[y, new_x] = image[y, x]
                    z_buffer[y, new_x] = norm_depth[y, x]
                    mask[y, new_x] = 255

    output_inpainted = cv2.inpaint(output, 255 - mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)        # 빈 공간을 자연스럽게 채우기 (inpainting)

    sobelx = cv2.Sobel(norm_depth, cv2.CV_64F, 1, 0, ksize=5)       # Sobel 필터로 x 방향 경계 검출 → 움직인 픽셀 경계 감지용
    sobel_mask = np.uint8(np.clip(np.abs(sobelx) * 255, 0, 255))
    dilated_edge = cv2.dilate(sobel_mask, np.ones((9,9), np.uint8), iterations=2)

    strong_blur = cv2.GaussianBlur(output_inpainted, (15, 15), 0)

    alpha = (dilated_edge / 255.0).astype(np.float32)       # 경계 영역에만 블러를 부드럽게 섞기 위한 알파 마스크 생성
    alpha = cv2.merge([alpha] * 3)
    blended = (alpha * strong_blur + (1 - alpha) * output_inpainted).astype(np.uint8)        # 블러 처리된 이미지와 원본을 혼합 (엣지만 부드럽게)

    return blended





      

     




