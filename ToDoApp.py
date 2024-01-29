import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QListWidgetItem

class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_db()
        self.setWindowTitle("To-Do List App")
        self.setGeometry(100, 100, 400, 600)

        self.layout = QVBoxLayout()

        self.input_field = QLineEdit()
        self.add_button = QPushButton("Add Task")
        self.toggle_status_button = QPushButton("Toggle Status")
        self.delete_button = QPushButton("Delete Task")
        self.delete_all_button = QPushButton("Delete All Tasks")
        self.task_list = QListWidget()

        self.layout.addWidget(self.input_field)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.toggle_status_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.delete_all_button)
        self.layout.addWidget(self.task_list)

        self.add_button.clicked.connect(self.add_task)
        self.toggle_status_button.clicked.connect(self.toggle_status)
        self.delete_button.clicked.connect(self.delete_task)
        self.delete_all_button.clicked.connect(self.delete_all_tasks)

        self.load_tasks()
        self.setLayout(self.layout)

    def init_db(self):
        self.conn = sqlite3.connect('todo.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS tasks 
                            (id INTEGER PRIMARY KEY, task TEXT, completed BOOLEAN)''')
        self.conn.commit()

    def add_task(self):
        task = self.input_field.text()
        if task:
            self.cur.execute("INSERT INTO tasks (task, completed) VALUES (?, ?)", (task, False))
            self.conn.commit()
            self.input_field.clear()
            self.load_tasks()

    def delete_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            self.cur.execute("DELETE FROM tasks WHERE task = ?", (selected_item.text().split(' - ')[1],))
            self.conn.commit()
            self.load_tasks()

    def delete_all_tasks(self):
        self.cur.execute("DELETE FROM tasks")
        self.conn.commit()
        self.load_tasks()

    def toggle_status(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task = selected_item.text().split(' - ')[1]
            new_status = not ("Completed" in selected_item.text())
            self.cur.execute("UPDATE tasks SET completed = ? WHERE task = ?", (new_status, task))
            self.conn.commit()
            self.load_tasks()

    def load_tasks(self):
        self.task_list.clear()
        self.cur.execute("SELECT task, completed FROM tasks")
        tasks = self.cur.fetchall()
        for task, completed in tasks:
            display_text = "Completed - " + task if completed else "Uncompleted - " + task
            self.task_list.addItem(display_text)

    def closeEvent(self, event):
        self.conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())
