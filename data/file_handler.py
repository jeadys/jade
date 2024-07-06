import os
import json
from PySide2 import QtWidgets


def get_open_file_name():
    response = QtWidgets.QFileDialog.getOpenFileName(
        caption="Select a file",
        directory=os.getcwd(),
        filter="JSON files (*.json);;All Files (*)"
    )
    return response[0]


def get_save_file_name():
    response = QtWidgets.QFileDialog.getSaveFileName(
        caption="Save file",
        directory=os.getcwd(),
        filter="JSON files (*.json);;All Files (*)",
        initialFilter="JSON files (*.json)"
    )
    return response[0]


def save_data_to_file(file_path, data):
    if not file_path:
        print("No file path provided")
        return False

    if not data:
        print("No data to save")
        return False
    try:
        with open(file_path, 'w') as file:
            file.write(data)
        print(f"Data saved to {file_path}")
        return True
    except IOError as e:
        print(f"Error writing to file: {e}")

    return False


def read_data_from_file(file_path):
    if not file_path:
        print("No file path provided")
        return False

    if not file_path.endswith(".json"):
        print("No JSON file provided")
        return False

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        print(f"Data read from {file_path}")
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")

    return None
