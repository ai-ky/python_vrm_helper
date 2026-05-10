import sys
import os
import json
import base64
import ctypes
from PySide6.QtCore import Qt, QUrl, QPoint, QObject, Slot, QRect, QEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtGui import QSurfaceFormat, QColor

# Native Windows Constants
GWL_STYLE = -16
WS_CAPTION = 0x00C00000
WS_THICKFRAME = 0x00040000
GCL_STYLE = -26
CS_DROPSHADOW = 0x00020000

class VRMHost(QObject):
    def __init__(self, window):
        super().__init__()
        self.window = window

    @Slot(int, int)
    def dragWindowBy(self, dx, dy):
        pos = self.window.pos()
        self.window.move(pos.x() + dx, pos.y() + dy)

    @Slot(int, int)
    def fitWindowToModel(self, width, height):
        new_width = max(100, width)
        new_height = max(100, height)
        self.window.resize(new_width, new_height)

    @Slot(str, result=str)
    def readTextFile(self, filename):
        try:
            path = os.path.join(os.path.dirname(__file__), filename)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print(f"Error reading text file {filename}: {e}")
        return ""

    @Slot(str, result=str)
    def readBinaryFile(self, filename):
        try:
            path = os.path.join(os.path.dirname(__file__), filename)
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            print(f"Error reading binary file {filename}: {e}")
        return ""

    @Slot()
    def closeWindow(self):
        QApplication.quit()

    @Slot()
    def triggerNextPose(self):
        # 此 Slot 供前端雙擊後呼叫
        print("Received triggerNextPose from JS")
        self.window.cyclePose()

    @Slot(str)
    def updatePose(self, json_data):
        content = ""
        if isinstance(json_data, str) and not json_data.startswith('{'):
            potential_path = os.path.join(os.path.dirname(__file__), json_data)
            if os.path.exists(potential_path):
                try:
                    with open(potential_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    print(f"Error reading file {potential_path}: {e}")
                    return
        else:
            content = json_data

        safe_content = json.dumps(content)
        self.window.browser.page().runJavaScript(
            f"if(window.applyPoseData) {{ window.applyPoseData({safe_content}); 'OK'; }} else {{ 'ERROR_JS_NOT_READY'; }}",
            lambda result: print(f"JS Update Result: {result}")
        )

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pose_index = 0
        self.poses = ["pose.json", "pose1.json", "pose2.json"]

        # 1. Window setup
        self.setWindowTitle("VRM_Desktop_Helper")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        
        self.resize(520, 820)

        # 2. WebEngineView setup
        self.browser = QWebEngineView(self)
        self.setCentralWidget(self.browser)
        
        self.browser.page().setBackgroundColor(Qt.transparent)
        self.browser.setAttribute(Qt.WA_TranslucentBackground)
        self.browser.setStyleSheet("background: transparent; border: none;")
        
        self.channel = QWebChannel()
        self.host_obj = VRMHost(self)
        self.channel.registerObject("vrmHost", self.host_obj)
        self.browser.page().setWebChannel(self.channel)

        # 改用對 focusProxy 安裝過濾器，這在某些系統上更有效
        if self.browser.focusProxy():
            self.browser.focusProxy().installEventFilter(self)
        self.browser.installEventFilter(self)

        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.ShowScrollBars, False)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.browser.setUrl(local_url)

    def eventFilter(self, obj, event):
        # 捕捉雙擊
        if event.type() == QEvent.MouseButtonDblClick:
            print(f"Native Double Click Detected on {obj}")
            if event.button() == Qt.LeftButton:
                self.cyclePose()
                return True
        return super().eventFilter(obj, event)

    def cyclePose(self):
        self.pose_index = (self.pose_index + 1) % len(self.poses)
        target_pose = self.poses[self.pose_index]
        print(f"Switching to Pose: {target_pose}")
        self.host_obj.updatePose(target_pose)

    def showEvent(self, event):
        super().showEvent(event)
        self.apply_native_fixes()

    def apply_native_fixes(self):
        if sys.platform == "win32":
            hwnd = self.winId()
            user32 = ctypes.windll.user32
            class_style = user32.GetClassLongW(hwnd, GCL_STYLE)
            if class_style & CS_DROPSHADOW:
                user32.SetClassLongW(hwnd, GCL_STYLE, class_style & ~CS_DROPSHADOW)
            style = user32.GetWindowLongW(hwnd, GWL_STYLE)
            style &= ~(WS_CAPTION | WS_THICKFRAME)
            user32.SetWindowLongW(hwnd, GWL_STYLE, style)
            user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0027)

if __name__ == "__main__":
    os.environ["QTWEBENGINE_WIDGETS_LOG_LEVEL"] = "1"
    fmt = QSurfaceFormat()
    fmt.setAlphaBufferSize(8)
    fmt.setSamples(4)
    QSurfaceFormat.setDefaultFormat(fmt)
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec())
