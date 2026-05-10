---
marp: true
theme: default
paginate: true
backgroundColor: #f5f5f5
---

# 🚀 手把手教你做：Python 3D 桌面小幫手
### 從零開始實作一個透明、互動、有物理感的 VRM 角色

製作人：AI 助教
日期：2026年5月10日

---

## 🎯 課程目標
*   理解 **PySide6** 如何管理桌面視窗。
*   掌握 **Three.js + VRM** 在 WebEngine 中的渲染技術。
*   實作 **Python 與 JavaScript** 的雙向通訊 (QWebChannel)。
*   解決 Windows 系統底層的透明度與陰影問題。

---

## 🛠️ 技術棧 (Tech Stack)
*   **後端**：Python 3.10+, PySide6 (Qt for Python)。
*   **前端**：Three.js, @pixiv/three-vrm (WebGL 渲染)。
*   **底層**：Windows API (ctypes) 進行視窗裝飾移除。

---

## 🏗️ 第一步：建立透明地基
### 實作一個「完全隱形」的 Python 視窗

*   使用 `Qt.FramelessWindowHint` 移除邊框。
*   設定 `WA_TranslucentBackground` 開啟透明。
*   **關鍵細節**：設定 `QSurfaceFormat` 的 Alpha Buffer 為 8，確保 WebEngine 內容能正確混合桌面。

```python
fmt = QSurfaceFormat()
fmt.setAlphaBufferSize(8)
QSurfaceFormat.setDefaultFormat(fmt)
```

---

## 🧱 第二步：移除 Windows 原生陰影
### 解決「淡淡的灰色邊框」問題

Windows 系統預設會給頂層視窗加上 `CS_DROPSHADOW` 陰影。
必須透過 `ctypes` 直接呼叫 `user32.dll`：

```python
hwnd = self.winId()
user32 = ctypes.windll.user32
class_style = user32.GetClassLongW(hwnd, GCL_STYLE)
user32.SetClassLongW(hwnd, GCL_STYLE, class_style & ~CS_DROPSHADOW)
```

---

## 🌉 第三步：搭建通訊橋樑
### QWebChannel：Python ↔ JS 雙向奔赴

*   **Python 送資料**：讀取本地 VRM 轉 Base64 傳給 JS (解決 CORS 問題)。
*   **JS 傳事件**：雙擊角色、偵測縮放，反向通知 Python 調整視窗。

```javascript
// JS 調用 Python
window.vrmHost.triggerNextPose();
```

---

## 💃 第四步：讓角色「活起來」
### 物理慣性與視線追蹤 (LookAt)

*   **物理感**：視窗移動時計算位移 Delta，同步更新 VRM 的 SpringBone。
*   **眼神對焦**：將滑鼠座標映射到 3D 空間，手動計算 `head` 骨骼旋轉。
*   **防鎖死**：在套用 Pose JSON 時，必須排除 head 骨骼，避免衝突。

---

## 🔍 第五步：視覺細節調優
### 亮度與比例的平衡

*   **光影**：使用 `sRGB` 色彩空間與 `toneMappingExposure` 控制質感。
*   **自適應縮放**：
    *   計算 3D 模型的 Bounding Box。
    *   滾輪縮放時，同步調整視窗物理寬高。
    *   保留 **0.1x** 的晃動緩衝區。

---

## 🎓 總結：你的第一個桌面伴侶
*   **完全透明**：無視窗感，像活在桌面上。
*   **深度互動**：雙擊換裝、眼神跟隨、滾輪縮放。
*   **高性能**：WebGL 渲染 + Python 系統管理。

---

## 🚀 下一步？
*   加入語音連動（音樂響起時跳舞）。
*   整合 AI 對話（讓角色能說話）。
*   增加系統掛件（顯示 CPU/記憶體狀態）。

# Q&A 時間
