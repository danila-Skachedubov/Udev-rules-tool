from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QWidget
from udevpy import process_parameters
import sys
import json

class UdevRuleConfigurator(QMainWindow):
    def __init__(self):
        super(UdevRuleConfigurator, self).__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('udev_rules')
        self.setGeometry(100, 100, 300, 200)

        self.device_label = QLabel('Select Device:', central_widget)
        self.device_selector = QComboBox(central_widget)
        self.device_selector.addItems(['USB', 'PCI', 'Network'])
        self.action_label = QLabel('Select Action:', central_widget)
        self.action_selector = QComboBox(central_widget)
        self.action_selector.addItems(['add', 'remove'])

        self.parameters_layout = QVBoxLayout()
        self.add_parameter_button = QPushButton('Add Parameter', central_widget)
        self.add_parameter_button.clicked.connect(self.add_parameter)

        self.generate_button = QPushButton('Generate Rule', central_widget)
        self.generate_button.clicked.connect(self.generate_rule)

        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.device_label)
        layout.addWidget(self.device_selector)
        layout.addWidget(self.action_label)
        layout.addWidget(self.action_selector)
        layout.addLayout(self.parameters_layout)
        layout.addWidget(self.add_parameter_button)
        layout.addWidget(self.generate_button)