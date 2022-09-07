from cgitb import text
from re import I
import tkinter as tk
import tkinter.ttk as ttk
import sys,os
import random
import csv
from typing_extensions import Self
import requests
import webbrowser

#125行目をcsvの絶対参照アドレスに変える、区切りは\\(￥マーク)

class Word:

    def __init__(self, english, japanese):
        self.english = english
        self.japanese = japanese


class WordQuestioner:

    def __init__(self, words):
        self._words = tuple(Word(*word) for word in words)
        self.question()

    def question(self, num=4):
        # 4(num)個の単語をsampleからselectionsに格納
        self.selections = random.sample(self._words, num)
        # answerはselectionsからランダムに一つ
        self.answer = random.choice(self.selections)


class Application(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        master.geometry("600x300")
        master.title("英単語ソフト")
        master.configure(bg='gray90')

        self.canvas = tk.Canvas(master, bg="black", width=50, height=50)
        self.canvas.place(x=350, y=240)
        
        # 英単語の問題
        self.question = tk.Label(master, width=33, bg="gray90",fg="black", font=("Helvetica 15 bold", "25", "bold"), anchor="w")
        self.question.place(x=20, y=8)

        #　解答入力欄
        #self.answer = tk.StringVar()

        #検索ボタン
        self.google = tk.Button(master, text="Google検索",bg="gray97", fg="black", font=("MSゴシック", "17", "bold"), width=10)
        self.google.place(x=420, y=10)

        self.weblio = tk.Button(master, text="Weblio検索",bg="gray97", fg="black", font=("MSゴシック", "17", "bold"), width=10)
        self.weblio.place(x=250, y=10)

        # 次に進むボタン 
        self.next = tk.Button(master, text="Next →", bg="gray97", font=("MSゴシック", "17", "bold"), width=8)
        self.next.place(x=450, y=245)

        #buttonの生成
        self.selections = [tk.Button(master,bg="gray97", fg="black", font=("MSゴシック", "14", "bold")) for i in range(4)]
        

        for i, selection in enumerate(self.selections):
            selection.place(x=20, y= 60 + 45 * i)
            

        self.pack()




    def get_csv_path(relative_path):
        try:
        # 一時フォルダのパスを取得
            base_path = sys._MEIPASS
        except Exception:
        # 一時フォルダパスを取得できない場合は実行階層パスを取得
            base_path = os.path.abspath(os.path.dirname(sys.argv[0]))

        # アイコンファイルの絶対パスを作成
        return os.path.join(base_path, relative_path)

    def correct(self):
        self.canvas.delete("x1")
        self.canvas.delete("x2")
        self.canvas.create_oval(10, 10, 43, 43, outline="red", width=5, tag="o")
        
    def wrong(self):
        self.canvas.delete("o")
        self.canvas.create_line(10, 10, 43, 43, fill="blue", width=5, tag="x1")
        self.canvas.create_line(10, 43, 43, 10, fill="blue", width=5, tag="x2")

    def clear(self):
    
        self.question["text"] = ""
        
        for selection in self.selections:
            selection["text"] = ""
            selection["fg"] = "black"
        self.canvas.delete("o")
        self.canvas.delete("x1")
        self.canvas.delete("x2")



def main():
    # Controller
    def get_csv_path(relative_path):
        try:
        # 一時フォルダのパスを取得
            base_path = sys._MEIPASS
        except Exception:
        # 一時フォルダパスを取得できない場合は実行階層パスを取得
            base_path = os.path.abspath(os.path.dirname(sys.argv[0]))

        # アイコンファイルの絶対パスを作成
        return os.path.join(base_path, relative_path)
    
    csv_path = get_csv_path("toeic.csv")
    #csv_path = 'C:\\Users\\'
    print(csv_path)

    # Model csv読み込み
    words = WordQuestioner(csv.reader(open(csv_path, encoding="utf-8-sig")))


    # View 
    win = tk.Tk()
    app = Application(master=win)
    
    # Controller
    def question():
        words.question()
        app.clear()
        app.question["text"] = f"{words.answer.english}"
        for i, (view, selection) in enumerate(zip(app.selections, words.selections), 1):
            view["text"] = f"{selection.japanese}"

    def googlereq(text):
        
        url = 'https://www.google.com/search?q='+ words.answer.english +'&sourceid=chrome&ie=UTF-8' 
        
        webbrowser.open_new_tab(url)

    def weblioreq(text):
        
        url = 'https://ejje.weblio.jp/content/' + words.answer.english
        print(words.answer.english)
        
        webbrowser.open_new_tab(url)

    # 正否判定
    def judge(event):
        
        judgetext = str(event.widget["text"])
        event.widget["fg"]
        event.widget["fg"] = "blue"

        if (judgetext) == words.answer.japanese:
            app.correct()
            event.widget["fg"] = "red"
        else:
            app.wrong()
            event.widget["fg"] = "blue"   
    
    app.selections[0].bind("<ButtonPress>", judge)
    app.selections[1].bind("<ButtonPress>", judge)
    app.selections[2].bind("<ButtonPress>", judge)
    app.selections[3].bind("<ButtonPress>", judge)
    app.google.bind("<ButtonPress>", googlereq)
    app.weblio.bind("<ButtonPress>", weblioreq)
    
    app.next["command"] = question
    
    question()
    app.mainloop()


if __name__ == "__main__":
    main()