import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QPushButton, QVBoxLayout, QHBoxLayout, QListWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QTime, Qt

class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()
        self.time = QTime(0, 0, 0, 0)
        self.time_label = QLabel("00:00:00.00", self)
        self.toggle_button = QPushButton(self)
        self.lap_button = QPushButton(self)
        self.reset_button = QPushButton(self)
        self.lap_list = QListWidget(self)
        self.timer = QTimer(self)
        self.is_running = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Stopwatch")

        vbox = QVBoxLayout()
        vbox.addWidget(self.time_label)

        self.setLayout(vbox)

        self.time_label.setAlignment(Qt.AlignCenter)

        hbox = QHBoxLayout()

        hbox.addWidget(self.toggle_button)
        hbox.addWidget(self.lap_button)
        hbox.addWidget(self.reset_button)

        vbox.addLayout(hbox)
        vbox.addWidget(self.lap_list)

        # Set icons for the buttons
        self.update_toggle_button_icon()
        self.lap_button.setIcon(QIcon('icon_lap.png'))
        self.reset_button.setIcon(QIcon('icon_reset.png'))

        # Modern, minimalistic style
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #FFFFFF;
            }
            QLabel {
                font-size: 80px;
                font-family: 'Segoe UI', sans-serif;
                background-color: #1E1E1E;
                border-radius: 20px;
                padding: 20px;
                margin-bottom: 20px;
            }
            QPushButton {
                font-size: 30px;
                font-family: 'Segoe UI', sans-serif;
                background-color: #0078D4;
                color: #FFFFFF;
                border: none;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            QListWidget {
                font-size: 20px;
                font-family: 'Segoe UI', sans-serif;
                background-color: #1E1E1E;
                color: #FFFFFF;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton#toggle_button {
                padding-left: 20px;
                padding-right: 20px;
            }
        """)

        self.toggle_button.clicked.connect(self.toggle)
        self.lap_button.clicked.connect(self.lap)
        self.reset_button.clicked.connect(self.reset)
        self.timer.timeout.connect(self.update_display)

    def toggle(self):
        if self.is_running:
            self.timer.stop()
            self.is_running = False
        else:
            self.timer.start(10)
            self.is_running = True
        self.update_toggle_button_icon()

    def update_toggle_button_icon(self):
        if self.is_running:
            self.toggle_button.setIcon(QIcon('icon_pause.png'))
        else:
            self.toggle_button.setIcon(QIcon('icon_start.png'))

    def lap(self):
        self.lap_list.addItem(self.format_time(self.time))

    def reset(self):
        self.timer.stop()
        self.is_running = False
        self.time = QTime(0, 0, 0, 0)
        self.time_label.setText(self.format_time(self.time))
        self.lap_list.clear()
        self.update_toggle_button_icon()

    def format_time(self, time):
        hours = time.hour()
        minutes = time.minute()
        seconds = time.second()
        milliseconds = time.msec() // 10
        return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}"

    def update_display(self):
        self.time = self.time.addMSecs(10)
        self.time_label.setText(self.format_time(self.time))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stopwatch = Stopwatch()
    stopwatch.show()
    sys.exit(app.exec_())
