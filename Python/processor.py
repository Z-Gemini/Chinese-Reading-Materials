from pypinyin import pinyin, Style
from googletrans import Translator
from gtts import gTTS
import pygame
import os
import tempfile

class Processor:
    def __init__(self):
        self.translator = Translator()
        pygame.mixer.init()


    def process_pinyin(self, text):
        """
        为每个汉字生成拼音并返回。
        :param text: 输入的中文文本
        :return: 包含每个字符及其拼音的列表
        """
        result = []
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # 判断是否是汉字
                py = pinyin(char, style=Style.TONE)  # 获取拼音（带声调）
                py_text = py[0][0] if py else ""
                result.append((char, py_text))
            else:
                result.append((char, ""))  # 非汉字无拼音
        return result

    def process_translation(self, text):
        """翻译整句话为英文"""
        try:
            translated = self.translator.translate(text, src='zh-cn', dest='en')
            return translated.text
        except Exception as e:
            return f"翻译失败: {e}"

    def process_read(self, text):
        """使用 gTTS 引擎朗读文本"""
        try:
            tts = gTTS(text, lang='zh')
            tts.save("output.mp3")
            os.system("start output.mp3")  # Windows 播放音频
        except Exception as e:
            print(f"朗读失败: {e}")