# `app.py` 實作與測試計畫

## 1. 目標 (Objective)
使用 Python (`PySide6`) 作為後端，將原本的 Electron 架構重構為 Python 桌面應用程式。`app.py` 需載入 `index.html`，並實現透明背景、無邊框視窗以及與使用者的滑鼠互動和模型物理回饋。

## 2. 實作步驟 (Implementation Steps)

### 2.1 環境與基礎設定
*   確保系統已安裝 `PySide6` (`pip install PySide6`)。
*   建立 `app.py` 檔案。

### 2.2 視窗建置與透明化
*   匯入 `PySide6.QtWidgets.QApplication`, `QMainWindow` 及 `PySide6.QtWebEngineWidgets.QWebEngineView`。
*   設定主視窗屬性為無邊框 (`Qt.FramelessWindowHint`) 與頂層顯示 (`Qt.WindowStaysOnTopHint`)。
*   設定視窗背景透明 (`setAttribute(Qt.WA_TranslucentBackground)`)。
*   設定 `QWebEngineView` 的網頁背景為透明 (`page().setBackgroundColor(Qt.transparent)`)。
*   將 `QWebEngineView` 指向專案目錄下的 `index.html`。

### 2.3 滑鼠互動機制 (拖曳與控制)
*   **左鍵拖曳移動視窗**：覆寫 `QMainWindow` 的 `mousePressEvent` 與 `mouseMoveEvent`，讓使用者可以透過拖曳模型所在視窗來移動。
*   **右鍵互動**：前端 `index.html` 原本可能負責處理滑鼠右鍵的視角旋轉，需確保 PySide6 的 WebEngine 事件有正確傳遞給前端，或者若需要，建立 `QWebChannel` 進行 Python 與 JS 雙向溝通。

### 2.4 物理慣性效果整合
*   在視窗移動時 (在 `mouseMoveEvent` 內) 計算視窗移動的位移量與速度。
*   透過 `QWebEnginePage.runJavaScript()` 將慣性數據傳遞給前端的 Three.js / three-vrm 實體。
*   觸發 VRM 的 SpringBone 以達到髮絲、衣物隨視窗移動而抖動的效果。

## 3. 執行與測試 (Execution & Testing)

### 3.1 啟動應用程式
*   在終端機執行 `python app.py`。

### 3.2 測試項目
*   **視覺測試**：確認 `charactor.vrm` 與 `pose.json` 成功載入，且視窗背景確實為透明，無視窗邊框。
*   **拖曳測試**：使用滑鼠左鍵點擊並拖拽模型，確認視窗會跟隨移動。
*   **操作測試**：使用滑鼠右鍵點擊並拖拽，確認是否能正確旋轉 3D 模型視角。
*   **物理效果測試**：快速移動視窗，觀察模型 (如頭髮、裙擺) 是否有慣性物理抖動效果 (SpringBone 觸發)。
