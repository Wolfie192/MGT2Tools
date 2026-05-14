import sys
import os
import xml.etree.ElementTree as ET
import markdown
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QFrame, QGridLayout
from PyQt6.QtCore import pyqtSignal, Qt


# --- THE PLAYER DISPLAY WINDOW ---
# This is the window that "receives" the information.
class PlayerDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Player Display")
        self.setStyleSheet("background-color: #050505; border: 2px solid #003333;")
        self.resize(600, 400)

        # We use a ScrollArea in case the text is longer than the screen
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Force the scroll bars to be hidden so the screen stays clean
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        self.layout=QVBoxLayout(container)
        self.layout.setSpacing(0)

        # --- THE HEADING/TITLE LABEL ---
        self.title_label = QLabel("", self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True)
        # Styled in Amber to differentiate from the Cyan body text
        self.title_label.setStyleSheet("""
            font-size: 56px; 
            color: #ffae00; 
            font-family: 'Courier New', Courier, monospace;
            font-weight: bold;
            margin-bottom: 0px;
            padding-top: 0px;
            padding-bottom: 0px;
        """)

        # Set a consistent height for the title area (approx 1.5x font size)
        self.title_label.setFixedHeight(100)
        # Hide the title label by default until it is needed
        self.title_label.hide()

        # --- THE MAIN BODY TEXT LABEL ---
        self.display_label = QLabel("Welcome Traveller, awaiting information from Referee.", self)
        self.display_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.display_label.setWordWrap(True)

        # Futuristic text styling: Cyan color, bold, and monospaced font
        self.display_label.setStyleSheet("""
            font-size: 32px; 
            color: #00f2ff; 
            font-family: 'Courier New', Courier, monospace;
            font-weight: normal;
        """)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.display_label)
        self.scroll_area.setWidget(container)
        
        # Save the common style traits so we don't have to re-type them
        self.body_style_base = """
            color: #00f2ff;
            font-family: 'Courier New', Courier, monospace;
            font-weight: normal;
        """
        self.html_extra_style = """
            <style>
                body { text-align: left; }
                p { margin-bottom: 25px; }
                ul { margin-left: 20px; color: #00f2ff; }
                li { margin-bottom: 5px; }
                table { border-collapse: collapse; width: 100%; margin-bottom: 20px; border: 1px solid #00f2ff; }
                th { background-color: #1a1a2e; color: #ffae00; padding: 10px; border: 1px solid #00f2ff; font-weight: bold; }
                td { padding: 8px; border: 1px solid #003333; color: #00f2ff; }
                tr:nth-child(even) {background-color: #0d0e1a; }
            </style>
        """

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)

    def resizeEvent(self, event):
        """This ensures text re-fits if you manually stretch the window."""
        super().resizeEvent(event)
        self.fit_text()

    def fit_text(self):
        """Adjusts font size to fill the screen if no title is present."""
        # Ensure text wraps to the current window width before calculating height
        available_width = max(200, self.scroll_area.viewport().width() - 20)
        self.display_label.setFixedWidth(available_width)

        # Calculate height available for content
        # We start with the total window height and subtract a small safety margin (20px)
        max_height = self.scroll_area.viewport().height() - 20
        
        if self.title_label.isVisible():
            # If the title is there, we subtract its fixed height (100px) from the available space
            max_height -= self.title_label.height()

        # Logic: Start big and shrink until it fits the available height
        current_size = 80 
        while current_size > 12:
            self.display_label.setStyleSheet(f"font-size: {current_size}px; {self.body_style_base}")
            # Check if the predicted height of the label fits our window
            if self.display_label.sizeHint().height() <= max_height:
                break
            current_size -= 1 # Shinking by 1px at a time for a more precise fit

    def update_display(self, title, content):
        """This function changes what is on the screen."""

        # Convert Markdown string to HTML and wrap it in a proper body
        markdown_html = markdown.markdown(content, extensions=['tables'])
        html_content = f"<html><body>{self.html_extra_style}{markdown_html}</body></html>"

        if title and title.strip():
            self.title_label.setText(title)
            self.title_label.show()
        else:
            self.title_label.hide()
            
        self.display_label.setText(html_content)
        self.fit_text()

    def clear_screen(self):
        """This function clears the display."""
        self.title_label.setText("")
        self.display_label.setText("")
        self.title_label.hide()


