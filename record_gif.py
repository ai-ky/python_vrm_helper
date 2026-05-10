import pyautogui
import time
import math
import imageio
import numpy as np
from PIL import ImageGrab, ImageDraw
import pygetwindow as gw
import os

def record_lookat_gif(output_path, wait_duration=7, move_duration=6, fps=12):
    print(f"🔍 正在尋找角色視窗 'VRM_Desktop_Helper'...")
    
    helper_windows = gw.getWindowsWithTitle('VRM_Desktop_Helper')
    if not helper_windows:
        print("❌ 找不到視窗！請確保 app.py 正在執行。")
        return

    win = helper_windows[0]
    center_x = win.left + win.width // 2
    center_y = win.top + win.height // 2
    radius = min(win.width, win.height) // 4
    
    print(f"✅ 找到視窗：位置=({win.left}, {win.top}), 大小={win.width}x{win.height}")
    print(f"🎬 開始錄製 (含虛擬滑鼠繪製)...")
    
    frames = []
    start_time = time.time()
    
    total_frames = int((wait_duration + move_duration) * fps)
    wait_frames = int(wait_duration * fps)
    interval = 1.0 / fps
    
    for i in range(total_frames):
        # 1. Update Mouse Position
        if i >= wait_frames:
            progress = (i - wait_frames) / (total_frames - wait_frames)
            angle = progress * 2 * math.pi
            mx = center_x + radius * math.cos(angle)
            my = center_y + radius * math.sin(angle)
            pyautogui.moveTo(mx, my)
        else:
            mx, my = pyautogui.position()
        
        # 2. Capture Frame
        screenshot = ImageGrab.grab()
        
        # 3. Draw "Visible Cursor" manually
        # Since ImageGrab doesn't include the OS cursor, we draw one.
        draw = ImageDraw.Draw(screenshot)
        
        # Draw a bright yellow circle with black outline as a "Cursor Marker"
        # This makes the mouse movement VERY obvious in the tutorial
        r = 12
        draw.ellipse([mx-r, my-r, mx+r, my+r], fill=(255, 255, 0), outline=(0, 0, 0), width=2)
        
        # Draw a small pointer tip
        draw.polygon([(mx, my), (mx+10, my+20), (mx+20, my+10)], fill=(255, 0, 0))

        frame = np.array(screenshot)
        frames.append(frame)
        
        # Precise timing
        elapsed = time.time() - start_time
        expected = (i + 1) * interval
        if expected > elapsed:
            time.sleep(expected - elapsed)
            
    print(f"📦 正在編碼高品質 GIF...")
    imageio.mimsave(output_path, frames, fps=fps, loop=0)
    print(f"✅ 錄製完成：{output_path}")

if __name__ == "__main__":
    output = r"C:\Users\user\Desktop\python_vrm_helper\screenshot_lookat.gif"
    record_lookat_gif(output)
