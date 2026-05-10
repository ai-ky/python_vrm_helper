# Python VRM Desktop Helper 完整對話紀錄 (Full Conversation Log)

本文件紀錄了本次開發過程中所有的 User Prompts 與 AI 實作歷程。

---

### 1. 任務啟動與計畫
*   **User**: 先讀取C:\Users\user\Desktop\python_vrm_helper\readme.md並列出重構app.py並執行與測試的計畫，詳細的列出來變成檔案放在專案中
*   **AI**: 讀取 README 並擬定實作計畫 `plan.md`，包含 PySide6 環境建置、透明無邊框實作、滑鼠互動與物理慣性連動。

---

### 2. 核心實作
*   **User**: OK 開始之後一次做完，中間不要停
*   **AI**: 安裝 PySide6，實作 `app.py` 核心邏輯（QWebEngine + QWebChannel），成功啟動透明視窗。

---

### 3. 透明度除錯 (陰影問題)
*   **User**: 程式執行後還是會有視窗外框的陰影，能不能消除到完全無痕
*   **AI**: 加入 `Qt.NoDropShadowWindowHint`。
*   **User**: 還是沒有變化，這會不會是 js 那邊或 css 有需要調整?
*   **AI**: 嘗試強制關閉系統背景 `WA_NoSystemBackground`。
*   **User**: 可以沒變化，是不是可能 index.htm的內容需要調整
*   **AI**: 設定 `QSurfaceFormat` 的 Alpha Buffer。
*   **User**: 還是看得到外框淺灰色的邊和陰影，請參考C:\Users\user\Desktop\3D_Desktop_helper 這個用js做方案，它就沒有陰影，先研究一下有什麼差別，為什麼它沒有陰影和邊框
*   **AI**: 分析 JS 版本，發現 Windows DWM 的 `CS_DROPSHADOW` 屬性問題。透過 `ctypes` 直接呼叫 Windows 原生 API (`user32.dll`) 徹底剔除陰影屬性與標題欄裝飾。**（成功解決）**

---

### 4. 學生教學與動態更新
*   **User**: 把這次專案的實作關鍵細節做記錄，產生一個讓我可以給學生的參考的一次性完成實作的 prompt
*   **AI**: 產出 `Implementation_Details.md` 與專屬教學 Prompt。
*   **User**: 在程式裡面留下可以動態更新資態的函式
*   **AI**: 在 Python (`VRMHost`) 與 JS (`applyPoseData`) 實作動態 JSON 姿態更新通道。

---

### 5. 雙擊切換與事件攔截
*   **User**: 我嘗試調用函式後無效果，找出關鍵原因，我在資料夾底下放了 pose1.json pose2.json 請修改程式然滑鼠雙擊時切換姿態
*   **AI**: 修正 JSON 跳脫問題與檔案路徑，實作雙擊循環切換邏輯。
*   **User**: 雙擊左鍵時沒有發生變化，是不是可能 index.html 和 app.py 之間的互動和即時顯示的機制有問題
*   **AI**: 發現 WebEngine 攔截了所有點擊事件。
*   **User**: 我在 if obj == self.browser and event.type() == QEvent.MouseButtonDblClick: if event.button() == Qt.LeftButton: 加上了 print('ok') 但沒有看到對應輸出，這樣正常嗎? 雙擊後還是無反應
*   **AI**: 實作雙層偵測：在 JS 端監聽 `dblclick` 並透過 QWebChannel 反饋 Python。**（成功解決）**
*   **User**: 成功了… 一樣把相關的實作細節作記錄
*   **AI**: 更新技術報告，加入「事件攔截 (Event Interception)」細節。

---

### 6. 視覺與比例調整
*   **User**: 角色放大一點，另外視窗也要多留一些空間給角色可能會產生的晃動
*   **AI**: 調整 `index.html` 內的渲染高度與視窗連動係數。
*   **User**: 不只是視窗變大，角色也要變大，再把角色調大
*   **AI**: 角色基礎高度提升至 800，緩衝系數提升至 1.35x。
*   **User**: 視窗留的晃動空間太大了，縮緊一點
*   **AI**: 緊湊視窗系數，縮減為 1.15x。
*   **User**: 左右空間留大一點，上下空間留小一點
*   **AI**: 實作獨立的水平/垂直 Padding。

