import cv2
import os
import threading
import time
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk

# 📂 이미지 폴더 설정 (사용자 경로로 변경)
folder_path = r"C:\Users\400T6B\Desktop\coloabimage"

# 📜 폴더 내 이미지 파일 가져오기
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
image_files.sort()

if not image_files:
    print("폴더에 이미지 파일이 없습니다.")
    exit()

# 현재 이미지 인덱스 및 선택한 이미지 저장
index = 0
checked_images = set()
slideshow_running = False  # 슬라이드쇼 상태


# 📸 이미지 업데이트 함수
def update_image():
    img_path = os.path.join(folder_path, image_files[index])
    img = cv2.imread(img_path)

    if img is None:
        return

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = img.resize((500, 400))  # 윈도우 크기에 맞게 조절
    img_tk = ImageTk.PhotoImage(img)

    image_label.config(image=img_tk)
    image_label.image = img_tk

    # 체크된 이미지 표시
    if image_files[index] in checked_images:
        status_label.config(text="✅ 선택됨", fg="green")
    else:
        status_label.config(text="❌ 선택 안됨", fg="red")


# ⬅ 이전 이미지
def prev_image():
    global index
    index = (index - 1) % len(image_files)
    update_image()


# ➡ 다음 이미지
def next_image():
    global index
    index = (index + 1) % len(image_files)
    update_image()


# ✅ 체크/해제
def toggle_check():
    if image_files[index] in checked_images:
        checked_images.remove(image_files[index])
    else:
        checked_images.add(image_files[index])
    update_image()


# 🎬 슬라이드쇼 실행
def start_slideshow():
    global slideshow_running
    slideshow_running = True
    slideshow_thread = threading.Thread(target=run_slideshow)
    slideshow_thread.start()


# 🖼️ 슬라이드쇼 함수 (3초마다 변경)
def run_slideshow():
    global slideshow_running
    checked_list = list(checked_images)

    if not checked_list:
        status_label.config(text="❌ 선택된 이미지 없음", fg="red")
        slideshow_running = False
        return

    for img_name in checked_list:
        if not slideshow_running:
            return

        img_path = os.path.join(folder_path, img_name)
        img = cv2.imread(img_path)
        if img is None:
            continue

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = img.resize((500, 400))
        img_tk = ImageTk.PhotoImage(img)

        image_label.config(image=img_tk)
        image_label.image = img_tk
        status_label.config(text=f"📷 {img_name}", fg="blue")

        time.sleep(3)  # 3초마다 변경


# 🛑 슬라이드쇼 중지
def stop_slideshow():
    global slideshow_running
    slideshow_running = False


# 🏠 Tkinter GUI 생성
root = tk.Tk()
root.title("이미지 뷰어")
root.geometry("600x600")

# 🖼️ 이미지 표시 라벨
image_label = Label(root)
image_label.pack()

# ✅ 체크 상태 표시
status_label = Label(root, text="❌ 선택 안됨", fg="red", font=("Arial", 12))
status_label.pack()

# 🖲️ 버튼 UI
btn_prev = Button(root, text="⬅ 이전", command=prev_image, width=10)
btn_prev.pack(side="left", padx=10, pady=10)

btn_check = Button(root, text="✅ 선택/해제", command=toggle_check, width=12)
btn_check.pack(side="left", padx=10, pady=10)

btn_next = Button(root, text="➡ 다음", command=next_image, width=10)
btn_next.pack(side="left", padx=10, pady=10)

btn_start = Button(root, text="🎬 슬라이드 시작", command=start_slideshow, width=15, bg="green", fg="white")
btn_start.pack(side="left", padx=10, pady=10)

btn_stop = Button(root, text="🛑 슬라이드 중지", command=stop_slideshow, width=12, bg="red", fg="white")
btn_stop.pack(side="left", padx=10, pady=10)

# 🎬 첫 번째 이미지 로드
update_image()

# 🏃‍♂️ 실행
root.mainloop()