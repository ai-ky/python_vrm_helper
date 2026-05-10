# Python VRM Desktop Helper 實作技術報告

本專案成功將原基於 Electron 的 3D 桌面助手重構為 Python 版本。以下是實現「完全透明、無視窗感」的關鍵技術細節。

## 1. 關鍵技術挑戰與解決方案

### A. 視窗透明度與 WebEngine 渲染
在 Windows 上，單純設定 `Qt.WA_TranslucentBackground` 往往不足以讓 `QWebEngineView` 內容完全透明，背景常會出現黑色或不透明塊。
*   **解決方案**：必須在 `QApplication` 實例化前設定 `QSurfaceFormat`。
    ```python
    fmt = QSurfaceFormat()
    fmt.setAlphaBufferSize(8) # 啟用 8-bit Alpha 通道
    QSurfaceFormat.setDefaultFormat(fmt)
    ```

### B. 徹底消除系統陰影與邊框
Windows DWM (桌面視窗管理員) 會強制為頂層視窗添加裝飾。即使使用了 `Qt.FramelessWindowHint`，有時仍會殘留淡淡的灰色陰影。
*   **解決方案**：利用 `ctypes` 呼叫 Windows 原生 API 移除視窗類別的 `CS_DROPSHADOW` 屬性。
    ```python
    user32.SetClassLongW(hwnd, GCL_STYLE, class_style & ~CS_DROPSHADOW)
    ```

### C. 跨網域與本地檔案存取 (CORS)
WebEngine 出於安全考慮會限制存取本地 3D 模型檔案。
*   **解決方案 1**：在 Python 端實作 `QWebChannel`，將模型轉換為 Base64 字串傳遞給 JS。
*   **解決方案 2**：設定 WebEngine 屬性允許本地檔案互訪。
    ```python
    settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
    ```

### D. 物理慣性回饋
為了讓模型「動起來」，我們在 Python 端捕捉視窗位移速度，並透過 `runJavaScript` 或 `QWebChannel` 通知前端的 Three.js 更新 VRM 的 SpringBone。

### E. 事件攔截與雙擊機制 (Event Interception)
在嵌入 `QWebEngineView` 時，所有的滑鼠事件預設會被網頁引擎優先攔截，導致父視窗無法接收到 `mouseDoubleClickEvent`。
*   **解決方案**：
    1.  **Python 端**：對 `browser.focusProxy()` 安裝 `eventFilter`，在事件抵達網頁前攔截。
    2.  **JS 端 (更穩健)**：在網頁內監聽 `dblclick` 事件，並透過 `QWebChannel` 反向呼叫 Python 的 Slot 函式。
    ```javascript
    // JS 端反向呼叫 Python
    window.vrmHost.triggerNextPose();
    ```

### F. 即時姿態更新與字串處理
從 Python 推送複雜的 JSON 數據給 JS 時，字串的跳脫 (Escape) 是常見的錯誤點。
*   **解決方案**：使用 `json.dumps()` 處理所有的數據內容，確保換行符號與引號在 `runJavaScript` 中能被正確解析為合法的 JS 字串參數。

### G. 跟隨滑鼠移動 (LookAt / Head Rotation)
實作「角色盯著滑鼠看」的功能時，必須處理座標映射與骨骼衝突問題。
*   **座標歸一化與平滑**：
    將滑鼠在視窗內的座標轉換為 `-1.0` 到 `1.0` 的區間，並使用 `lerp` 進行濾波處理。這能賦予頭部轉動一種「物理重量感」，避免滑鼠快速移動時造成角色閃現或劇烈抖動。
*   **骨骼衝突排除 (Pose Exclusion)**：
    這是最容易被忽略的細節。當程式從 `pose.json` 套用全身動作時，必須**主動跳過 head 與 neck 骨骼**的 Quaternion 設定。否則，靜態的動作資料會每一幀強行覆蓋動態的滑鼠追蹤數據，導致角色「轉不動」。
*   **手動計算旋轉 (Manual Rotation)**：
    不依賴 `three-vrm` 的自動 LookAt 組件（其受限於模型預設設定），直接對 `humanoid.getNormalizedBoneNode('head')` 進行 `rotation.set(pitch, yaw, 0)`。
*   **正負號校正 (Sign Correction)**：
    - **Yaw (左右)**：通常與滑鼠水平位移同向。
    - **Pitch (上下)**：須注意網頁座標系與 3D 座標系的 Y 軸方向相反，必須正確翻轉正負號，才能達成「滑鼠往上，角色抬頭」的效果。

---

## 2. 實作 Prompt (給學生的參考版本)

您可以將以下 Prompt 提供給 AI（如 Gemini, GPT-4），即可一次性生成高品質的實作方案：

> **Prompt：**
> 「請扮演資深 Python 工程師，使用 PySide6 與 Three.js 實作一個 3D 桌面助手，並滿足以下要求：
> 1. **視窗特性**：完全透明背景、無標題欄、無視窗陰影（須使用 ctypes 移除 Windows 原生陰影）、視窗最上層顯示。
> 2. **3D 渲染**：使用 QWebEngineView 載入 index.html，利用 Three.js 與 @pixiv/three-vrm 載入 VRM 模型。
> 3. **通訊機制**：實作 QWebChannel 雙向溝通。
>    - Python -> JS：傳遞模型二進位數據與動態姿態 JSON。
>    - JS -> Python：偵測網頁雙擊並通知 Python 切換動作。
> 4. **互動邏輯**：
>    - 左鍵拖拽：移動視窗。
>    - 左鍵雙擊：循環切換目錄下的 `pose.json`, `pose1.json`, `pose2.json`。
>    - 物理回饋：視窗移動時帶動 VRM 髮絲物理慣性抖動。
> 5. **穩健性優化**：使用 json.dumps 處理傳遞給 JS 的數據，並使用 QSurfaceFormat 解決 Windows 透明渲染問題。
> 請提供完整且可直接執行的 app.py 與 index.html 關鍵修改。」

---

## 3. 專案目錄結構
*   `app.py`: 負責視窗管理、系統 API 呼叫與 Python-JS 橋接。
*   `index.html`: 負責 WebGL 渲染、VRM 載入與動畫更新。
*   `charactor.vrm`: 3D 模型本體。
*   `pose.json`: 角色姿勢數據。
