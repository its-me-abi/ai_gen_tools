import sys
import yaml
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QTreeView, QTabWidget, QVBoxLayout,
    QWidget, QTextEdit, QPushButton
)
from PySide6.QtGui import QStandardItemModel, QStandardItem

class YAMLViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YAML Viewer")

        # Create the central widget with tabs
        self.tabs = QTabWidget()

        # Create the tree view tab
        self.tree_view_tab = QWidget()
        self.tree_view = QTreeView()
        self.tree_layout = QVBoxLayout()
        self.tree_layout.addWidget(self.tree_view)
        self.tree_view_tab.setLayout(self.tree_layout)

        # Create the text view tab
        self.text_view_tab = QWidget()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_layout = QVBoxLayout()
        self.text_layout.addWidget(self.text_edit)
        self.text_view_tab.setLayout(self.text_layout)

        # Add tabs to QTabWidget
        self.tabs.addTab(self.tree_view_tab, "Tree View")
        self.tabs.addTab(self.text_view_tab, "Text View")

        # Load button to open YAML file
        self.load_button = QPushButton("Open YAML File")
        self.load_button.clicked.connect(self.load_yaml_file)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.load_button)
        layout.addWidget(self.tabs)

        # Create central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_yaml_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open YAML File", "", "YAML Files (*.yaml *.yml)")
        if file_path:
            with open(file_path, 'r') as f:
                try:
                    data = yaml.safe_load(f)

                    # Prepare tree view
                    model = QStandardItemModel()
                    model.setHorizontalHeaderLabels(['Key', 'Value'])
                    self.populate_tree(model.invisibleRootItem(), data)
                    self.tree_view.setModel(model)
                    self.tree_view.expandAll()

                    # Prepare text view
                    self.text_edit.setPlainText(yaml.dump(data, sort_keys=False, default_flow_style=False,indent=7))

                except yaml.YAMLError as e:
                    print(f"YAML parse error: {e}")

    def populate_tree(self, parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                key_item = QStandardItem(str(key))
                if isinstance(value, (dict, list)):
                    value_item = QStandardItem("")
                    self.populate_tree(key_item, value)
                else:
                    value_item = QStandardItem(str(value))
                parent.appendRow([key_item, value_item])
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                key_item = QStandardItem(f"[{idx}]")
                if isinstance(item, (dict, list)):
                    value_item = QStandardItem("")
                    self.populate_tree(key_item, item)
                else:
                    value_item = QStandardItem(str(item))
                parent.appendRow([key_item, value_item])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = YAMLViewer()
    viewer.resize(800, 600)
    viewer.show()
    sys.exit(app.exec())
