from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt


class LogDetailWindow(QWidget):
    def __init__(self, logs, current_index, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Szczegóły loga")
        self.resize(500, 400)

        self.logs = logs
        self.index = current_index

        # Widżety
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.info_label.setWordWrap(True)

        self.prev_button = QPushButton("Poprzedni")
        self.next_button = QPushButton("Następny")

        # Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        layout = QVBoxLayout()
        layout.addWidget(self.info_label)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Połączenia sygnałów
        self.prev_button.clicked.connect(self.show_previous)
        self.next_button.clicked.connect(self.show_next)

        self.update_view()

    def update_view(self):
        log = self.logs[self.index]
        self.info_label.setText(self.format_log(log))

        # Dezaktywacja przycisków na brzegach
        self.prev_button.setDisabled(self.index == 0)
        self.next_button.setDisabled(self.index == len(self.logs) - 1)

    def format_log(self, log):
        labels = [
            "Timestamp", "UID", "Orig Host", "Orig Port", "Resp Host", "Resp Port",
            "Method", "Host", "URI", "Status code"
        ]
        formatted = []
        for i, value in enumerate(log):
            label = labels[i] if i < len(labels) else f"Field {i}"
            formatted.append(f"{label}: {value}")
        return "\n".join(formatted)

    def show_previous(self):
        if self.index > 0:
            self.index -= 1
            self.update_view()

    def show_next(self):
        if self.index < len(self.logs) - 1:
            self.index += 1
            self.update_view()
