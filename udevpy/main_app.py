from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QFont
import signal
import sys
import json

class UdevRuleConfigurator(QMainWindow):
    def __init__(self):
        super(UdevRuleConfigurator, self).__init__()

        self.setup_signals()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.param_widgets = []

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
        self.action_selector.addItems(['RUN', 'NAME', 'MODE', 'GROUP', 'SYMLINK', 'OWNER'])
        self.action_selector.setCurrentIndex(-1)
        self.action_selector.currentIndexChanged.connect(self.show_action_input)

        self.kernel_label = QLabel('Select Kernel:', central_widget)
        self.kernel_selector = QComboBox(central_widget)
        self.kernel_selector.addItems(['ttyUSB*', 'console', 'lp*'])
        self.kernel_selector.setCurrentIndex(-1)

        self.parameter_input_label = QLabel('Enter Value:', central_widget)
        self.parameter_input = QLineEdit(central_widget)
        self.parameter_input.hide()

        self.add_parameter_button = QPushButton('Add Parameter', central_widget)
        self.add_parameter_button.clicked.connect(self.add_parameter)

        self.generate_button = QPushButton('Generate Rule', central_widget)
        self.generate_button.clicked.connect(self.generate_rule)

        self.disable_connection_checkbox = QCheckBox('Disable Connection')

        self.param_name_input = None
        self.param_value_input = None

        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.option_label)
        layout.addWidget(self.device_option)
        layout.addWidget(self.kernel_label)
        layout.addWidget(self.kernel_selector)
        layout.addWidget(self.device_label)
        layout.addWidget(self.device_selector)
        layout.addWidget(self.action_label)
        layout.addWidget(self.action_selector)
        layout.addWidget(self.parameter_input_label)
        layout.addWidget(self.parameter_input)
        layout.addWidget(self.disable_connection_checkbox)
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

        layout = self.centralWidget().layout()
        layout.insertWidget(layout.count() - 2, param_name_label)
        layout.insertWidget(layout.count() - 2, param_name_input)
        layout.insertWidget(layout.count() - 2, param_value_label)
        layout.insertWidget(layout.count() - 2, param_value_input)
        self.param_widgets.append((param_name_input, param_value_input))

    def generate_rule(self):
        option_device = self.device_option.currentText()
        selected_device = self.device_selector.currentText()
        selected_action = self.action_selector.currentText()
        selected_kernel = self.kernel_selector.currentText()

        parameters = {}

        layout = self.centralWidget().layout()
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if isinstance(item, QHBoxLayout):
                param_name_widget = item.itemAt(1).widget()
                param_value_widget = item.itemAt(3).widget()
                if isinstance(param_name_widget, QLabel) and isinstance(param_value_widget, QLineEdit):
                    param_name = param_name_widget.text()
                    param_value = param_value_widget.text()
                    if param_name and param_value:
                        parameters[param_name] = param_value

        param_value = self.parameter_input.text()


        for param_name_input, param_value_input in self.param_widgets:
            param_name_value = param_name_input.text()
            param_value_value = param_value_input.text()
            if param_name_value and param_value_value:
                parameters[param_name_value] = param_value_value


        rule = {}

        if option_device or selected_device or selected_kernel:

            rule = {
                "ACTION": option_device.lower(),
                "KERNEL": selected_kernel.lower(),
                "SUBSYSTEM": selected_device.lower(),
                "ATTRS": {key: value for key, value in parameters.items()},
                selected_action : param_value,
                "authorized" : self.is_disable_connection_checked()
            }


        json_string = json.dumps(rule, indent=2)
        print(json_string)

        self.close()

    def show_action_input(self):
        selected_action = self.action_selector.currentText()
        if selected_action:
            self.parameter_input_label.show()
            self.parameter_input.show()
        else:
            self.parameter_input_label.hide()
            self.parameter_input.hide()

    def is_disable_connection_checked(self):
        return 0 if self.disable_connection_checkbox.isChecked() else 1

    def setup_signals(self):
        signal.signal(signal.SIGINT, self.close)

    def cleanup(self):
        pass

if __name__ == '__main__':
    app = QApplication([])
    window = UdevRuleConfigurator()
    window.show()

    app.aboutToQuit.connect(window.cleanup)
    sys.exit(app.exec_())
