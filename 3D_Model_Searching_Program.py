# -*- coding: UTF-8 -*-

"""

@Project Name: 3D_Model_Searching_Program
@File Name:    3D_Model_Searching_Program

@User:         smile
@Author:       Smile
@Email:        Xiaofei.Smile365@Gmail.com

@Date Time:    2020/12/21 14:00
@IDE:          PyCharm

"""
import glob  # 导入glob函数库
import re  # 导入re函数库，用于字符检索
import time  # 导入time函数库，用于时间显示等
import datetime  # 导入datetime函数库，用于日期的显示等

import os  # 导入os函数库，用于系统路径打开等
import sys  # 基本作用同上

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ["PATH"]  # PyQt打包环境变量存在异常，此程序语句用于修复环境变量

from PyQt5.QtCore import Qt, QTimer, QDateTime  # 导入PyQt5等相关函数，用于GUI的建立与显示
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QAction, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QPushButton, QTableWidget, QAbstractItemView, QGridLayout, QTextEdit, QFileDialog, QMessageBox, QTableWidgetItem, \
    QMdiSubWindow, QMdiArea, QDialog
from PyQt5.QtWidgets import QMainWindow

import shutil  # 导入shutil函数库，用于文件的复制与移动
from shutil import copyfile  # 复制一个文件到另一个文件夹下    copyfile(src,dst)

import pandas as pd  # 导入pandas函数库，用于文件数据的读取与分析

global model_list_name_path_photo_readme  # 声明全局变量


