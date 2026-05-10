# Python VRM Desktop Helper 重點總結

本專案將複雜的 3D 渲染與 Windows 系統底層操作完美結合，開發出一個「無視窗邊界感」的桌面助手。以下為本次開發的核心技術精華：

## 1. 真正的「無視窗感」
*   **關鍵字**：`ctypes`, `CS_DROPSHADOW`, `WA_TranslucentBackground`
*   **技術點**：普通的透明視窗在 Windows 下仍有裝飾陰影。我們透過 `user32.SetClassLongW` 從 Window Class 層級強制抹除 `CS_DROPSHADOW` 樣式，並配合 `QSurfaceFormat` 的 Alpha 通道設定，達成與桌面背景 100% 的無縫混合。

## 2. 跨語言高效通訊 (Python ↔ JS)
*   **關鍵字**：`QWebChannel`, `Base64`, `Slot`
*   **技術點**：為解決網頁瀏覽器無法直接讀取本地二進位檔案 (CORS) 的限制，我們在 Python 端實作了檔案讀取 Slot，將 VRM 模型轉換為 Base64 數據傳給前端。同時利用 `QWebChannel` 讓 JS 事件（如雙擊）能即時回傳 Python。

## 3. 動態物理追蹤與姿態疊加
*   **關鍵字**：`Manual Bone Manipulation`, `Pose Exclusion`, `Lerp`
*   **技術點**：
    *   **視線追蹤**：手動操作 `head` 骨骼的 `Euler` 旋轉，而非依賴受限的內建組件。
    *   **衝突解決**：在套用 Pose 時精確排除正在被動態控制的骨骼（Head/Neck），達成「身體做固定動作，頭部跟隨滑鼠」的複合動態。
    *   **慣性平滑**：使用線性插值 (`lerp`) 與 `MathUtils` 讓大幅度轉頭變得平滑，消除機械感。

## 4. 自適應視窗縮放系統
*   **關鍵字**：`Bounding Box`, `Aspect Ratio`, `Wheel Event`
*   **技術點**：建立了一套數學模型，能夠在角色缩放時：
    1.  自動計算 3D 模型的真實像素邊界。
    2.  精準連動調整 `QMainWindow` 的物理寬高。
    3.  自動維持 **10% (0.1x)** 的視覺緩衝區，確保動作晃動不破圖。

---
## 未來擴展建議：
*   **語音連動**：可參考 `Mate-Engine` 加入音訊監聽，讓角色隨電腦播放的音樂擺動。
*   **系統托盤**：將視窗控制（如重載、隱藏）整合至 Windows 托盤圖示。
