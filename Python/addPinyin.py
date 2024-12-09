from PyQt5 import QtCore, QtGui, QtWidgets
from pypinyin import pinyin, Style
from googletrans import Translator


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Label_input = QtWidgets.QLabel(self.centralwidget)
        self.Label_input.setObjectName("Label_input")
        self.verticalLayout_4.addWidget(self.Label_input)

        # 修改为 QTextEdit 使其可编辑
        self.textEdit_input = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_input.setObjectName("textEdit_input")
        self.verticalLayout_4.addWidget(self.textEdit_input)
        self.verticalLayout_7.addLayout(self.verticalLayout_4)

        self.Button_trans = QtWidgets.QPushButton(self.centralwidget)
        self.Button_trans.setObjectName("Button_trans")
        self.verticalLayout_7.addWidget(self.Button_trans)

        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.Label_pinyin = QtWidgets.QLabel(self.centralwidget)
        self.Label_pinyin.setObjectName("Label_pinyin")
        self.verticalLayout_5.addWidget(self.Label_pinyin)
        self.textBrowser_pinyin = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_pinyin.setObjectName("textBrowser_pinyin")
        self.verticalLayout_5.addWidget(self.textBrowser_pinyin)
        self.verticalLayout_7.addLayout(self.verticalLayout_5)

        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.Label_note = QtWidgets.QLabel(self.centralwidget)
        self.Label_note.setObjectName("Label_note")
        self.verticalLayout_6.addWidget(self.Label_note)
        self.textBrowser_note = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_note.setObjectName("textBrowser_note")
        self.verticalLayout_6.addWidget(self.textBrowser_note)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 连接翻译按钮的点击事件
        self.Button_trans.clicked.connect(self.add_pinyin_and_translate)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Label_input.setText(_translate("MainWindow", "输入中文句子"))
        self.Button_trans.setText(_translate("MainWindow", "翻译"))
        self.Label_pinyin.setText(_translate("MainWindow", "加拼音并翻译"))
        self.Label_note.setText(_translate("MainWindow", "注解"))

    def add_pinyin_and_translate(self):
        sentence = self.textEdit_input.toPlainText().strip()
        if not sentence:
            return

        # 获取带声调的拼音
        pinyin_sentence = " ".join([word[0] for word in pinyin(sentence, style=Style.TONE)])

        # 获取不带声调的拼音
        pinyin_no_tone = " ".join([word[0] for word in pinyin(sentence, style=Style.NORMAL)])

        # 获取拼音与汉字对应
        pinyin_with_hanzi = ""
        for word, pinyin_word in zip(sentence, pinyin(sentence, style=Style.TONE)):
            pinyin_with_hanzi += f"{word}\n{pinyin_word[0]}\n"

        # 获取翻译
        translator = Translator()
        translation = translator.translate(sentence, src="zh-cn", dest="en").text

        # 设置拼音和翻译
        self.textBrowser_pinyin.setText(f"{pinyin_sentence}\n{translation}")
        self.textBrowser_note.setText(f"{pinyin_no_tone} ({pinyin_sentence})\n{pinyin_with_hanzi}")

        # 在汉字上方显示拼音
        self.show_pinyin_above_hanzi(sentence)

    def show_pinyin_above_hanzi(self, sentence):
        """
        用 QPainter 绘制拼音在汉字上方
        """
        # 创建一个 QPainter 来绘制拼音和汉字
        painter = QtGui.QPainter(self.textEdit_input.viewport())
        painter.setFont(QtGui.QFont("Arial", 12))

        pinyin_list = pinyin(sentence, style=Style.TONE)
        x, y = 10, 10  # 起始位置

        for char, pinyin_word in zip(sentence, pinyin_list):
            # 绘制拼音
            painter.drawText(x, y, pinyin_word[0])  # 拼音在汉字上方
            # 绘制汉字
            painter.drawText(x, y + 20, char)  # 汉字在拼音下方
            x += 30  # 每个字符间隔

        painter.end()


# 程序入口，启动 PyQt 应用
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)  # 初始化 QApplication
    MainWindow = QtWidgets.QMainWindow()  # 创建主窗口
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)  # 设置界面
    MainWindow.show()  # 显示窗口
    sys.exit(app.exec_())  # 启动事件循环