---

### 7. 參考 Mate-Engine 實作 LookAt
*   **User**: 分析下列專案的vrm角色動作相關事件 C:\Users\user\Desktop\codespace\Mate-Engine-Public-Release-X3.3.0
*   **AI**: 深度分析 `AvatarSwayController` 與 `AvatarLocomotionController`。
*   **User**: 看一下 C:\Users\user\Desktop\codespace\Mate-Engine-Public-Release-X3.3.0 裡面臉會朝向滑鼠的程式，它是怎麼做到的
*   **AI**: 分析 `AvatarMouseTracking.cs`，總結其座標轉換與骨骼權重控制。
*   **User**: 請再目前的專案中加入類似 AvatarMouseTracking.cs 的功能
*   **AI**: 在 `index.html` 加入 3D 座標映射與 `vrm.lookAt`。
*   **User**: 執行並除錯
*   **AI**: 修正 ES Modules 導入問題與 `Clock` 錯誤，將 `index.html` 模組化。
*   **User**: LookAt 未正常運作，且角色亮度太高了
*   **AI**: 調低燈光強度，加入色彩空間校正。
*   **User**: LookAt 一樣沒有正常發揮，前測看看讓角色固定看右邊，我看一下有沒有可以正常控制視線
*   **AI**: 診斷 VRM 1.0 的 LookAt Applier 自動更新問題。
*   **User**: 好像沒有運作成功，重新執行一次
*   **AI**: 改為手動顯式呼叫 `lookAt.update(dt)`。
*   **User**: 還是不行… 可以要從 pose.json 直接處理
*   **AI**: **關鍵修正**：在 Pose 套用時排除 `head/neck` 骨骼，並改採手動計算 Euler 角度。
*   **User**: 他的頭會轉動了… 可是上下相反，左右相反，焦距不對且轉得太劇烈了…沒有直視中間的時刻
*   **AI**: 翻轉正負號，加入 `lerp` 平滑濾波，修正映射範圍。
*   **User**: 角色消失了
*   **AI**: 修正 `getWorldPosition` TypeError（物件類型錯誤）。
*   **User**: 和滑鼠的關係上下左右相反了
*   **AI**: 重新調整 Yaw/Pitch 正負號與靈敏度。**（成功解決）**

---

### 8. 最終功能整合與總結
*   **User**: 太暗了調亮一點，加入功能，滑鼠滾輪可以放大縮小角色，視窗大小也跟著角色大小一樣調整，長寬都保留0.3倍的空間
*   **AI**: 實作滾輪 Zoom 功能與同步視窗縮放模型。
*   **User**: 環境光與直射光強度及toneMappingExposure改為 0.8，視窗的長與寬都會比角色本體多出 0.1倍
*   **AI**: 精準調優亮度至 0.8，將緩衝空間縮減為 0.1x。
*   **User**: 上下左右的轉頭幅度可以再大一點，亮度等設定參考 C:\Users\user\Desktop\python_vrm_helper_TEMP\index.html
*   **AI**: 讀取 TEMP 設定（恢復亮度至 2.4），將 `maxYaw` 提升至 0.8，`maxPitch` 提升至 0.5。
*   **User**: 把「跟隨滑鼠移動」的功能實作注意事項寫入
*   **AI**: 更新 `Implementation_Details.md` 加入座標歸一化、骨骼衝突排除等細節。
*   **User**: 先記錄目前所有對話的內容，再記錄重點整理總結後的內容
*   **AI**: 產出 `Conversation_Log.md` 與 `Project_Summary.md`。
*   **User**: Conversation_Log.md 應該要存完整的對話內容(至少我每次下的prompt都要有)，你有辦法取得嗎
*   **AI**: 重新取得並整理完整的全對話歷程紀錄。

