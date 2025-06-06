# 3D Depth Effect

단일 2D 이미지를 입력으로 받아, MiDaS 딥러닝 모델을 활용한 깊이 예측과 OpenCV 기반 시차 효과(parallax effect)를 통해 입체감 있는 이미지 표현을 구현하는 프로젝트입니다.

## 🔍 Project Overview
이 프로젝트는 2D 이미지 한 장에서 MiDas 모델을 활용해 깊이를 추정하고, 깊이에 따라 픽셀을 이동시켜 입체적인 효과를 연출합니다. 

## 🎯 Motivation
소품샵 [프레젠트모먼트(PRESENT MOMENT)](https://presentmoment.kr/85/?idx=150#prod_detail_detail)에서 본 월레스와 그로밋 3D 렌티큘러 카드에서 영감을 받았습니다 ~

## 🎥 Demo Video
[![Watch the video](https://img.youtube.com/vi/tYM8hmwlflc/0.jpg)](https://youtu.be/tYM8hmwlflc?si=88IS8XDW7v8pksEm)

## 🖼️ Depth map output 
![Depth Map](images/output.png)
가까운 영역은 밝게, 먼 영역은 어둡게!


## 🔧 Features
- **MiDaS 모델 기반 깊이 추정**  
  DPT-Hybrid 모델 (`dpt_hybrid_384.pt`)을 활용하여 단일 RGB 이미지로부터 픽셀별 상대 깊이 정보를 예측합니다.

- **시차 효과 (Parallax Effect)**  
  예측된 깊이를 바탕으로 가까운 픽셀은 더 많이, 먼 픽셀은 덜 이동시키는 방식으로 입체감 있는 움직임을 구현합니다.

- **Z-Buffer 기반 깊이 충돌 방지 및 픽셀 재배치**  
  픽셀이 이동한 이후, 깊이에 따라 겹침을 방지하여 현실감 있는 시차 표현을 유도합니다.

- **OpenCV 기반 Inpainting 및 경계 Blur 처리**  
  픽셀 이동으로 생기는 공백을 `cv2.inpaint`로 보완하고, Sobel edge + Gaussian blur를 이용해 경계선을 자연스럽게 합니다. 

- **자동 움직임 or 마우스 기반 인터랙션**  
  기본적으로는 `np.sin` 기반 자동 움직임을 구현했으며, 주석을 해제하면 마우스를 따라 움직이는 인터랙션도 가능합니다.

## 📚 References
깊이 추정은 Intelligent Systems Lab (ISL)에서 제공하는 MiDaS 저장소의 코드 및 모델 가중치를 포함하고 있습니다. `midas` 디렉토리 전체를 이용하여 단일 이미지 기반의 깊이 추정을 수행하였습니다.  
MiDaS 코드는 MIT 라이선스 하에 배포되며, 자세한 내용은 아래 링크를 참고해 주세요.

- [MiDaS: Monocular Depth Estimation](https://github.com/isl-org/MiDaS)

또한, 데모에 사용된 이미지는 [WallpaperBetter](https://www.wallpaperbetter.com/ko)에서 다운로드하였습니다.

  
