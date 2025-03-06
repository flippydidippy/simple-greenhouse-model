import sys
import json
import numpy as np
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton,
    QLabel, QSplitter, QFrame
)
from PyQt6.QtGui import QPainter, QPen, QFont
from PyQt6.QtCore import Qt

###! THIS IS WIP RIGHT NOW, NOT FINISHED
class GreenhouseVisualizer(QWidget):
    def __init__(self, param_file, df):
        super().__init__()
        self.params = self.load_params(param_file)
        self.df = df
        self.current_index = 0

        self.setWindowTitle("Greenhouse Visualization")
        self.setGeometry(100, 100, 1000, 700)
        #self.setStyleSheet("background: white;")  # 

        self.sidebar = QWidget(self)
        self.sidebar.setFixedWidth(250)
        self.sidebar.setStyleSheet("background: lightgray; border: 1px solid black;")  
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.available_list = QListWidget()
        self.available_list.addItems(list(df.columns))
        self.available_list.setStyleSheet("background: white; color: black; border: 1px solid black;")

        self.displayed_list = QListWidget()
        self.displayed_list.setStyleSheet("background: white; color: black; border: 1px solid black;")

        self.add_button = QPushButton("→") # move back and forth
        self.remove_button = QPushButton("←")
        button_style = "background: gray; color: black; border: 1px solid black;" # styling
        self.add_button.setStyleSheet(button_style) 
        self.remove_button.setStyleSheet(button_style)
        self.add_button.clicked.connect(self.add_variable)
        self.remove_button.clicked.connect(self.remove_variable)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        self.sidebar_layout.addWidget(QLabel("Available Variables:"))
        self.sidebar_layout.addWidget(self.available_list)
        self.sidebar_layout.addLayout(button_layout)
        self.sidebar_layout.addWidget(QLabel("Displayed Variables:"))
        self.sidebar_layout.addWidget(self.displayed_list)
        self.toggle_sidebar_button = QPushButton("☰", self)
        self.toggle_sidebar_button.setFixedSize(40, 40)
        self.toggle_sidebar_button.setStyleSheet(button_style)
        self.toggle_sidebar_button.clicked.connect(self.toggle_sidebar)
        self.time_label = QLabel(f"Time Step: {self.current_index}")
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")

        for btn in [self.prev_button, self.next_button]:
            btn.setStyleSheet(button_style)

        self.prev_button.clicked.connect(self.prev_step)
        self.next_button.clicked.connect(self.next_step)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.prev_button)
        control_layout.addWidget(self.time_label)
        control_layout.addWidget(self.next_button)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(QFrame())  # placeholder
        self.splitter.addWidget(self.sidebar)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.toggle_sidebar_button, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(self.splitter)
        main_layout.addLayout(control_layout)

        self.setLayout(main_layout)

    def load_params(self, file_path):
        """Loads greenhouse parameters from JSON."""
        with open(file_path, "r") as file:
            return json.load(file)

    def toggle_sidebar(self):
        """Show or hide the sidebar for variable selection."""
        self.sidebar.setVisible(not self.sidebar.isVisible())

    def add_variable(self):
        """Move a variable from available list to displayed list."""
        selected_item = self.available_list.currentItem()
        if selected_item:
            var_name = selected_item.text()
            self.displayed_list.addItem(var_name)
            self.available_list.takeItem(self.available_list.row(selected_item))
            self.repaint()

    def remove_variable(self):
        selected_item = self.displayed_list.currentItem()
        if selected_item:
            var_name = selected_item.text()
            self.available_list.addItem(var_name)
            self.displayed_list.takeItem(self.displayed_list.row(selected_item))
            self.repaint()

    def prev_step(self):
        """Move to previous time step."""
        if self.current_index > 0:
            self.current_index -= 1
        self.repaint()

    def next_step(self):
        """Move to next time step."""
        if self.current_index < len(self.df) - 1:
            self.current_index += 1
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.draw_greenhouse(painter)
        self.display_values(painter)


    def draw_greenhouse(self, painter):
        """Draws the greenhouse outline in black."""
        gh_x, gh_y = 300, 200
        gh_width = int(self.params["gh_width"] * 30)
        gh_height = int(self.params["gh_height"] * 30)

        painter.setPen(QPen(Qt.GlobalColor.black, 3)) 
        painter.setBrush(Qt.GlobalColor.transparent)
        painter.drawRect(gh_x, gh_y, gh_width, gh_height)  

        # **Roof**
        roof_height = gh_height // 2
        painter.drawLine(gh_x, gh_y, gh_x + gh_width // 2, gh_y - roof_height)
        painter.drawLine(gh_x + gh_width, gh_y, gh_x + gh_width // 2, gh_y - roof_height)

    def display_values(self, painter):
        """Displays selected variable values at appropriate positions."""
        font = QFont("Arial", 12, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QPen(Qt.GlobalColor.black))

        data_row = self.df.iloc[self.current_index]
        self.time_label.setText(f"Time Step: {self.current_index}")

        positions = {
            "top": (500, 10),
            "air": (500, 200),
            "wall": (100, 200),
            "ground": (500, 600),
            "soil": (500, 600),
            "ext": (100, 600),
            "default": (800, 200)
        }

        label_offsets = {key: 0 for key in positions}

        for index in range(self.displayed_list.count()):
            var = self.displayed_list.item(index).text()
            value = data_row.get(var, "N/A")

            if "top" in var: # different places /cat
                category = "top"
            elif "air" in var:
                category = "air"
            elif "wall" in var:
                category = "wall"
            elif "soil" in var or "ground" in var:
                category = "soil"
            elif "ext" in var:
                category = "ext"
            else:
                category = "default"

            pos_x, pos_y = positions[category]
            pos_y += label_offsets[category]
            label_offsets[category] += 15 

            painter.drawText(pos_x, pos_y, f"{var}: {value:.2f}")

def run_visualizer(param_file, df): # start this vis
    app = QApplication(sys.argv)
    window = GreenhouseVisualizer(param_file, df)
    window.show()
    sys.exit(app.exec())
