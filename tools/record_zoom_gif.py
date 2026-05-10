import pyautogui
import time
import imageio
import numpy as np
from PIL import ImageGrab, ImageDraw
import pygetwindow as gw
import os

def record_zoom_gif(output_path, wait_duration=3, drag_duration=3, zoom_duration=5, fps=12):
    print(f"🔍 正在尋找角色視窗 'VRM_Desktop_Helper'...")
    
    helper_windows = gw.getWindowsWithTitle('VRM_Desktop_Helper')
    if not helper_windows:
        print("❌ 找不到視窗！請確保 app.py 正在執行。")
        return

    win = helper_windows[0]
    
    print(f"✅ 找到視窗：位置=({win.left}, {win.top}), 大小={win.width}x{win.height}")
    print(f"🎬 開始錄製「拖拽與縮放」展示...")
    
    frames = []
    start_time = time.time()
    
    screen_width, screen_height = pyautogui.size()
    target_center_x = screen_width // 2
    target_center_y = screen_height // 2
    
    # Timeline
    total_frames = int((wait_duration + drag_duration + zoom_duration) * fps)
    wait_frames = int(wait_duration * fps)
    drag_frames = int(drag_duration * fps)
    zoom_frames = int(zoom_duration * fps)
    interval = 1.0 / fps
    
    is_dragging = False
    
    for i in range(total_frames):
        # Current mouse pos
        mx, my = pyautogui.position()
        
        if i < wait_frames:
            # Wait stage: Move to window top area
            tx, ty = win.left + win.width // 2, win.top + 20
            mx = mx + (tx - mx) * 0.2
            my = my + (ty - my) * 0.2
            pyautogui.moveTo(mx, my)
            
        elif i < wait_frames + drag_frames:
            # Drag stage
            if not is_dragging:
                pyautogui.mouseDown(button='left')
                is_dragging = True
            
            progress = (i - wait_frames) / drag_frames
            tx = win.left + win.width // 2 + (target_center_x - (win.left + win.width // 2)) * progress
            ty = win.top + 20 + (target_center_y - win.height // 2 - (win.top + 20)) * progress
            pyautogui.moveTo(tx, ty)
            mx, my = tx, ty
            
        else:
            # Zoom stage
            if is_dragging:
                pyautogui.mouseUp(button='left')
                is_dragging = False
                # Move to center for zoom
                pyautogui.moveTo(target_center_x, target_center_y)
                mx, my = target_center_x, target_center_y
            
            # Scroll every few frames
            if i % 10 == 0:
                # Scroll up to zoom in, then down to zoom out
                amount = 200 if (i < wait_frames + drag_frames + zoom_frames // 2) else -200
                pyautogui.scroll(amount)
        
        # Capture
        screenshot = ImageGrab.grab()
        draw = ImageDraw.Draw(screenshot)
        
        # Virtual Cursor
        r = 12
        color = (0, 255, 0) if is_dragging else (255, 255, 0)
        draw.ellipse([mx-r, my-r, mx+r, my+r], fill=color, outline=(0, 0, 0), width=2)
        draw.polygon([(mx, my), (mx+10, my+20), (mx+20, my+10)], fill=(255, 0, 0))

        frame = np.array(screenshot)
        frames.append(frame)
        
        # Precise timing
        elapsed = time.time() - start_time
        expected = (i + 1) * interval
        if expected > elapsed:
            time.sleep(expected - elapsed)
    
    if is_dragging: pyautogui.mouseUp(button='left')
            
    print(f"📦 正在編碼縮放 GIF...")
    imageio.mimsave(output_path, frames, fps=fps, loop=0)
    print(f"✅ 錄製完成：{output_path}")

if __name__ == "__main__":
    output = r"C:\Users\user\Desktop\python_vrm_helper\screenshot_zoom.gif"
    record_zoom_gif(output)
