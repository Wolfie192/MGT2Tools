from PyQt6.QtWidgets import QWidget, QTextEdit, QFrame, QVBoxLayout
from PyQt6.QtGui import QTextOption


class PlayerDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Player Display")
        self.setStyleSheet("background-color: #050505; border: 2px solid #003333;")
        self.resize(600, 400)

        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setSpacing(0)

        self.text_browser = QTextEdit(self)
        self.text_browser.setReadOnly(True)
        self.text_browser.setFrameShape(QFrame.Shape.NoFrame)
        self.text_browser.setWordWrapMode(QTextOption.WrapMode.WordWrap)

        self.text_browser_style_base = """
            color: #00f2ff;
            font-family: 'OCR A Extended', 'OCR-A', 'Courier New', monospace;
            font-weight: normal;
        """

        self.layout.addWidget(self.text_browser)

    def resizeEvent(self, event):
        """This ensures text re-fits if you manually stretch the window."""
        super().resizeEvent(event)
        self.fit_text()

    def fit_text(self):
        """Adjusts contents to fit the screen."""
        available_width = max(200, self.text_browser.viewport().width() - 20)
        available_height = self.text_browser.viewport().height() - 20

        text_size = 48
        while text_size > 12:
            self.text_browser.setStyleSheet(f"font-size: {text_size}px; {self.text_browser_style_base}")
            if self.text_browser.sizeHint().height() <= available_height:
                break
            text_size -= 4

    def clear_screen(self):
        self.text_browser.setText("")