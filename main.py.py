import sys
from PyQt5.QtWidgets import (QApplication,QWidget,QPushButton,QLineEdit,QLabel,QVBoxLayout,QHBoxLayout,QFrame,QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os
if not os.path.exists("my_list.txt"):
    with open("my_list.txt", "w") as file:
        pass

class ToDo(QWidget):
    def __init__(self):
        super().__init__()
        self.title=QLabel(self)
        self.task_input=QLineEdit(self)
        self.add_button=QPushButton("Add Task",self)
        self.title = QLabel("To-Do Items")
        self.List=[]
        with open("my_list.txt","r") as file :
            for line in file:
                self.List.append(line.strip())
        self.initUI()


    def initUI(self):
        self.setWindowTitle("To-Do App")
        self.setGeometry(200, 200, 400, 600)
        vbox=QVBoxLayout()
        self.setLayout(vbox)

        self.setWindowIcon(QIcon("icon_todo.png"))
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
        vbox.addWidget(self.title)

        self.task_input.setPlaceholderText("Task")
        self.task_input.setStyleSheet(
            "padding: 10px;"
            "font-size: 16px;"
            "border: 1px solid #ddd;"
            "border-radius: 8px;"
            
        )

        self.add_button.setStyleSheet("""
    
    border-radius: 5px;
    background-color: #949392;
    border: 1px solid #f5f5f5;
    padding: 10px 15px;
""")
        

        self.task_container = QVBoxLayout()
        
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.task_container)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        vbox.addWidget(scroll_area)
        scroll_area.setStyleSheet("""
            border: 1px solid #eee;
            border-radius: 10px;
            background-color: #f9f9f9;
        """)

        hbox=QHBoxLayout()
        hbox.addWidget(self.task_input)
        hbox.addWidget(self.add_button)
        vbox.addLayout(hbox)

        self.task_input.returnPressed.connect(self.add_button.click)
        self.add_button.clicked.connect(self.add_task_to_ui)

        for task in self.List:
            self.task_input.setText(task)
            self.add_task_to_ui()


    def add_task_to_ui(self):
        task_text = self.task_input.text().strip()
        if not task_text:
            return
        
        task_frame = QFrame()
        task_frame.setMaximumHeight(60)
        self.task_container.setAlignment(Qt.AlignTop)
        task_frame.setStyleSheet("background-color: #f0f0f0; border: 1px solid #f5f5f5; border-radius: 5px;")
        
        hbox = QHBoxLayout()
        hbox.setContentsMargins(10, 5, 10, 5)
        task_frame.setLayout(hbox)

        task_label = QLabel(task_text)
        task_edit=QLineEdit(self)
        task_edit.setStyleSheet("background-color: #f0f0f0; border: 1px solid #f0f0f0; border-radius: 5px;font-size: 16px;")
        task_edit.hide()
        task_label.setStyleSheet("font-size: 16px;")
        hbox.addWidget(task_label)
        hbox.addWidget(task_edit)

        edit_btn = QPushButton("✏️")
        edit_btn.setFixedSize(30, 30)
        edit_btn.setStyleSheet("background-color: lightblue; border: none;")
        hbox.addWidget(edit_btn)

        save_btn = QPushButton("✔️")
        save_btn.setFixedSize(30, 30)
        save_btn.setStyleSheet("background-color: lightgreen; border: none;")
        hbox.addWidget(save_btn)

        save_btn.hide()

        delete_btn = QPushButton("🗑️")
        delete_btn.setFixedSize(30, 30)
        delete_btn.setStyleSheet("background-color: lightcoral; border: none;")
        hbox.addWidget(delete_btn)


        self.task_container.addWidget(task_frame)
        
        if not task_text in self.List:
            self.List.append(task_text)

        self.task_input.setText("")
        print(self.List)

        delete_btn.clicked.connect(lambda _, label=task_label, frame=task_frame: self.del_task(label, frame))
        edit_btn.clicked.connect(lambda _,label=task_label,LineEdit=task_edit,frame=task_frame: self.edit_task(label, frame,LineEdit,save_btn,edit_btn))
        save_btn.clicked.connect(lambda _: self.save_edit(task_label, task_edit, edit_btn, save_btn))

    def edit_task(self,label, frame,LineEdit,save_btn,edit_btn):
        LineEdit.show()
        label.hide()
        save_btn.show()
        edit_btn.hide()
        LineEdit.setText(label.text())

        LineEdit.returnPressed.connect(lambda: self.save_edit(label, LineEdit,save_btn,edit_btn))
        save_btn.clicked.connect(lambda: self.save_edit(label, LineEdit, save_btn, edit_btn))
    
    def save_edit(self,label,LineEdit,save_btn,edit_btn):
        index =self.List.index(label.text())
        label.setText(LineEdit.text())
        self.List[index]=label.text()
        label.show()
        LineEdit.hide()
        save_btn.hide()
        edit_btn.show()
        print(self.List)

    
    def del_task(self, task_label, task_frame):
        print(f"{task_label.text()} is deleted")
        self.List.remove(task_label.text())
        task_frame.setParent(None)

    def closeEvent(self, event):
        
        with open("my_list.txt","w") as file :
            for item in self.List:
                file.write(item+"\n")

        event.accept()


if __name__=="__main__":
    app = QApplication(sys.argv)
    todo =ToDo()
    todo.show()
    sys.exit(app.exec_())