---

### 9. 教學素材與互動網頁開發
*   **User**: 以上內容可以做成教學簡報嗎? 請上網搜尋有沒有相關的skill，我如果要做一個教學「手把手教你做桌面小幫手」…
*   **AI**: 產出 Marp 格式簡報 `Tutorial_Presentation.md`，將開發過程拆解為五大教學步驟。
*   **User**: 把簡報做成互動網頁的形式，再幫我啟動程式並擷出程式運行圖片範例，不同的功能給不同的圖片範例嵌在教學網頁中
*   **AI**: 實作 `Tutorial_Web.html` 互動網頁。自動編寫 PowerShell 與 Python 腳本擷取實機畫面。
*   **User**: 第一張圖改用現在剪貼範裡面的
*   **AI**: 實作剪貼簿讀取腳本 `save_clipboard.ps1`，成功擷取自訂圖片。
*   **User**: 第3張圖改成動態的gif，再開一次程式在移動滑鼠於視茖周圍繞圓的狀態下重新的擷取，可以先上網找找有沒有擷取gif的skill可供參考
*   **AI**: 整合 `pyautogui` 與 `imageio`。
*   **User**: 要先確定程式啟動之後，滑鼠等一下再移動gif沒錄到程式執行狀況，要先確定程式啟動之後，滑鼠等約7秒再移動並同時錄製gif
*   **AI**: 優化錄製腳本 `record_gif.py`，加入精準的時間控制。
*   **User**: 滑鼠要繞角色的視窗內部繞圈，請先擷取解色視窗的位置及大小再動作
*   **AI**: 修改 `app.py` 加入唯一視窗標題，並讓錄製腳本自動偵測視窗座標進行「內部繞圈」。
*   **User**: 錄製的時候明顯沒有錄到滑鼠，想辦法解決的這個問題，滑鼠要明顯
*   **AI**: **關鍵技術**：實作虛擬游標繪製邏輯。在 GIF 每一幀手動畫上「亮黃色圓圈 + 紅色箭頭」，徹底解決系統錄影隱藏下游標的問題。
*   **User**: 第4張一樣改gif demo 雙擊更換姿勢 啟動程式後去角色的視窗中心做雙擊，過程中同時錄下雙擊後更更換姿勢的效果
*   **AI**: 實作 `record_pose_gif.py`。自動執行雙擊，並在點擊瞬間讓虛擬游標「閃爍紅色」以強化視覺提示。
*   **User**: 第5張也改gif demo 滑鼠滾輪縮放與自適應視窗 程式執行後先用滑鼠左鍵選萬視窗拖到螢幕中央，再滾輸縮放，過程做錄影變gif。第1張改成程式執行後擷圖，但做一要影像處理，把角色視窗的周圍用灰線框起來
*   **AI**: 實作自動化拖拽與縮放錄製。實作 `capture_framed.py` 透過影像處理為 Step 1 畫上邊框。
*   **User**: 第1張 and 第2張圖要demo原本有帶框及陰影的版本，請重新實作一個新project來demo
*   **AI**: 建立 `python_vrm_helper_original` 臨時專案。
*   **User**: 沒有顯示到 vrm 角色
*   **AI**: 修正 Demo 程式碼缺失的通訊 Slot，並延長載入等待時間至 12 秒，成功捕捉到包含角色的「Before」對比圖。

---

### 10. 專案組織與 GitHub Pages 上架
*   **User**: capture_framed.py 這類型過程中用到的工具另外放一個資料夾，教學網頁及相關檔案再放另一個資料夾(做成github靜態網頁，幫我上架一下)
*   **AI**: 建立 `tools` 與 `docs` 資料夾。將自動化腳本移入 `tools`，將教學網頁與 GIF 素材移入 `docs` 並重新命名為 `index.html` 以符合 GitHub Pages 規範。更新 `README.md` 指向新路徑並加入線上教學連結。
*   **AI**: 執行 Git Commit 與 Push，並引導使用者開啟 GitHub Pages 設定。
