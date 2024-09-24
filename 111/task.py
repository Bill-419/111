import sys

from PySide6.QtGui import QDesktopServices, QShortcut, Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QApplication, QSplitter
from rn_summary_windows import RN_summary_Window

class ExtendedRN_summary_Window(RN_summary_Window):
    def __init__(self):
        super().__init__()

        # 创建一个右侧部分的容器QWidget
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)

        # 创建两个新的按钮
        self.button1 = QPushButton("复制信息", self)
        self.button1.clicked.connect(self.button1_clicked)
        self.button2 = QPushButton("打开URL", self)
        self.button2.clicked.connect(self.button2_clicked)

        # 创建一个水平布局并添加按钮
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)

        # 创建一个容器widget来放置按钮布局
        button_container = QWidget()
        button_container.setLayout(button_layout)

        # 将按钮容器和HtmlTabWidget添加到右侧容器布局
        right_layout.addWidget(button_container)
        right_layout.addWidget(self.html_tab_widget)

        # 获取父类中的splitter_horizontal属性，并插入新的right_container
        self.splitter_horizontal.insertWidget(1, right_container)  # 插入到splitter_horizontal的指定位置

        # 更新初始宽度比例
        self.splitter_horizontal.setSizes([200, 400])
        # 创建并设置快捷键 Ctrl+C
        self.shortcut_copy = QShortcut(Qt.ControlModifier | Qt.Key_C, self)
        self.shortcut_copy.activated.connect(self.button1_clicked)

    def get_record_by_tab_title(self):
        # 获取当前选中的tab标题并在表格中搜索记录
        current_index = self.html_tab_widget.currentIndex()
        current_tab_title = self.html_tab_widget.tabText(current_index)
        print(f"当前选中的Tab标题: {current_tab_title}")

        # 使用问题单号作为标题在表格中搜索记录
        record = self.table.find_record_by_title(current_tab_title)
        return record

    def get_selected_record_info(self, record, keys):
        # 提取指定键的值
        selected_info = {key: record.get(key, '') for key in keys}
        return selected_info

    def button1_clicked(self):
        # 按钮1点击的逻辑
        record = self.get_record_by_tab_title()
        if record:
            # 如果找到了记录，提取指定的键值对
            keys = ['问题单号', '问题描述', '涉及网元', '解决方案'] # 指定key
            selected_info = self.get_selected_record_info(record, keys)

            # 将提取的信息格式化为字符串
            info_str = '\n'.join(f"{key}: {value}" for key, value in selected_info.items())

            # 复制到剪贴板
            clipboard = QApplication.clipboard()
            clipboard.setText(info_str)

            print(f"已复制到剪贴板:\n{info_str}")
        else:
            print("没有找到匹配的记录")

    def open_url_if_valid(self, url):
        # 检查给定的字符串是否是有效的URL
        if url:
            QDesktopServices.openUrl(url)
        else:
            print("没有提供URL")

    def button2_clicked(self):
        # 按钮2点击的逻辑
        record = self.get_record_by_tab_title()
        if record:
            # 假设我们要查找的键是 '涉及网元'
            key = '涉及网元'
            url = record.get(key, '')
            if url:
                self.open_url_if_valid(url)
            else:
                print(f"没有找到键 '{key}' 或者它的值不是URL")
        else:
            print("没有找到匹配的记录")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExtendedRN_summary_Window()
    window.show()
    sys.exit(app.exec())