# --- THE CONTROL PANEL WINDOW ---
# This is the window that "sends" the commands.
class ControlPanel(QWidget):
    # We define custom "Signals" - think of these as specific telephone lines
    # that can carry a message (a string of text).
    change_text_signal = pyqtSignal(str, str) # Now carries (Title, Content)
    clear_signal = pyqtSignal()
    request_player_show = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Panel")
        self.setStyleSheet("background-color: #0a0b10; color: #00f2ff;")
        self.main_layout = QVBoxLayout()

        # Futuristic border style for our group containers
        group_frame_style = """
            QFrame {
                border: 1px solid #00f2ff;
                border-radius: 10px;
                margin-bottom: 5px;
                background-color: #0d0e1a;
            }
            QLabel { border: none; margin-bottom: 2px; }
        """

        # This is a shared style for our "Space Buttons"
        button_style = """
            QPushButton {
                background-color: #1a1a2e;
                border: 2px solid #00f2ff;
                border-radius: 5px;
                color: #00f2ff;
                padding: 10px;
                font-family: 'Courier New';
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

        # --- XML PARSING LOGIC ---
        # We load the XML file relative to where this script is saved
        xml_path = "C:/Users/Wolfie/PycharmProjects/MGT2Tools/screens.xml"
        if os.path.exists(xml_path):
            tree = ET.parse(xml_path)
            root = tree.getroot()

            current_group = None
            current_frame = None
            current_frame_layout = None
            current_grid = None
            button_count = 0

            for screen in root.findall('screen'):
                group_name = screen.get('button_group')
                if group_name  != current_group:
                    # Create a container frame for the group
                    current_frame = QFrame()
                    current_frame.setStyleSheet(group_frame_style)
                    current_frame_layout = QVBoxLayout(current_frame)
                    current_frame_layout.setSpacing(2)
                    current_frame_layout.setContentsMargins(5, 5, 5, 5)
                    
                    group_label = QLabel(group_name.upper())
                    group_label.setStyleSheet("color: #00f2ff; font-weight: bold; font-size: 14px;")
                    group_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                    current_frame_layout.addWidget(group_label)
                    
                    # Create a new grid for this new section
                    current_grid = QGridLayout()
                    current_frame_layout.addLayout(current_grid)
                    self.main_layout.addWidget(current_frame)
                    
                    current_group = group_name
                    button_count = 0 # Reset count for the new grid

                screen_title = screen.get('title', "")
                btn_text = screen.get('button_text')
                btn = QPushButton(btn_text)
                btn.setStyleSheet(button_style)

                # --- ADVANCED XML TO MARKDOWN CONVERSION ---
                content_parts = []

                for element in screen:
                    if element.tag == 'paragraph' and element.text:
                        p_heading = element.get('heading')
                        if p_heading:
                            content_parts.append(f"### {p_heading}")
                        content_parts.append(element.text.strip())

                    elif element.tag == 'ul':
                        if element.get('heading'):
                            content_parts.append(f"### {element.get('heading')}")
                        for li in element.findall('li'):
                            bold_part = li.get('bold', '')
                            li_text = li.text.strip() if li.text else ""
                            if bold_part:
                                content_parts.append(f"* **{bold_part}**: {li_text}")
                            else:
                                content_parts.append(f"* {li_text}")

                    elif element.tag == 'table':
                        table_header = element.get('header')
                        if table_header:
                            content_parts.append(f"### {table_header}")
                        else:
                            # If no heading is present, add an empty string to force 
                            # an extra line break when joined later.
                            content_parts.append("")

                        table_lines = [] # Temporary list to build the table's Markdown
                        header_cols_text = "" # Will hold the text for the header row
                        num_cols_for_separator = 1 # Default to 1 column for separator if no info

                        columns_el = element.find('columns')
                        if columns_el is not None and columns_el.text:
                            # Use provided columns for header
                            header_cols_text = columns_el.text.strip()
                            num_cols_for_separator = len(header_cols_text.split('|'))
                        else:
                            # No <columns> tag, so create an empty header row
                            # Try to infer column count from the first row
                            first_row = element.find('row')
                            if first_row is not None and first_row.text:
                                num_cols_for_separator = len(first_row.text.split('|'))
                                header_cols_text = " | ".join([" "] * num_cols_for_separator) # Empty cells
                            else:
                                # If no columns and no rows, just a single empty column
                                header_cols_text = " "
                                num_cols_for_separator = 1
                        
                        # Always add the header (empty or actual) and separator for Markdown to recognize the table
                        table_lines.append(f"| {header_cols_text} |")
                        table_lines.append("|" + "|".join(["---"] * num_cols_for_separator) + "|")

                        # Process rows and any nested paragraphs
                        for child in element:
                            if child.tag == 'row' and child.text:
                                table_lines.append(f"| {child.text.strip()} |")
                            elif child.tag == 'paragraph' and child.text:
                                # If a table was being built, finish it before the paragraph
                                if table_lines:
                                    content_parts.append("\n".join(table_lines))
                                    table_lines = [] # Reset for potential new table
                                content_parts.append(child.text.strip())
                        
                        # Add any remaining table lines (if no paragraph interrupted)
                        if table_lines:
                            content_parts.append("\n".join(table_lines))

                full_content = "\n\n".join(content_parts)
                btn.clicked.connect(lambda checked, t=screen_title, c=full_content: self.change_text_signal.emit(t, c))
                
                # Calculate Row and Column (10 buttons wide)
                row = button_count // 10
                col = button_count % 10
                current_grid.addWidget(btn, row, col)
                button_count += 1

        # --- CONTROLS SECTION ---
        controls_frame = QFrame()
        controls_frame.setStyleSheet(group_frame_style)
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setSpacing(2)
        controls_layout.setContentsMargins(5, 5, 5, 5)
        
        controls_label = QLabel("SYSTEM CONTROLS")
        controls_label.setStyleSheet("color: #00f2ff; font-weight: bold; font-size: 14px;")
        controls_layout.addWidget(controls_label)
        
        controls_grid = QGridLayout()
        controls_layout.addLayout(controls_grid)

        # 1. Re-open Player Window Button
        reopen_btn = QPushButton("Re-open Player Screen")
        reopen_btn.setStyleSheet(button_style)
        reopen_btn.clicked.connect(lambda: self.request_player_show.emit())

        # 2. Clear Button
        clear_btn = QPushButton("Clear Display")
        clear_btn.setStyleSheet(button_style + """
            QPushButton { /* Normal state for Warning/Clear button */
                border: 2px solid #ffae00; /* Amber/Orange warning border */
                color: #ffae00; /* Amber/Orange warning text */
            }
            QPushButton:hover { /* Hover state */
                background-color: #ffae00; /* Fill with amber on hover */
                color: #0a0b10; /* Dark text for contrast */
            }
            QPushButton:pressed { /* Pressed state */
                background-color: #cc8b00; /* Darker amber when pressed */
            }
        """)
        clear_btn.clicked.connect(lambda: self.clear_signal.emit())

        # 3. Exit Button
        exit_btn = QPushButton("Shutdown App")
        exit_btn.setStyleSheet(button_style + """
            QPushButton {
                border: 2px solid #ff4b2b;
                color: #ff4b2b;
            }
        """)
        exit_btn.clicked.connect(QApplication.instance().quit)

        # Add control buttons to the control grid (first row)
        controls_grid.addWidget(reopen_btn, 0, 0)
        controls_grid.addWidget(clear_btn, 0, 1)
        controls_grid.addWidget(exit_btn, 0, 2)

        self.main_layout.addWidget(controls_frame)
        self.setLayout(self.main_layout)

    def closeEvent(self, event):
        """This ensures that if the Control Panel is closed, the whole app exits."""
        QApplication.instance().quit()
        event.accept()


# --- THE MAIN APPLICATION LOGIC ---
def main():
    # Every PyQt app needs one (and only one) QApplication object
    app = QApplication(sys.argv)

    # 1. Create the two windows
    control_window = ControlPanel()
    player_window = PlayerDisplay()

    # 2. "Wire" them together using Signals and Slots
    # This connects the 'telephone lines' from the control panel to the functions in the display
    control_window.change_text_signal.connect(player_window.update_display)
    control_window.request_player_show.connect(player_window.showMaximized)
    control_window.clear_signal.connect(player_window.clear_screen)

    # 3. Show both windows
    # We position the control panel to the left and player to the right
    control_window.move(100, 100)
    player_window.move(450, 100)

    control_window.show()
    player_window.showMaximized()

    # Run the application loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()