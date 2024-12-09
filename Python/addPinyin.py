import tkinter as tk
from tkinter import messagebox
from pypinyin import pinyin, Style
from googletrans import Translator

# Function to add pinyin and translation to the sentence
def add_pinyin_and_translate():
    # Get the input sentence
    sentence = input_text.get("1.0", "end-1c").strip()
    if not sentence:
        messagebox.showerror("Error", "Please enter a sentence!")
        return
    
    # Generate pinyin for the entire sentence
    pinyin_sentence = " ".join([word[0] for word in pinyin(sentence, style=Style.TONE3)])

    # Initialize the translator
    translator = Translator()
    
    # Split sentence into words or phrases (for simplicity, we'll assume the user will provide them)
    words = sentence.split("，")
    
    # For each word, add pinyin and translation
    result_text.delete("1.0", "end")
    for word in words:
        # Generate pinyin for each word
        word_pinyin = " ".join([w[0] for w in pinyin(word, style=Style.TONE3)])
        
        # Translate the word
        translation = translator.translate(word, src="zh-cn", dest="en").text
        
        # Display the word, pinyin, and translation
        result_text.insert(tk.END, f"{word} [{word_pinyin}] : {translation}\n")

# Set up the UI
root = tk.Tk()
root.title("Chinese Sentence Pinyin and Translation")

# Input text box for the user to enter the sentence
input_label = tk.Label(root, text="Enter a Chinese sentence:")
input_label.pack(pady=5)

input_text = tk.Text(root, height=5, width=50)
input_text.pack(pady=10)

# Button to process the input
process_button = tk.Button(root, text="Process Sentence", command=add_pinyin_and_translate)
process_button.pack(pady=10)

# Output area to display the result
result_label = tk.Label(root, text="Result:")
result_label.pack(pady=5)

result_text = tk.Text(root, height=10, width=50)
result_text.pack(pady=10)

# Run the application
root.mainloop()
