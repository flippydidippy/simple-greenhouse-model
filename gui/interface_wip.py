import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QLineEdit, QFormLayout, QInputDialog

from simulation.run import run_simulation  #
from validate.run_validation_data import validate_simulation 
from analysis.optimize import optimize_greenhouse_design
from greenhouse_setups.params import update_params 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Greenhouse Simulation")
        self.setGeometry(100, 100, 400, 300)  # window size of now 
        layout = QVBoxLayout()
        self.config_button = QPushButton("Configure Parameters / Greenhouse")
        self.simulation_button = QPushButton("Run Simulation")
        self.validation_button = QPushButton("Validate Model")
        self.optimize_button = QPushButton("Optimize Parameters to Crops")
        self.config_button.clicked.connect(self.open_config_window)
        self.simulation_button.clicked.connect(self.open_simulation_window)
        self.validation_button.clicked.connect(self.open_validation_window)
        self.optimize_button.clicked.connect(self.open_optimization_window)
        layout.addWidget(QLabel("Welcome to the Greenhouse Simulation!"))
        layout.addWidget(self.config_button)
        layout.addWidget(self.simulation_button)
        layout.addWidget(self.validation_button)
        layout.addWidget(self.optimize_button)
        central_widget = QWidget() # central widget
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
    def open_config_window(self): # open config
        self.config_window = ConfigWindow()
        self.config_window.show()

    def open_simulation_window(self): # open sim
        self.simulation_window = SimulationWindow()
        self.simulation_window.show()

    def open_validation_window(self): # open validation 
        self.validation_window = ValidationWindow()
        self.validation_window.show()

    def open_optimization_window(self): # open opt
        self.optimization_window = OptimizationWindow()
        self.optimization_window.show()

CONFIG_FOLDER = "greenhouse_setups"

os.makedirs(CONFIG_FOLDER, exist_ok=True)

def load_params(file_path):
    """Loads a JSON configuration file as a dictionary."""
    with open(file_path, "r") as file:
        return json.load(file)

def save_params(params, file_path):
    """Saves the dictionary as a JSON file."""
    with open(file_path, "w") as file:
        json.dump(params, file, indent=4)


# config
class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Configure Greenhouse Parameters")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Configure parameters from file:")
        layout.addWidget(self.label)  #title
        self.load_button = QPushButton("Load Parameters") # buttons
        self.save_button = QPushButton("Save Parameters")
        self.new_button = QPushButton("Create New Configuration")

        self.load_button.clicked.connect(self.load_parameters)
        self.save_button.clicked.connect(self.save_parameters)
        self.new_button.clicked.connect(self.create_new_configuration)

        layout.addWidget(self.load_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.new_button)

        self.form_layout = QFormLayout()
        self.fields = {} 
        layout.addLayout(self.form_layout)

        self.setLayout(layout)

        self.current_file = None 

    def load_parameters(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Parameter File", CONFIG_FOLDER, "JSON Files (*.json)")
        
        if file_name:
            try:
                params = load_params(file_name)
                self.current_file = file_name 
                self.display_parameters(params)
                QMessageBox.information(self, "Parameters Loaded", f"Parameters loaded from {os.path.basename(file_name)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load parameters: {str(e)}")

    def save_parameters(self):
        if not self.current_file:
            QMessageBox.warning(self, "Warning", "No configuration file is currently loaded!")
            return

        params = {key: float(self.fields[key].text()) if self.fields[key].text().replace('.', '', 1).isdigit() else self.fields[key].text()
                  for key in self.fields}

        try:
            save_params(params, self.current_file)
            QMessageBox.information(self, "Parameters Saved", f"Parameters saved to {os.path.basename(self.current_file)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save parameters: {str(e)}")

    def create_new_configuration(self):
        new_name, ok = QInputDialog.getText(self, "New Configuration", "Enter new configuration name:")
        
        if ok and new_name.strip():
            new_file = os.path.join(CONFIG_FOLDER, f"{new_name.strip()}.json")

            if os.path.exists(new_file):
                QMessageBox.warning(self, "Warning", "A configuration with this name already exists!")
                return

            default_params = {
                "gh_length": 12.53,
                "gh_width": 14,
                "gh_height": 3,
                "h_conv": 21.23,
                "vent_rate": 0.85,
                "solar_absorp": 30.95,
                "plant_transpiration_rate": 0.0001,
                "soil_depth": 5,
                "soil_conduct": 1.80,
                "thermal_mass": 498.97,
                "wall_conductivity": 0.03,
                "wall_thickness": 0.01,
                "wall_emissivity": 0.3
            }

            save_params(default_params, new_file)
            self.current_file = new_file  # Set new file as active
            self.display_parameters(default_params)

            QMessageBox.information(self, "New Configuration", f"New configuration '{new_name.strip()}.json' created successfully!")

    ### 📌 Display Parameters in Editable Fields ###
    def display_parameters(self, params):
        """Displays parameters in input fields for editing."""
        # Clear existing fields
        for key in self.fields:
            self.form_layout.removeRow(self.fields[key])
        
        self.fields.clear()

        for key, value in params.items():
            input_field = QLineEdit(str(value))
            self.form_layout.addRow(f"{key}:", input_field)
            self.fields[key] = input_field

class SimulationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Run Greenhouse Simulation")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        self.label = QLabel("Select weather data file:")
        self.run_button = QPushButton("Run Simulation")

        self.run_button.clicked.connect(self.run_simulation)

        layout.addWidget(self.label)
        layout.addWidget(self.run_button)
        self.setLayout(layout)

    def run_simulation(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Weather Data", "", "CSV Files (*.csv)")
        if file_name:
            run_simulation(file_name)
            QMessageBox.information(self, "Simulation Complete", "Simulation has been successfully completed.")

class ValidationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Validate Model")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        self.label = QLabel("Validate the model against real-world data:")
        self.validate_button = QPushButton("Validate Model")

        self.validate_button.clicked.connect(self.run_validation)

        layout.addWidget(self.label)
        layout.addWidget(self.validate_button)
        self.setLayout(layout)

    def run_validation(self):
        validate_simulation()
        QMessageBox.information(self, "Validation Complete", "Model validation is complete. Check results.")

class OptimizationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Optimize Parameters")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        self.label = QLabel("Optimize parameters for crops:")
        self.optimize_button = QPushButton("Run Optimization")

        self.optimize_button.clicked.connect(self.run_optimization)

        layout.addWidget(self.label)
        layout.addWidget(self.optimize_button)
        self.setLayout(layout)

    def run_optimization(self):
        optimize_greenhouse_design()
        QMessageBox.information(self, "Optimization Complete", "Parameter optimization is done.")


