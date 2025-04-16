import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class PDFViewer(QWidget):
    def __init__(self, pdf_path: str):
        super().__init__()
        self.setWindowTitle("PDF Viewer - WebEngine")

        layout = QVBoxLayout(self)
        self.webview = QWebEngineView()

        # 设置自适应大小
        self.webview.setZoomFactor(1.0)
        layout.addWidget(self.webview)

        # 加载本地 PDF 文件（注意需要 file:// 开头）
        self.load_pdf(pdf_path)

    def load_pdf(self, path: str):
        # if not path.startswith("file:///"):
        #     path = "file:///" + path.replace("\\", "/")  # Windows 路径处理
        # pdfjs_url = QUrl.fromUserInput(
        #     "https://mozilla.github.io/pdf.js/web/viewer.html?file=file:///E:/your/path/to.pdf"
        # )

        # self.webview.load(pdfjs_url)
        # # self.webview.load(QUrl(path))
        self.webview.load(QUrl("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置你的 PDF 文件路径
    pdf_path = r"E:\10_Programm\0002_Python\0903_ADP_Ladesaeule_OCPP\github\python_script\test\EVSE_Test\evse-wb-din_latest.pdf"

    viewer = PDFViewer(pdf_path)
    viewer.resize(800, 1000)
    viewer.show()

    sys.exit(app.exec_())
