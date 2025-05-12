import sys
from datetime import datetime, timezone

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QListWidget, QVBoxLayout,
    QWidget, QFileDialog, QMessageBox, QLineEdit, QLabel, QHBoxLayout
)
from reader import read_log 
from detail import LogDetailWindow



class LogViewerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Przeglądarka logów HTTP (PySide6)")
        self.resize(800, 600)

        self.logs = []       # aktualnie wyświetlane logi
        self.all_logs = []   # pełny zbiór logów, niezmieniony

        # Widżety główne
        self.load_button = QPushButton("Wczytaj plik z logami")
        self.log_list = QListWidget()

        # Widżety filtrów
        self.from_date_input = QLineEdit()
        self.from_date_input.setPlaceholderText("Od (YYYY-MM-DD HH:MM)")

        self.to_date_input = QLineEdit()
        self.to_date_input.setPlaceholderText("Do (YYYY-MM-DD HH:MM)")

        self.filter_button = QPushButton("Filtruj")
        self.reset_button = QPushButton("Resetuj filtry")

        # Układ główny
        layout = QVBoxLayout()
        layout.addWidget(self.load_button)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Od:"))
        filter_layout.addWidget(self.from_date_input)
        filter_layout.addWidget(QLabel("Do:"))
        filter_layout.addWidget(self.to_date_input)
        filter_layout.addWidget(self.filter_button)
        filter_layout.addWidget(self.reset_button)

        layout.addLayout(filter_layout)
        layout.addWidget(self.log_list)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Połączenia sygnałów
        self.load_button.clicked.connect(self.load_logs)
        self.filter_button.clicked.connect(self.filter_logs)
        self.reset_button.clicked.connect(self.reset_filters)


    def load_logs(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Wybierz plik z logami", "", "Pliki tekstowe (*.log *.txt);;Wszystkie pliki (*)"
        )

        if not file_path:
            return

        try:
            self.all_logs = read_log(file_path)
            self.logs = self.all_logs.copy()
            self.update_log_list(self.logs)

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wczytać pliku:\n{e}")

    def update_log_list(self, log_list=None):
        self.log_list.clear()
        for entry in log_list or self.logs:
            short = f"{entry[0]} {entry[6]} {entry[8]}"
            display = short[:30] + "..." if len(short) > 30 else short
            self.log_list.addItem(display)
            self.log_list.itemClicked.connect(self.show_log_details)


    def filter_logs(self):
        from_text = self.from_date_input.text()
        to_text = self.to_date_input.text()

        try:
            from_dt = datetime.strptime(from_text, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc) if from_text else None
            to_dt = datetime.strptime(to_text, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc) if to_text else None
            print(from_dt, to_dt)

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Niepoprawny format daty. Użyj YYYY-MM-DD HH:MM:SS.")
            return

        filtered = []
        for log in self.all_logs:
            print(log)
            timestamp = log[0]

            # DEBUG: pokaż szczegóły porównania
            print(f"[DEBUG] timestamp: {timestamp} | from_dt: {from_dt} | to_dt: {to_dt}")

            if (from_dt and timestamp < from_dt) or (to_dt and timestamp > to_dt):
                print(f"[DEBUG] -> ODRZUCAM: {timestamp}")
                continue

            print(f"[DEBUG] -> AKCEPTUJĘ: {timestamp}")
            print(type(timestamp), timestamp.tzinfo)

            filtered.append(log)

        self.logs = filtered
        self.update_log_list(self.logs)


    def reset_filters(self):
        self.from_date_input.clear()
        self.to_date_input.clear()
        self.logs = self.all_logs.copy()
        self.update_log_list(self.logs)

    def show_log_details(self, item):
        index = self.log_list.currentRow()
        self.detail_window = LogDetailWindow(self.logs, index)
        self.detail_window.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogViewerWindow()
    window.show()
    sys.exit(app.exec())

