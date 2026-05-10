# Python VRM Desktop Helper

這是一個使用 Python (PySide6) + Webview (Three.js/VRM) 實作的 3D 桌面助手。
功能與原版 Electron 版本相同，但使用 Python 作為後端。

## 功能
- **透明背景與無邊框視窗**
- **載入 VRM 模型** (`charactor.vrm`)
- **套用 Pose** (`pose.json`)
- **滑鼠互動**：
  - 左鍵拖拽：移動視窗 (觸發物理慣性)
  - 右鍵拖拽：旋轉模型
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
- `plan.md`: 重構計畫紀錄。
