from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QFont
from udevpy import process_parameters
import sys
import json

class UdevRuleConfigurator(QMainWindow):
    def __init__(self):
        super(UdevRuleConfigurator, self).__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('udev_rules')
        self.setGeometry(100, 100, 400, 300)


        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

        self.option_label = QLabel('Device option:', central_widget)
        self.device_option = QComboBox(central_widget)
        self.device_option.addItems(['Add', 'Remove'])
        self.device_option.setCurrentIndex(-1)

        self.device_label = QLabel('Select Device:', central_widget)
        self.device_selector = QComboBox(central_widget)
        self.device_selector.addItems(['USB'])
        self.device_selector.setCurrentIndex(-1)

        self.action_label = QLabel('Select Action:', central_widget)
        self.action_selector = QComboBox(central_widget)
        self.action_selector.addItems(['AUTHORIZATION', 'RUN SCRIPT', 'NAME', 'MODE', 'GROUP', 'SYMLINK', 'OWNER'])
        self.action_selector.setCurrentIndex(-1)
        self.action_selector.currentIndexChanged.connect(self.show_action_input)

        self.parameters_layout = QVBoxLayout()

        self.add_parameter_button = QPushButton('Add Parameter', central_widget)
        self.add_parameter_button.clicked.connect(self.add_parameter)

        self.generate_button = QPushButton('Generate Rule', central_widget)
        self.generate_button.clicked.connect(self.generate_rule)

        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.option_label)
        layout.addWidget(self.device_option)
        layout.addWidget(self.device_label)
        layout.addWidget(self.device_selector)
        layout.addWidget(self.action_label)
        layout.addWidget(self.action_selector)
        layout.addLayout(self.parameters_layout)
        layout.addWidget(self.add_parameter_button)
        layout.addWidget(self.generate_button)

        self.setStyleSheet("""
            QLabel {
                font-size: 12px;
            }
            QComboBox, QLineEdit {
                font-size: 12px;
                padding: 5px;
            }
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                color: #333333;
                padding: 8px 16px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 12px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)

    def add_parameter(self):
        param_name_label = QLabel('Parameter Name:', self.centralWidget())
        param_value_label = QLabel('Parameter Value:', self.centralWidget())

        param_name_input = QLineEdit(self.centralWidget())
        param_value_input = QLineEdit(self.centralWidget())

        self.parameters_layout.addWidget(param_name_label)
        self.parameters_layout.addWidget(param_name_input)
        self.parameters_layout.addWidget(param_value_label)
        self.parameters_layout.addWidget(param_value_input)

    def generate_rule(self):
        option_device = self.device_option.currentText()
        selected_device = self.device_selector.currentText()
        selected_action = self.action_selector.currentText()

        parameters = {}
        for i in range(0, self.parameters_layout.count(), 4):
            param_name = self.parameters_layout.itemAt(i + 1).widget().text()
            param_value = self.parameters_layout.itemAt(i + 3).widget().text()
            if param_name and param_value:
                parameters[param_name] = param_value

        json_data = json.dumps({'ACTION': option_device, 'SUBSYSTEM': selected_device, 'RULE': selected_action, **parameters})

        process_parameters(json_data)

    def show_action_input(self):
        selected_action = self.action_selector.currentText()
        if selected_action == 'Authorization':
            self.add_authorization_input()
        else:
            self.remove_authorization_input()

    def add_authorization_input(self):
        self.authorization_layout = QHBoxLayout()
        self.authorization_label = QLabel('Authorization:', self.centralWidget())
        self.authorization_selector = QComboBox(self.centralWidget())
        self.authorization_selector.addItems(['Yes', 'No'])
        self.authorization_layout.addWidget(self.authorization_label)
        self.authorization_layout.addWidget(self.authorization_selector)
        self.parameters_layout.addLayout(self.authorization_layout)

    def remove_authorization_input(self):
        if hasattr(self, 'authorization_layout'):
            self.authorization_layout.deleteLater()
            del self.authorization_layout

if __name__ == '__main__':
    app = QApplication([])
    window = UdevRuleConfigurator()
    window.show()
    sys.exit(app.exec_())
