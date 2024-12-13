from PyQt5.QtWidgets import QGraphicsScene, QFileDialog
from processor import Processor
from PyQt5.QtCore import Qt
from PinYin_UI import *
from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QFont
from pypinyin import pinyin, Style

class My_mainUI(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.sentences = []  # 用于存储文件中的句子
        self.current_sentence_index = 0  # 当前句子索引
        self.processor = Processor()  # 处理模块实例化
        self.scene = QGraphicsScene()  # 创建图形场景

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        # 连接按钮到功能
        self.graphicsView_pinyin.setScene(self.scene)  # 绑定 scene 到 QGraphicsView
        self.pushButton_next.clicked.connect(self.next_sentence)
        self.pushButton_previous.clicked.connect(self.previous_sentence)

        self.pushButton_process1.clicked.connect(self.process_sentence)
        self.actionFile.triggered.connect(self.on_select_file)

        self.pushButton_read1.clicked.connect(self.read_sentence)


    def on_select_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self.centralwidget, "Select a Text File", "./", "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            self.sentences = [line.strip() for line in content.split('\n') if line.strip()]
            self.current_sentence_index = 0
            self.update_sentence_display()
            self.preview_sentence_display()

    def preview_sentence_display(self):
        # Get the current sentence from plainTextEdit_input
        current_sentence = self.plainTextEdit_input.toPlainText().strip()

        # Create a list to store sentences with HTML highlighting
        highlighted_sentences = []

        # Iterate over all sentences and apply highlighting to the current sentence
        for i, sentence in enumerate(self.sentences):
            if sentence == current_sentence:
                # Highlight the current sentence by applying inline CSS style
                highlighted_sentences.append(
                    f'<p style="background-color: yellow; color: black; padding: 2px;">{sentence}</p>')
            else:
                highlighted_sentences.append(f'<p>{sentence}</p>')

        # Combine all sentences into one string with <br> tags between each sentence
        all_sentences = "<br>".join(highlighted_sentences)

        # Set the HTML content for the text browser
        self.textBrowser_preview.setHtml(all_sentences)

    def update_sentence_display(self):
        if self.sentences:
            self.plainTextEdit_input.setPlainText(self.sentences[self.current_sentence_index])  # 显示当前句子

    def next_sentence(self):
        if self.sentences and self.current_sentence_index < len(self.sentences) - 1:
            self.current_sentence_index += 1
            self.update_sentence_display()

    def previous_sentence(self):
        if self.sentences and self.current_sentence_index > 0:
            self.current_sentence_index -= 1
            self.update_sentence_display()

    def process_sentence(self):
        current_sentence = self.plainTextEdit_input.toPlainText()

        # 获取拼音和翻译结果
        pinyin_result = self.processor.process_pinyin(current_sentence)
        translation_result = self.processor.process_translation(current_sentence)

        # 更新拼音显示
        self.scene.clear()
        x, y = 0, 0
        spacing = 45  # 字符间距

        pinyin_font = QFont("Times New Roman", 10, QFont.Normal)
        chinese_font = QFont("楷体", 12, QFont.Normal)
        from PyQt5.QtGui import QTextDocument
        document = QTextDocument()

        for char, py in pinyin_result:
            # 添加拼音
            pinyin_item = QGraphicsTextItem(py)
            pinyin_item.setFont(pinyin_font)
            pinyin_item.setPos(x, y)
            self.scene.addItem(pinyin_item)

            # 添加汉字
            chinese_item = QGraphicsTextItem(char)
            chinese_item.setFont(chinese_font)
            chinese_item.setPos(x, y + 20)
            self.scene.addItem(chinese_item)

            x += spacing

            # 更新翻译显示
            self.textBrowser_translation.setPlainText(translation_result)

    def read_sentence(self):
        current_sentence = self.plainTextEdit_input.toPlainText()
        self.processor.process_read(current_sentence)