class MainWindow(QMainWindow):  # 建立GUI相关类，继承自QMainWindows
    def __init__(self, parent=None):  # __init__函数，主界面初始化时执行此函数
        super(MainWindow, self).__init__(parent)  # 初始化界面

        self.designer_xiao = "Xiao"  # 定义变量，设计者

        self.status = self.statusBar()  # 定义变量，状态栏

        self.menu = self.menuBar()  # 定义变量，菜单栏

        self.palette = QPalette()  # 定义变量，界面背景

        self.size = self.geometry()  # 定义变量，GUI窗口尺寸大小
        self.screen = QDesktopWidget().screenGeometry()  # 定义变量，获取显示设备屏幕尺寸

        self.fileMenu = self.menu.addMenu("文件")  # 定义变量，菜单栏，文件
        self.import_action = QAction(QIcon("./source/import.png"), "&导入模型", self)  # 定义变量，菜单栏，导入模型，同步设定图标
        self.refresh_action = QAction(QIcon("./source/refresh.png"), "&刷新列表", self)  # 定义变量，菜单栏，刷新列表，同步设定图标
        self.helpMenu = self.menu.addMenu("帮助")  # 定义变量，菜单栏，帮助
        self.readme_action = QAction(QIcon("./source/readme.png"), "&使用说明", self)  # 定义变量，菜单栏，使用说明，同步设定图标
        self.designer_action = QAction(QIcon("./source/designer.png"), "&开发者", self)  # 定义变量，菜单栏，开发者，同步设定图标

        self.main_frame = QWidget()  # 定义变量，中央窗口控件
        self.layout_main_frame = QVBoxLayout()  # 定义变量，中央窗口布局，垂直布局

        self.label_title = QLabel(self)  # 定义变量，标题Label
        self.layout_label_title = QHBoxLayout()  # 定义变量，标题Label的布局，水平布局

        self.label_designer = QLabel(self)  # 定义变量，设计者Label
        self.layout_label_designer = QHBoxLayout()  # 定义变量，设计者Label的布局，水平布局

        self.label_datetime = QLabel(self)  # 定义变量，日期时间Label
        self.layout_label_datetime = QHBoxLayout()  # 定义变量，日期时间Label的布局，水平布局

        self.show_Time_QTimer = QTimer(self)  # 定义变量，定时器，日期时间实时显示

        self.layout_label_designer_datetime = QHBoxLayout()  # 定义变量，设计者和日期时间的布局，水平布局

        self.line_keyword = QLineEdit()  # 定义变量，关键字LineEdit
        self.layout_line_keyword = QHBoxLayout()  #定义变量，关键字LineEdit布局，水平布局

        self.button_search = QPushButton()  # 定义变量，检索按钮PushButton
        self.layout_button_search = QHBoxLayout()  # 定义变量，检索按钮PushButton布局，水平布局

        self.layout_label_keyword_search = QHBoxLayout()  # 定义变量，关键字和检索按钮的布局，水平布局

        self.table_model_list = QTableWidget()  # 定义变量，ModelList表格控件
        self.layout_table_model_list = QHBoxLayout()  # 定义变量，ModelList表格控件布局，水平布局

        self.layout_label_keyword_search_model_list = QVBoxLayout()  # 定义变量，关键字和检索按钮及ModelList的布局，垂直布局

        self.layout_model_photo = QGridLayout()

        self.label_photo_after = QLabel()
        self.layout_label_photo_after = QHBoxLayout()
        self.label_photo_left = QLabel()
        self.layout_label_photo_left = QHBoxLayout()
        self.label_photo_under = QLabel()
        self.layout_label_photo_under = QHBoxLayout()
        self.label_photo_right = QLabel()
        self.layout_label_photo_right = QHBoxLayout()
        self.label_photo_before = QLabel()
        self.layout_label_photo_before = QHBoxLayout()
        self.label_photo_on = QLabel()
        self.layout_label_photo_on = QHBoxLayout()

        self.label_model_name = QLabel(self)
        self.layout_label_model_name = QHBoxLayout()

        self.line_the_model_name = QLineEdit(self)
        self.layout_line_the_model_name = QHBoxLayout()

        self.label_model_path = QLabel(self)
        self.layout_label_model_path = QHBoxLayout()

        self.line_the_model_path = QLineEdit(self)
        self.layout_line_the_model_path = QHBoxLayout()

        self.button_open_path = QPushButton()
        self.layout_button_open_path = QHBoxLayout()

        self.layout_button_model_path_open_path = QHBoxLayout()

        self.label_model_readme = QLabel(self)
        self.layout_label_model_readme = QHBoxLayout()

        self.text_the_model_readme = QTextEdit(self)
        self.layout_text_the_model_readme = QHBoxLayout()

        self.layout_model_description = QVBoxLayout()

        self.layout_model_photo_description = QHBoxLayout()

        self.layout_search_model = QHBoxLayout()

        global model_list_name_path_photo_readme
        model_list_name_path_photo_readme = []

        self.initUI()

    def initUI(self):
        self.setFocus()
        self.status.showMessage("三维数模检索程序启动中", 3000)

        self.setFixedSize(960, 540)
        self.setWindowIcon(QIcon("./source/search.png"))
        self.setWindowTitle("三维数模检索程序")

        self.palette.setBrush(QPalette.Background, QBrush(QPixmap("./source/background.jpg").scaled(self.width(), self.height())))
        self.setPalette(self.palette)
        self.setAutoFillBackground(True)

        # self.move((self.screen.width() - self.size.width())/2, (self.screen.height() - self.size.height())/2)

        self.import_action.triggered.connect(self.import_Model)
        self.fileMenu.addAction(self.import_action)
        self.refresh_action.triggered.connect(self.refresh_List)
        self.fileMenu.addAction(self.refresh_action)

        self.readme_action.triggered.connect(self.readme)
        self.helpMenu.addAction(self.readme_action)
        self.designer_action.triggered.connect(self.designer)
        self.helpMenu.addAction(self.designer_action)

        self.setCentralWidget(self.main_frame)
        self.main_frame.setLayout(self.layout_main_frame)

        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.setText("三维数模检索程序")
        self.label_title.setFont(QFont("微软雅黑", 20))
        self.label_title.setFixedSize(250, 30)
        self.layout_label_title.addWidget(self.label_title)

        self.layout_main_frame.addLayout(self.layout_label_title)
        # self.layout_main_frame.addStretch(1)

        self.label_designer.setAlignment(Qt.AlignCenter)
        self.label_designer.setText("Designer: Xiao")
        self.label_designer.setFont(QFont("微软雅黑", 10))
        self.label_designer.setFixedSize(90, 20)
        self.layout_label_designer.addWidget(self.label_designer)

        self.label_datetime.setAlignment(Qt.AlignCenter)
        self.label_datetime.setText("DateTime: 1997/01/01 00:00:00")
        self.label_datetime.setFont(QFont("微软雅黑", 10))
        self.label_datetime.setFixedSize(200, 20)
        self.layout_label_datetime.addWidget(self.label_datetime)

        self.show_Time_QTimer.timeout.connect(self.show_Time)
        self.show_Time_QTimer.start(500)

        self.layout_label_designer_datetime.addLayout(self.layout_label_designer)
        self.layout_label_designer_datetime.addStretch(1)
        self.layout_label_designer_datetime.addLayout(self.layout_label_datetime)

        self.layout_main_frame.addLayout(self.layout_label_designer_datetime)
        self.layout_main_frame.addStretch(1)

        self.line_keyword.setAlignment(Qt.AlignLeft)
        self.line_keyword.setPlaceholderText("请输入关键字...")
        self.line_keyword.editingFinished.connect(self.search_model)
        self.line_keyword.setFont(QFont("微软雅黑", 12))
        self.line_keyword.setFixedSize(165, 25)
        self.layout_line_keyword.addWidget(self.line_keyword)

        self.button_search.setIcon(QIcon("source/search_model.png"))
        self.button_search.setText("搜索")
        self.button_search.setToolTip("搜索范围：模型名称、视图、详细描述及其对应路径")
        self.button_search.clicked.connect(self.search_model)
        self.button_search.setFont(QFont("微软雅黑", 12))
        self.button_search.setFixedSize(80, 28)
        self.layout_button_search.addWidget(self.button_search)

        # self.layout_label_keyword_search.addStretch(1)
        self.layout_label_keyword_search.addLayout(self.layout_line_keyword)
        self.layout_label_keyword_search.addLayout(self.layout_button_search)
        # self.layout_label_keyword_search.addStretch(1)

        self.table_model_list.setRowCount(99)
        self.table_model_list.setColumnCount(2)
        self.table_model_list.setFixedSize(250, 380)
        self.table_model_list.setToolTip("此处为模型列表...")
        self.table_model_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_model_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_model_list.setHorizontalHeaderLabels(["文件名", '路径'])
        self.table_model_list.itemClicked.connect(self.show_message_model_name)
        self.table_model_list.itemDoubleClicked.connect(self.open_model_path)
        self.layout_table_model_list.addWidget(self.table_model_list)

        self.layout_label_keyword_search_model_list.addLayout(self.layout_label_keyword_search)
        self.layout_label_keyword_search_model_list.addLayout(self.layout_table_model_list)

        self.label_photo_after.setAlignment(Qt.AlignCenter)
        self.label_photo_after.setToolTip("后视图")
        self.label_photo_after.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
        self.label_photo_after.setFixedSize(100, 100)
        self.layout_label_photo_after.addWidget(self.label_photo_after)

        self.label_photo_left.setAlignment(Qt.AlignCenter)
        self.label_photo_left.setToolTip("左视图")
        self.label_photo_left.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
        self.label_photo_left.setFixedSize(100, 100)
        self.layout_label_photo_left.addWidget(self.label_photo_left)

        self.label_photo_under.setAlignment(Qt.AlignCenter)
        self.label_photo_under.setToolTip("仰视图")
        self.label_photo_under.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
        self.label_photo_under.setFixedSize(100, 100)
        self.layout_label_photo_under.addWidget(self.label_photo_under)

        self.label_photo_right.setAlignment(Qt.AlignCenter)
        self.label_photo_right.setToolTip("右视图")
        self.label_photo_right.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
        self.label_photo_right.setFixedSize(100, 100)
        self.layout_label_photo_right.addWidget(self.label_photo_right)

        self.label_photo_before.setAlignment(Qt.AlignCenter)
        self.label_photo_before.setToolTip("前视图")
        self.label_photo_before.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
        self.label_photo_before.setFixedSize(100, 100)
        self.layout_label_photo_before.addWidget(self.label_photo_before)

        self.label_photo_on.setAlignment(Qt.AlignCenter)
        self.label_photo_on.setToolTip("俯视图")
        self.label_photo_on.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
        self.label_photo_on.setFixedSize(100, 100)
        self.layout_label_photo_on.addWidget(self.label_photo_on)

        self.layout_model_photo.addLayout(self.layout_label_photo_after, 0, 1)
        self.layout_model_photo.addLayout(self.layout_label_photo_left, 1, 0)
        self.layout_model_photo.addLayout(self.layout_label_photo_under, 1, 1)
        self.layout_model_photo.addLayout(self.layout_label_photo_right, 1, 2)
        self.layout_model_photo.addLayout(self.layout_label_photo_before, 2, 1)
        self.layout_model_photo.addLayout(self.layout_label_photo_on, 3, 1)

        self.label_model_name.setAlignment(Qt.AlignLeft)
        self.label_model_name.setText("1. 模型名称")
        self.label_model_name.setFont(QFont("微软雅黑", 12))
        self.label_model_name.setFixedSize(300, 20)
        self.layout_label_model_name.addWidget(self.label_model_name)

        self.line_the_model_name.setAlignment(Qt.AlignLeft)
        self.line_the_model_name.setPlaceholderText("此处为该模型名称...")
        # self.line_the_model_name.setReadOnly(True)
        self.line_the_model_name.setFont(QFont("微软雅黑", 10))
        self.line_the_model_name.setFixedSize(260, 20)
        self.layout_line_the_model_name.addWidget(self.line_the_model_name)

        self.label_model_path.setAlignment(Qt.AlignLeft)
        self.label_model_path.setText("2. 模型路径")
        self.label_model_path.setFont(QFont("微软雅黑", 12))
        self.label_model_path.setFixedSize(300, 20)
        self.layout_label_model_path.addWidget(self.label_model_path)

        self.line_the_model_path.setAlignment(Qt.AlignLeft)
        self.line_the_model_path.setPlaceholderText("此处为该模型路径...")
        self.line_the_model_path.setFont(QFont("微软雅黑", 10))
        self.line_the_model_path.setFixedSize(180, 20)
        self.layout_line_the_model_path.addWidget(self.line_the_model_path)

        self.button_open_path.setIcon(QIcon("./source/open_path.png"))
        self.button_open_path.setText("打开")
        self.button_open_path.setFont(QFont("微软雅黑", 8))
        self.button_open_path.setFixedSize(56, 23)
        self.button_open_path.clicked.connect(self.open_model_path_button)
        self.layout_button_open_path.addWidget(self.button_open_path)

        # self.layout_button_model_path_open_path.addStretch(1)
        self.layout_button_model_path_open_path.addLayout(self.layout_line_the_model_path)
        self.layout_button_model_path_open_path.addLayout(self.layout_button_open_path)
        # self.layout_button_model_path_open_path.addStretch(1)

        self.label_model_readme.setAlignment(Qt.AlignLeft)
        self.label_model_readme.setText("3. 模型描述")
        self.label_model_readme.setFont(QFont("微软雅黑", 12))
        self.label_model_readme.setFixedSize(300, 20)
        self.layout_label_model_readme.addWidget(self.label_model_readme)

        self.text_the_model_readme.setAlignment(Qt.AlignLeft)
        self.text_the_model_readme.setPlaceholderText("此处为该模型的详细描述...")
        self.text_the_model_readme.setFont(QFont("微软雅黑", 10))
        self.text_the_model_readme.setFixedSize(260, 284)
        self.layout_text_the_model_readme.addWidget(self.text_the_model_readme)

        self.layout_model_description.addLayout(self.layout_label_model_name)
        self.layout_model_description.addLayout(self.layout_line_the_model_name)
        # self.layout_model_description.addStretch(1)
        self.layout_model_description.addLayout(self.layout_label_model_path)
        self.layout_model_description.addLayout(self.layout_button_model_path_open_path)
        # self.layout_model_description.addStretch(1)
        self.layout_model_description.addLayout(self.layout_label_model_readme)
        self.layout_model_description.addLayout(self.layout_text_the_model_readme)

        self.layout_model_photo_description.addLayout(self.layout_model_photo)
        self.layout_model_photo_description.addLayout(self.layout_model_description)

        self.layout_search_model.addLayout(self.layout_label_keyword_search_model_list)
        self.layout_search_model.addLayout(self.layout_model_photo_description)

        self.layout_main_frame.addLayout(self.layout_search_model)

    def show_Time(self):
        now_time = QDateTime.currentDateTime()
        self.label_datetime.setText("DateTime: " + now_time.toString("yyyy/MM/dd hh:mm:ss"))

    def import_Model(self):
        file_path = QFileDialog.getExistingDirectory(self, "选择模型所在文件夹", ".")

        # 递归函数
        def copy_file(path_read, path_write):
            # 输出path_read目录下的所有文件包括文件夹的名称
            names = os.listdir(path_read)
            # 循环遍历所有的文件或文件夹
            for name in names:
                # 定义新的读入路径（就是在原来目录下拼接上文件名）
                path_read_new = path_read + "\\" + name
                # 定义新的写入路径（就是在原来目录下拼接上文件名）
                path_write_new = path_write + "\\" + name
                # 判断该读入路径是否是文件夹，如果是文件夹则执行递归，如果是文件则执行复制操作
                if os.path.isdir(path_read_new):
                    # 判断写入路径中是否存在该文件夹，如果不存在就创建该文件夹
                    if not os.path.exists(path_write_new):
                        # 创建要写入的文件夹
                        os.mkdir(path_write_new)
                    # 执行递归函数，将文件夹中的文件复制到新创建的文件夹中（保留原始目录结构）
                    copy_file(path_read_new, path_write_new)
                else:
                    # 将文件path_read_new复制到path_write_new
                    copyfile(path_read_new, path_write_new)

        if int(len(file_path)) > 0:
            self.status.showMessage("模型导入中...")
            # shutil.move(file_path, "./model/")
            # 执行递归函数
            if os.path.exists("./model/" + file_path.split("/")[-1]):
                result = QMessageBox.warning(self, "警告", "目标已包含一个名为“%s”的文件夹，是否进行替换？" % file_path.split("/")[-1], QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if result == QMessageBox.Yes:
                    shutil.rmtree("./model/" + file_path.split("/")[-1])
                    os.mkdir("./model/" + file_path.split("/")[-1])
                    copy_file(file_path, "./model/" + file_path.split("/")[-1] + "/")
                    self.status.showMessage("模型导入成功", 1000)
                    QMessageBox.about(self, "导入成功", "模型导入成功，请点击刷新列表进行模型数据库更新！")
                else:
                    self.status.showMessage("取消模型导入", 1000)
            else:
                os.mkdir("./model/" + file_path.split("/")[-1])
                copy_file(file_path, "./model/" + file_path.split("/")[-1] + "/")
                self.status.showMessage("模型导入成功", 1000)
                QMessageBox.about(self, "导入成功", "模型导入成功，请点击刷新列表进行模型数据库更新！")
        else:
            self.status.showMessage("取消模型导入", 1000)

    def refresh_List(self):
        def file_create(file_path):
            file = open(file_path, 'w')
            new_file_columns = ['Model Name', 'Model Path', 'Readme Name', 'Readme Path', '1. Photo Before Name', '1. Photo Before Path', '2. Photo After Name', '2. Photo After Path', '3. Photo Left Name', '3. Photo Left Path', '4. Photo Right Name', '4. Photo Right Path', '5. Photo On Name', '5. Photo On Path', '6. Photo Under Name', '6. Photo Under Path']
            data = pd.DataFrame(columns=new_file_columns)
            data.to_csv(file_path)
            file.close()

        file_create("./temp/model_list.csv")  # 新建csv文件用于存储model信息

        def model_list_create(model_path):
            model_list = []
            for parent, dirnames, filenames in os.walk(model_path, followlinks=True):
                for filename in filenames:
                    model_name_list = []
                    if filename.split(".")[-1] == "stp" or filename.split(".")[-1] == "prt" or filename.split(".")[-1] == "1" or filename.split(".")[-1] == "drw" or filename.split(".")[-1] == "2" or filename.split(".")[-1] == "asm" or filename.split(".")[-1] == "3":
                        file_path = os.path.join(os.path.abspath(parent), filename)
                        # print("文件名：%s" % filename, "文件路径：%s" % file_path)
                        model_name_list.append(filename)
                        model_name_list.append(os.path.abspath(parent))

                        readme_list = []
                        for path_the_model, dir_list_the_model, file_list_the_model in os.walk(os.path.abspath(parent), followlinks=True):
                            for readmename_the_model in file_list_the_model:
                                if readmename_the_model.split(".")[-1] == "txt" or readmename_the_model.split(".")[-1] == "TXT":
                                    file_path_the_model = os.path.join(os.path.abspath(path_the_model), readmename_the_model)
                                    # print("文件名：%s" % readmename_the_model, "文件路径：%s" % file_path_the_model)
                                    model_name_list.append(readmename_the_model)
                                    model_name_list.append(os.path.abspath(path_the_model))

                        photo_model_list = []
                        for path_the_model, dir_list_the_model, file_list_the_model in os.walk(os.path.abspath(parent), followlinks=True):
                            for filename_the_model in file_list_the_model:
                                if filename_the_model.split(".")[-1] == "png" or filename_the_model.split(".")[-1] == "PNG" or filename_the_model.split(".")[-1] == "JPG" or filename_the_model.split(".")[-1] == "jpg":
                                    file_path_the_model = os.path.join(os.path.abspath(path_the_model), filename_the_model)
                                    # print("文件名：%s" % filename_the_model, "文件路径：%s" % file_path_the_model)
                                    model_name_list.append(filename_the_model)
                                    model_name_list.append(os.path.abspath(path_the_model))

                        model_list.append(model_name_list)

            return model_list

        model_list_for_csv = model_list_create("./model/")  # 获取model文件夹下的model信息
        # print(model_list_for_csv)
        global model_list_name_path_photo_readme
        model_list_name_path_photo_readme = model_list_for_csv

        def write_to_csv(model_list):
            data_list = model_list
            data_model_list = pd.DataFrame(data=data_list)
            data_model_list.to_csv("./temp/model_list.csv", mode='a', header=False)  # 写入到csv文件

        write_to_csv(model_list_for_csv)  # 将model_list写入到csv文件

        def show_table():
            self.table_model_list.setRowCount(len(model_list_for_csv))

            for row in range(0, len(model_list_for_csv)):
                for column in range(0, 2):
                    self.table_model_list.setItem(row, column, QTableWidgetItem(str(model_list_for_csv[row][column])))
                    pass

        show_table()

        def model_description_clear():
            self.label_photo_after.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_left.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_under.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_right.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_before.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_on.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.line_the_model_name.clear()
            self.line_the_model_path.clear()
            self.text_the_model_readme.clear()
            self.table_model_list.setCurrentItem(None)
            self.table_model_list.setToolTip("此处为模型列表...")
            self.line_keyword.clear()

        model_description_clear()
        # print(self, datetime.datetime.now())

    def show_message_model_name(self, item):
        def model_description_clear():
            self.label_photo_after.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_left.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_under.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_right.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_before.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_on.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.line_the_model_name.clear()
            self.line_the_model_path.clear()
            self.text_the_model_readme.clear()
            # self.table_model_list.setCurrentItem(None)
            self.table_model_list.setToolTip("此处为模型列表...")
            # self.line_keyword.clear()

        model_description_clear()

        global model_list_name_path_photo_readme
        # print(item.text(), item.row(), item.column())
        self.table_model_list.setToolTip(item.text())
        self.line_the_model_name.setText(str(model_list_name_path_photo_readme[item.row()][0]))
        self.line_the_model_path.setText(str(model_list_name_path_photo_readme[item.row()][1]))

        try:  # readme和photo存在缺失时，造成model_list位置混乱，无法正确打开文档或照片
            if len(model_list_name_path_photo_readme[item.row()]) >= 3:
                readme_the_model_path = str(model_list_name_path_photo_readme[item.row()][3]) + "\\" + str(model_list_name_path_photo_readme[item.row()][2])
                # print(readme_the_model_path)
                with open(r"%s" % readme_the_model_path, "r", encoding='utf-8') as readme_file:
                    readme_data = readme_file.read()
                    # print(readme_data)
                    self.text_the_model_readme.setText(readme_data)
            else:
                self.status.showMessage("Readme文档不存在，请确认！", 1000)
                self.text_the_model_readme.setText("Readme文档不存在，请确认！")

            if len(model_list_name_path_photo_readme[item.row()]) >= 5:
                after_photo_the_model_path = str(model_list_name_path_photo_readme[item.row()][5]) + "\\" + str(model_list_name_path_photo_readme[item.row()][4])
                self.label_photo_after.setPixmap(QPixmap(after_photo_the_model_path).scaled(100, 100))
            else:
                self.status.showMessage("后视图不存在，请确认！", 1000)
                self.label_photo_after.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))

            if len(model_list_name_path_photo_readme[item.row()]) >= 7:
                before_photo_the_model_path = str(model_list_name_path_photo_readme[item.row()][7]) + "\\" + str(model_list_name_path_photo_readme[item.row()][6])
                self.label_photo_before.setPixmap(QPixmap(before_photo_the_model_path).scaled(100, 100))
            else:
                self.status.showMessage("前视图不存在，请确认！", 1000)
                self.label_photo_before.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))

            if len(model_list_name_path_photo_readme[item.row()]) >= 9:
                left_photo_the_model_path = str(model_list_name_path_photo_readme[item.row()][9]) + "\\" + str(model_list_name_path_photo_readme[item.row()][8])
                self.label_photo_left.setPixmap(QPixmap(left_photo_the_model_path).scaled(100, 100))
            else:
                self.status.showMessage("左视图不存在，请确认！", 1000)
                self.label_photo_left.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))

            if len(model_list_name_path_photo_readme[item.row()]) >= 11:
                on_photo_the_model_path = str(model_list_name_path_photo_readme[item.row()][11]) + "\\" + str(model_list_name_path_photo_readme[item.row()][10])
                self.label_photo_on.setPixmap(QPixmap(on_photo_the_model_path).scaled(100, 100))
            else:
                self.status.showMessage("俯视图不存在，请确认！", 1000)
                self.label_photo_on.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))

            if len(model_list_name_path_photo_readme[item.row()]) >= 13:
                right_photo_the_model_path = str(model_list_name_path_photo_readme[item.row()][13]) + "\\" + str(model_list_name_path_photo_readme[item.row()][12])
                self.label_photo_right.setPixmap(QPixmap(right_photo_the_model_path).scaled(100, 100))
            else:
                self.status.showMessage("右视图不存在，请确认！", 1000)
                self.label_photo_right.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))

            if len(model_list_name_path_photo_readme[item.row()]) >= 15:
                under_photo_the_model_path = str(model_list_name_path_photo_readme[item.row()][15]) + "\\" + str(model_list_name_path_photo_readme[item.row()][14])
                self.label_photo_under.setPixmap(QPixmap(under_photo_the_model_path).scaled(100, 100))
            else:
                self.status.showMessage("仰视图不存在，请确认！", 1000)
                self.label_photo_under.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
        except Exception as e:
            self.status.showMessage("出现错误： %s" % e, 1000)

    def open_model_path(self, item):
        # print(self, item.text(), item.row(), item.column())
        if item.column() == 1 and len(item.text()) > 0:
            try:
                os.startfile(item.text())
                self.status.showMessage("模型路径已打开", 1000)
            except Exception as e:
                self.status.showMessage("出现错误： %s" % e, 1000)

    def open_model_path_button(self):
        if len(self.line_the_model_path.text()) > 0:
            try:
                os.startfile(self.line_the_model_path.text())
                self.status.showMessage("模型路径已打开", 1000)
            except Exception as e:
                self.status.showMessage("出现错误： %s" % e, 1000)

    def search_model(self):
        def model_description_clear():
            self.label_photo_after.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_left.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_under.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_right.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_before.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.label_photo_on.setPixmap(QPixmap("./source/cube.png").scaled(100, 100))
            self.line_the_model_name.clear()
            self.line_the_model_path.clear()
            self.text_the_model_readme.clear()
            self.table_model_list.setCurrentItem(None)
            self.table_model_list.setToolTip("此处为模型列表...")
            # self.line_keyword.clear()

        model_description_clear()

        key_word = self.line_keyword.text()
        if len(str(key_word)) > 0:

            def model_list_create(model_path):  # 获取model的信息，用于检索，包含readme内容
                model_list_has_readme = []
                for parent, dirnames, filenames in os.walk(model_path, followlinks=True):
                    for filename in filenames:
                        model_name_list = []
                        if filename.split(".")[-1] == "stp" or filename.split(".")[-1] == "prt" or filename.split(".")[
                            -1] == "1" or filename.split(".")[-1] == "drw" or filename.split(".")[-1] == "2" or \
                                filename.split(".")[-1] == "asm" or filename.split(".")[-1] == "3":
                            file_path = os.path.join(os.path.abspath(parent), filename)
                            # print("文件名：%s" % filename, "文件路径：%s" % file_path)
                            model_name_list.append(filename)
                            model_name_list.append(os.path.abspath(parent))

                            readme_list = []
                            for path_the_model, dir_list_the_model, file_list_the_model in os.walk(
                                    os.path.abspath(parent), followlinks=True):
                                for readmename_the_model in file_list_the_model:
                                    if readmename_the_model.split(".")[-1] == "txt" or readmename_the_model.split(".")[-1] == "TXT":
                                        file_path_the_model = os.path.join(os.path.abspath(path_the_model), readmename_the_model)
                                        # print("文件名：%s" % readmename_the_model, "文件路径：%s" % file_path_the_model)
                                        model_name_list.append(readmename_the_model)
                                        model_name_list.append(os.path.abspath(path_the_model))

                                        readme_the_model_path = str(os.path.abspath(path_the_model)) + "\\" + str(readmename_the_model)
                                        # print(readme_the_model_path)
                                        with open(r"%s" % readme_the_model_path, "r", encoding='utf-8') as readme_file:
                                            readme_data = readme_file.read()
                                            # model_name_list.append(readme_data)

                            photo_model_list = []
                            for path_the_model, dir_list_the_model, file_list_the_model in os.walk(
                                    os.path.abspath(parent), followlinks=True):
                                for filename_the_model in file_list_the_model:
                                    if filename_the_model.split(".")[-1] == "png" or filename_the_model.split(".")[
                                        -1] == "PNG" or filename_the_model.split(".")[-1] == "JPG" or \
                                            filename_the_model.split(".")[-1] == "jpg":
                                        file_path_the_model = os.path.join(os.path.abspath(path_the_model),
                                                                           filename_the_model)
                                        # print("文件名：%s" % filename_the_model, "文件路径：%s" % file_path_the_model)
                                        model_name_list.append(filename_the_model)
                                        model_name_list.append(os.path.abspath(path_the_model))

                            model_name_list.append(readme_data)

                            model_list_has_readme.append(model_name_list)

                return model_list_has_readme

            model_list_for_search = model_list_create("./model/")  # 获取model文件夹下的model信息
            model_list_result_for_search = []
            # print(self, datetime.datetime.now(), key_word)
            # print(self, datetime.datetime.now(), len(model_list_for_search))
            for i in range(0, len(model_list_for_search)):
                # print(self, datetime.datetime.now(), model_list_for_search[i])
                result = re.findall(str(key_word), str(model_list_for_search[i]))
                if len(result) > 0:
                    # print(self, datetime.datetime.now(), result, i)
                    # model_list_result_for_search.append(model_list_for_search[i])
                    model_list_search_the_model = []
                    for j in range(0, len(model_list_for_search[i])):
                        # if j !=
                        model_list_search_the_model.append(model_list_for_search[i][j])
                    model_list_result_for_search.append(model_list_search_the_model)
            # print(model_list_result_for_search)

            def show_table():
                self.table_model_list.setRowCount(len(model_list_result_for_search))

                for row in range(0, len(model_list_result_for_search)):
                    for column in range(0, 2):
                        self.table_model_list.setItem(row, column,QTableWidgetItem(str(model_list_result_for_search[row][column])))
                        pass

            show_table()

            global model_list_name_path_photo_readme
            model_list_name_path_photo_readme = model_list_result_for_search

    def readme(self):
        readme_dialog = QDialog()
        readme_dialog.setFocus()

        readme_text = QTextEdit(readme_dialog)

        try:
            with open("./source/readme.txt", "r", encoding='utf-8') as readme_file:
                readme_data = readme_file.read()
        except Exception as e:
            self.status.showMessage("出现错误： %s" % e, 1000)
            readme_data = "		三维数模检索程序使用说明\n\
1. 模型导入功能\n\
    1.1 点击 文件-导入模型，打开模型所在文件夹\n\
          PS：每个模型所在文件夹应包含以下8个文件\n\
                 a：模型文件（仅支持prt、stp、drw、asm格式）\n\
                 b：描述文档，命名-readme.txt（仅支持txt格式）\n\
                 c：前视图，命名-before.png（仅支持png、jpg格式）\n\
                 d：后视图，命名-after.png（仅支持png、jpg格式）\n\
                 e：左视图，命名-left.png（仅支持png、jpg格式）\n\
                 f：右视图，命名-right.png（仅支持png、jpg格式）\n\
                 g：俯视图，命名-on.png（仅支持png、jpg格式）\n\
                 h：仰视图，命名-under.png（仅支持png、jpg格式）\n\
    1.2 点击 文件-刷新列表，进行模型数据库列表刷新\n\
\n\
2. 模型预览功能\n\
    2.1 点击列表内的模型，显示该模型名称、路径、描述及视图信息\n\
          PS：模型无描述文档或视图照片时，会造成信息显示不全\n\
\n\
3. 模型检索功能\n\
    3.1 在输入框输入关键字后，点击搜索\n\
          PS：搜索范围为模型名称、视图、描述文档及其对应路径\n\
    3.2 模型列表刷新后，可点击模型进行预览操作\n\
\n\
其他未尽事项，请联系开发者！！！"

        readme_text.setText(readme_data)
        readme_text.setAlignment(Qt.AlignLeft)
        readme_text.setFont(QFont("微软雅黑", 10))
        readme_text.setFixedSize(480, 270)
        readme_text.move(0, 0)

        readme_dialog.setWindowTitle("使用说明")
        readme_dialog.setFixedSize(480, 270)
        readme_dialog.setWindowIcon(QIcon("./source/readme.png"))
        readme_dialog.setWindowModality(Qt.ApplicationModal)
        readme_dialog.exec_()

        # print(self, datetime.datetime.now())

    def designer(self):
        designer_dialog = QDialog()
        designer_dialog.setFocus()

        designer_label = QLabel(designer_dialog)

        designer_label.setText(self.designer_xiao)
        designer_label.setAlignment(Qt.AlignCenter)
        designer_label.setFont(QFont("微软雅黑", 12))
        designer_label.setFixedSize(60, 35)
        designer_label.move(int((240 - 60)/2), int((67 - 35)/2))
        # designer_label.move(0, 0)

        designer_dialog.setWindowTitle("开发者")
        designer_dialog.setFixedSize(240, 67)
        designer_dialog.setWindowIcon(QIcon("./source/designer.png"))
        designer_dialog.setWindowModality(Qt.ApplicationModal)
        designer_dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())

    pass
