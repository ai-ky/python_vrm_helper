import pyautogui
import time
import imageio
import numpy as np
from PIL import ImageGrab, ImageDraw
import pygetwindow as gw
import os

def record_pose_gif(output_path, wait_duration=5, after_click_duration=5, fps=12):
    print(f"🔍 正在尋找角色視窗 'VRM_Desktop_Helper'...")
    
    helper_windows = gw.getWindowsWithTitle('VRM_Desktop_Helper')
    if not helper_windows:
        print("❌ 找不到視窗！請確保 app.py 正在執行。")
        return

    win = helper_windows[0]
    center_x = win.left + win.width // 2
    center_y = win.top + win.height // 2
    
    print(f"✅ 找到視窗：位置=({win.left}, {win.top}), 大小={win.width}x{win.height}")
    print(f"🎬 開始錄製「雙擊更換姿勢」展示...")
    
    frames = []
    start_time = time.time()
    
    # Total frames
    wait_frames = int(wait_duration * fps)
    total_frames = int((wait_duration + after_click_duration) * fps)
    interval = 1.0 / fps
    
    clicked = False
    
    for i in range(total_frames):
        # 1. Update Mouse Position
        if i == wait_frames:
            # Time to double click!
            print("🖱️ 正在執行雙擊...")
            pyautogui.moveTo(center_x, center_y)
            pyautogui.doubleClick()
            clicked = True
        elif i < wait_frames:
            # Move mouse slowly to center to show intent
            progress = i / wait_frames
            curr_mx, curr_my = pyautogui.position()
            target_mx = center_x
            target_my = center_y
            # Simplified lerp for recording
            mx = curr_mx + (target_mx - curr_mx) * 0.1
            my = curr_my + (target_my - curr_my) * 0.1
            pyautogui.moveTo(mx, my)
        
        mx, my = pyautogui.position()
        
        # 2. Capture Frame
        screenshot = ImageGrab.grab()
        draw = ImageDraw.Draw(screenshot)
        
        # 3. Draw Virtual Cursor
        r = 12
        # If we just clicked, flash red to indicate the double click
        color = (255, 0, 0) if (clicked and i < wait_frames + 5) else (255, 255, 0)
        draw.ellipse([mx-r, my-r, mx+r, my+r], fill=color, outline=(0, 0, 0), width=2)
        draw.polygon([(mx, my), (mx+10, my+20), (mx+20, my+10)], fill=(255, 0, 0))

        frame = np.array(screenshot)
        frames.append(frame)
        
        # Precise timing
        elapsed = time.time() - start_time
        expected = (i + 1) * interval
        if expected > elapsed:
            time.sleep(expected - elapsed)
            
    print(f"📦 正在編碼姿勢切換 GIF...")
    imageio.mimsave(output_path, frames, fps=fps, loop=0)
    print(f"✅ 錄製完成：{output_path}")

if __name__ == "__main__":
    output = r"C:\Users\user\Desktop\python_vrm_helper\screenshot_pose.gif"
    record_pose_gif(output)
