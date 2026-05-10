# Python VRM Desktop Helper

這是一個使用 Python (PySide6) + Webview (Three.js/VRM) 實作的 3D 桌面助手。
功能與原版 Electron 版本相同，但使用 Python 作為後端。

## 錄影展示 (Demos)

### 1. 視線追蹤 (LookAt)
角色眼神與頭部會平滑跟隨滑鼠移動：
![LookAt Demo](screenshot_lookat.gif)

### 2. 動態切換姿勢 (Double Click)
左鍵雙擊角色可即時切換不同的 Pose：
![Pose Demo](screenshot_pose.gif)

### 3. 視窗拖拽與滾輪縮放
支援自由移動視窗，並透過滾輪即時縮放角色與視窗大小：
![Zoom Demo](screenshot_zoom.gif)

## 功能
- **透明背景與無邊框視窗**：解決 Windows 陰影問題，達成無視窗邊界感。
- **載入 VRM 模型** (`charactor.vrm`)
- **套用 Pose** (`pose.json`)
- **滑鼠互動**：
  - 左鍵拖拽：移動視窗 (觸發物理慣性)
  - 右鍵拖拽：旋轉模型
  - 滑鼠滾輪：動態縮放角色與視窗
  - 左鍵雙擊：切換動作
  - 物理效果：移動時模型會有慣性抖動（觸發髮絲等 SpringBone）

## 安裝需求
需安裝 Python 3.10+ 以及 PySide6：

```bash
pip install PySide6
```

## 執行方式
在專案目錄下執行：

```bash
python app.py
```

## 檔案說明
- `app.py`: Python 主程式，負責建立視窗、透明化設定以及透過 QWebChannel 與 JS 溝通。
- `index.html`: 渲染層，使用 Three.js 與 three-vrm 進行 3D 渲染，並處理物理模擬。
- `charactor.vrm`: 預設載入的模型檔案。
- `pose.json`: 預設載入的姿勢檔案。
- `Tutorial_Web.html`: 互動式開發教學網頁。
- `Implementation_Details.md`: 詳細技術實作報告。
