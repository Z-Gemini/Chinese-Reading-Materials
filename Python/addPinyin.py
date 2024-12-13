import sys
import pyttsx3
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QTextEdit, QPushButton, \
    QLabel, QLineEdit, QGraphicsView, QGraphicsScene, QGraphicsTextItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from googletrans import Translator
from pypinyin import pinyin, Style


class PinyinTranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("中文句子处理工具")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

        # 初始化语音引擎
        self.speaker = pyttsx3.init()

    def initUI(self):
        # 主窗口布局
        self.layout = QVBoxLayout()

        # 文本编辑框显示文件内容
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("选择文本文件后显示内容...")
        self.layout.addWidget(self.text_edit)

        # 按钮：选择文件
        self.file_button = QPushButton('选择文本文件', self)
        self.file_button.clicked.connect(self.load_file)
        self.layout.addWidget(self.file_button)

        # 按钮：处理文本
        self.process_button = QPushButton('Process', self)
        self.process_button.clicked.connect(self.process_text)
        self.layout.addWidget(self.process_button)

        # 按钮：为选中文本加拼音
        self.pinyin_button = QPushButton('为选中文本加拼音', self)
        self.pinyin_button.clicked.connect(self.add_pinyin_for_selection)
        self.layout.addWidget(self.pinyin_button)

        # 按钮：朗读文本
        self.speak_button = QPushButton('朗读文本', self)
        self.speak_button.clicked.connect(self.speak_text)
        self.layout.addWidget(self.speak_button)

        # 显示翻译结果
        self.translated_label = QLabel("翻译结果：", self)
        self.layout.addWidget(self.translated_label)

        # 拼音显示区域
        self.graphics_view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)
        self.layout.addWidget(self.graphics_view)

        # 设置主窗口布局
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def load_file(self):
        """加载文件并显示到输入框"""
        file_path, _ = QFileDialog.getOpenFileName(self, '选择文本文件', '', 'Text Files (*.txt)')
        if not file_path:
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        self.text_edit.setText(content)

    def process_text(self):
        """处理文本：翻译和加拼音"""
        content = self.text_edit.toPlainText().strip()
        if not content:
            return

        # 1. 翻译
        translated_text = self.translate_sentence(content)
        self.translated_label.setText(f"翻译结果：{translated_text}")

        # 2. 加拼音
        self.scene.clear()  # 清空之前的拼音内容
        self.render_pinyin(content)

    def render_pinyin(self, sentence):
        """在 GraphicsView 中渲染拼音和文字"""
        # 设置拼音字体
        pinyin_font = QFont("Arial", 12, QFont.Bold)
        # 设置汉字字体
        chinese_font = QFont("Arial", 14, QFont.Normal)

        x, y = 10, 20
        for char in sentence:
            if '\u4e00' <= char <= '\u9fff':  # 如果是汉字
                py = pinyin(char, style=Style.TONE, heteronym=False)
                py_text = py[0][0] if py else ""
                pinyin_item = QGraphicsTextItem(py_text)
                pinyin_item.setFont(pinyin_font)
                pinyin_item.setPos(x, y)  # 拼音位置
                self.scene.addItem(pinyin_item)

                chinese_item = QGraphicsTextItem(char)
                chinese_item.setFont(chinese_font)
                chinese_item.setPos(x, y + 20)  # 汉字位置
                self.scene.addItem(chinese_item)

                x += 50  # 字间距
            else:
                chinese_item = QGraphicsTextItem(char)
                chinese_item.setFont(chinese_font)
                chinese_item.setPos(x, y + 20)  # 非汉字直接显示
                self.scene.addItem(chinese_item)
                x += 20  # 英文或标点的间距

    def add_pinyin_for_selection(self):
        """为选中的文本添加拼音"""
        selected_text = self.text_edit.textCursor().selectedText()
        if not selected_text:
            return

        # 获取拼音
        pinyin_text = self.get_pinyin_for_text(selected_text)
        self.text_edit.insertPlainText(f"  [{pinyin_text}]")  # 将拼音插入到选中文本后

    def get_pinyin_for_text(self, text):
        """为文本获取拼音"""
        py_list = pinyin(text, style=Style.TONE, heteronym=False)
        py_text = ' '.join([p[0] for p in py_list])
        return py_text

    def translate_sentence(self, sentence):
        """翻译整句话为英文"""
        translator = Translator()
        try:
            translated = translator.translate(sentence, src='zh-cn', dest='en')
            return translated.text
        except Exception as e:
            return f"翻译失败: {e}"

    def speak_text(self):
        """朗读输入框中的文本"""
        text = self.text_edit.toPlainText().strip()
        if not text:
            return

        # 设置语音引擎的属性（如语速和音量）
        self.speaker.setProperty('rate', 150)  # 设置语速
        self.speaker.setProperty('volume', 1)  # 设置音量（0.0 to 1.0）

        # 朗读文本
        self.speaker.say(text)
        self.speaker.runAndWait()


def main():
    app = QApplication(sys.argv)
    window = PinyinTranslatorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
