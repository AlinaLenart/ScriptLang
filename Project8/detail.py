from PySide6.QtWidgets import (
    QWidget, QLabel, QFormLayout, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
import utils


class LogDetailPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.logs = []
        self.index = 0
        self.fields = {}  

        self.labels = [
            "Timestamp", "UID", "Orig Host", "Orig Port", "Resp Host", "Resp Port",
            "Method", "Host", "URI", "Status Code"
        ]

        self.header = QLabel("Log Details")
        self.header.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.header.setStyleSheet("font-size: 24pt; font-weight: bold; margin-bottom: 6px;")
        self.header.setSizePolicy(self.header.sizePolicy().horizontalPolicy(), 
                          QSizePolicy.Fixed)
        

        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        for label in self.labels:
            key_label = QLabel(f"{label}:")
            key_label.setStyleSheet("color: #807e7e; font-weight: bold;")

            value_label = QLabel("")
            value_label.setStyleSheet("color: #ffffcf;") 
            value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

            form_layout.addRow(key_label, value_label)
            self.fields[label] = value_label

        # buttons: next / previous
        self.prev_button = QPushButton("← Previous")
        self.next_button = QPushButton("Next →")

        self.prev_button.clicked.connect(self.show_previous)
        self.next_button.clicked.connect(self.show_next)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.next_button)

        # main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(nav_layout)


        self.setLayout(main_layout)
        self.update_navigation_buttons()


    def load_logs(self, logs, index):
        self.logs = logs
        self.index = index
        self.update_view()


    def update_view(self):
        if not self.logs or not (0 <= self.index < len(self.logs)):
            return

        log = self.logs[self.index]
        for i, val in enumerate(log):
            label = self.labels[i] if i < len(self.labels) else f"Field {i}"
            if label in self.fields:
                widget = self.fields[label]
                widget.setText(str(val))

                # Kolorowanie statusu
                if label == "Status Code":
                    if utils.is_error_code(val):
                        widget.setStyleSheet("color: red; font-weight: bold;")
                    else:
                        widget.setStyleSheet("color: green; font-weight: bold;")


        self.update_navigation_buttons()

    def update_navigation_buttons(self):
        self.prev_button.setEnabled(self.index > 0)
        self.next_button.setEnabled(self.index < len(self.logs) - 1)

    def show_previous(self):
        if self.index > 0:
            self.index -= 1
            self.update_view()

    def show_next(self):
        if self.index < len(self.logs) - 1:
            self.index += 1
            self.update_view()

