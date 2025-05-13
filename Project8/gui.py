import sys
from datetime import datetime, timezone

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QListWidget, QVBoxLayout,
    QWidget, QFileDialog, QMessageBox, QLineEdit, QLabel, QHBoxLayout, QDateTimeEdit
)

from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout
)

from PySide6.QtCore import QDateTime
from reader import read_log 
from detail import LogDetailPanel



class LogViewerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTTP Logs Viewer")
        self.resize(1000, 700)

        # currently shown logs
        self.logs = []       
        # all logs loaded from file, not modified
        self.all_logs = []   

        
        self.load_button = QPushButton("Load log file")
        self.log_list = QListWidget()

        
        self.from_date_input = QDateTimeEdit()
        self.from_date_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.from_date_input.setCalendarPopup(True)
        self.from_date_input.setDateTime(QDateTime.currentDateTime())

        self.to_date_input = QDateTimeEdit()
        self.to_date_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.to_date_input.setCalendarPopup(True)
        self.to_date_input.setDateTime(QDateTime.currentDateTime())


        self.filter_button = QPushButton("Filter")
        self.reset_button = QPushButton("Reset")


        left_layout = QVBoxLayout()
        left_layout.addWidget(self.load_button)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("From date:"))
        filter_layout.addWidget(self.from_date_input)
        filter_layout.addWidget(QLabel("To date:"))
        filter_layout.addWidget(self.to_date_input)
        filter_layout.addWidget(self.filter_button)
        filter_layout.addWidget(self.reset_button)

        left_layout.addLayout(filter_layout)
        left_layout.addWidget(self.log_list)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        # rgiht panelwith chosen log details
        self.detail_panel = LogDetailPanel()
        self.detail_panel.hide()

        # main alyout (horizontal)
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget, 2)
        main_layout.addWidget(self.detail_panel, 1)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


        # connect buttons to functions
        self.load_button.clicked.connect(self.load_logs)
        self.filter_button.clicked.connect(self.filter_logs)
        self.reset_button.clicked.connect(self.reset_filters)
        self.log_list.itemClicked.connect(self.show_log_details)



    def load_logs(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choose file with logs", "", "(*.log *.txt);;(*)"
        )

        if not file_path:
            return

        try:
            self.all_logs = read_log(file_path)
            self.logs = self.all_logs.copy()
            self.update_log_list(self.logs)
            self.detail_panel.hide()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failure during reading file:\n{e}")


    def update_log_list(self, log_list=None):
        self.log_list.clear()
        for entry in log_list or self.logs:
            short = f"{entry[0]} {entry[6]} {entry[8]}"
            display = short[:50] + "..." if len(short) > 50 else short
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
            QMessageBox.warning(self, "Error", "Incorrect data format, use YYYY-MM-DD HH:MM:SS")
            return

        filtered = []
        for log in self.all_logs:
            timestamp = log[0]

            if (from_dt and timestamp < from_dt) or (to_dt and timestamp > to_dt):
                continue

            #print(type(timestamp), timestamp.tzinfo)

            filtered.append(log)

        self.logs = filtered
        self.update_log_list(self.logs)


    def reset_filters(self):
        self.from_date_input.clear()
        self.to_date_input.clear()
        self.logs = self.all_logs.copy()
        self.update_log_list(self.logs)
        self.detail_panel.hide()

    # show details of selected log
    # if no log is selected hide the details panel
    # if no logs are loaded hide the details panel
    def show_log_details(self):
        index = self.log_list.currentRow()
        if index < 0 or not self.logs:
            self.detail_panel.hide()
            return

        self.detail_panel.load_logs(self.logs, index)
        self.detail_panel.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogViewerWindow()
    window.show()
    sys.exit(app.exec())

