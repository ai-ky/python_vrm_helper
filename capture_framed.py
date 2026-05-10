from PIL import ImageGrab, ImageDraw
import pygetwindow as gw
import os

def capture_framed(output_path):
    print(f"🔍 正在尋找角色視窗 'VRM_Desktop_Helper'...")
    helper_windows = gw.getWindowsWithTitle('VRM_Desktop_Helper')
    if not helper_windows:
        print("❌ 找不到視窗！請確保 app.py 正在執行。")
        return

    win = helper_windows[0]
    print(f"📸 擷取畫面並繪製邊框...")
    
    # 1. Capture screen
    screenshot = ImageGrab.grab()
    draw = ImageDraw.Draw(screenshot)
    
    # 2. Draw gray frame around the window
    # Boundary: win.left, win.top, win.left + win.width, win.top + win.height
    rect = [win.left, win.top, win.left + win.width, win.top + win.height]
    # Draw multiple lines to make the border thicker
    for i in range(4):
        draw.rectangle([rect[0]-i, rect[1]-i, rect[2]+i, rect[3]+i], outline=(128, 128, 128))
    
    # 3. Save
    screenshot.save(output_path)
    print(f"✅ 帶邊框截圖已儲存：{output_path}")

if __name__ == "__main__":
    output = r"C:\Users\user\Desktop\python_vrm_helper\screenshot_framed.png"
    capture_framed(output)
