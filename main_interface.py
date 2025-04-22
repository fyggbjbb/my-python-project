import tkinter as tk
from ui_components.user_management import UserManagementModule
from ui_components.data_input import DataInputModule
from ui_components.data_processing import DataProcessingModule
from ui_components.visualization import VisualizationModule
from ui_components.data_crud import DataCRUDModule
from ui_components.prediction import PredictionPage
from utils.data_handler import DataHandler


class Controller:
    def __init__(self, main_interface):
        self.main_interface = main_interface
        self.file_path = None
        self.uploaded_data = None
        self.data_crud_module=None

    def set_file_path(self, file_path):
        self.file_path = file_path

    def handle_data_processing(self):
        if not self.file_path:
            tk.messagebox.showerror("错误", "未上传文件，请先上传文件")
            return
        data_processing_module = DataProcessingModule(self.main_interface, self.data_crud_module)
        data_processing_module.process_data(self.file_path)


class MainInterface(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg="#d9d9d9")

        self.controller = Controller(self)

        self.sidebar = tk.Frame(self, bg="#333", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.module_buttons = {
            "user_management": tk.Button(
                self.sidebar, text="用户管理", fg="white", bg="#333",
                command=lambda: self.show_module(UserManagementModule)
            ),
            "data_input": tk.Button(
                self.sidebar, text="数据输入", fg="white", bg="#333",
                command=lambda: self.show_module(DataInputModule)
            ),
            "data_processing": tk.Button(
                self.sidebar, text="数据处理", fg="white", bg="#333",
                command=lambda: self.show_module(DataProcessingModule)
            ),
            "data_crud": tk.Button(
                self.sidebar, text="数据分析", fg="white", bg="#333",
                command=lambda: self.show_module(DataCRUDModule)
            ),
            "visualization": tk.Button(
                self.sidebar, text="可视化", fg="white", bg="#333",
                command=lambda: self.show_module(VisualizationModule)
            ),
            "prediction": tk.Button(
                self.sidebar, text="数据预测", fg="white", bg="#333",
                command=lambda: self.show_module(PredictionPage)
            )
        }

        for btn in self.module_buttons.values():
            btn.pack(pady=10)

        self.content_area = tk.Frame(self)
        self.content_area.pack(fill=tk.BOTH, expand=True)

        self.show_module(DataCRUDModule)

    def show_module(self, module_class):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        if module_class==DataCRUDModule:
            module = module_class(self.content_area, self.controller)
            self.controller.data_crud_module=module
        else:
            module=module_class(self.content_area,self.controller)
        module.pack(fill=tk.BOTH, expand=True)