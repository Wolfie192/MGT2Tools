import xml.etree.ElementTree as ET
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QGridLayout
from PyQt6.QtCore import pyqtSignal, Qt

class ControlPanel(QWidget):
    change_text_signal = pyqtSignal(str, str)
    clear_signal = pyqtSignal()
    request_player_show = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Panel")
        self.setStyleSheet("background-color: #0a0b10; color: #00f2ff;")
        self.main_layout = QVBoxLayout()

        group_frame_style = """
            QFrame {
                border: 1px solid #00f2ff;
                border-radius: 10px;
                margin-bottom; 5px;
                background-color: #0d0e1a;
            }
            QLabel { border: none; margin_bottom: 2px; }
        """

        button_style = """
            QPushButton {
                background-color: #1a1a2e;
                border: 2px solid #00f2ff;
                border-radius: 5px;
                color: #00f2ff;
                padding: 10px;
                font-family: 'OCR A Extended';
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00f2ff;
                color: #0a0b10;
            }
            QPushButton:pressed {
                background-color: #008b94;
            }
        """

        xml_path = Path("../screens.xml")
        if xml_path.exists():
            tree = ET.parse(xml_path)
            root = tree.getroot()

            groups = []

            for group in root.findall('group'):
                group_name = group.get('title')
                if group_name not in groups:
                    groups.append(group_name)
                    current_frame = QFrame()
                    current_frame.setStyleSheet(group_frame_style)
                    current_frame_layout = QVBoxLayout(current_frame)
                    current_frame_layout.setSpacing(2)
                    current_frame_layout.setContentsMargins(5, 5, 5, 5)

                    group_label = QLabel(group_name.upper())
                    group_label.setStyleSheet("color: #00f2ff; font-weight: bold; font-size: 14px;")
                    group_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                    current_frame_layout.addWidget(group_label)

                    current_grid = QGridLayout()
                    current_frame_layout.addLayout(current_grid)
                    self.main_layout.addWidget(current_frame)