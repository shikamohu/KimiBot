#! c:/Python27/python.exe
#coding: UTF-8

import sqlite3
import random
import sys
import cgi
import datetime

class Screen:    # htmlのクラス
    def __init__(self):
        # htmlの内容
        self.html_body = u"""
            <html>
            <head>
            <meta http-equiv="content-type" content="text/html;charset=utf-8" />
            </head>
            <body>
                <form method="POST" action="/cgi-bin/kimi.py">
                    you :
                    <input type="text" name="word">
                    <input type="submit" />
                </form>
                kimi: %s<br>
                %s
            </body>
            </html>"""

    # htmlを表示
    def show(self):                 #クラス内ではselfが必要？
        print "Content-type: text/html;charset=utf-8¥n"
        print self.html_body      #クラス変数へのアクセスは、Screen.とする

#pycharm
class DB:   # DataBaseクラス
    # データベースと接続
    def __init__(self):
        self.form = cgi.FieldStorage()
        self.str = self.form.getvalue('word', '')

        #データベースと接続、無ければ作成
        self.con = sqlite3.connect("memory.db")

        # cursorオブジェクトを作る
        self.cur = self.con.cursor()

        #テーブルの作成(存在しなければ）
        self.sql = "create table if not exists log(who text, word text, time text)"          #会話履歴
        self.con.execute(self.sql)

    # コミットして、とじる
    def close(self):
        self.con.commit()
        self.con.close()

    #入力文字列をデータベースのlogテーブルに保存
    def insertLog(self, who, str):               # who = u'you' or u'kimi'
        if str:     #空なら入れない
            self.d = datetime.datetime.today()   #時間の読み込み
            self.now = self.d.strftime(u'%Y/%m/%d %H:%M:%S')      #日付と時刻に対応する文字列(例:2008/06/06 11:50:25)
            self.sql = "insert into log values('%s', '%s', '%s')" % (who, str, self.now)
            self.con.execute(self.sql)

    # logテーブルのwordを取得
    def getWords(self):
        self.cur.execute(u"select * from log")
        words = []                      # wordsリストにすべてのwordを入れる     この操作いらないかも
        for row in self.cur:                 # rowはtuple
            words.append(row[1])        # row[1]は2列目のwordの列を意味する。
        return words                    # wordsを返す

    # logテーブルのwho,word,timeを取得
    def getLogs(self):
        self.cur.execute(u"select * from log")
        logs = []                       # logsリストにすべての会話履歴を入れる
        for row in self.cur:
            logs.append(u'<b>'+row[0]+u'</b>　　　　　　　　　　　　　　　'+u'<font color="#808080">'+row[2]+u'</font><br>'+row[1]+'<br>')
        logs.reverse()                  # logsリストを反転
        return logs                     # logsを返す

    # リストのlogを一行の変数にして返す。範囲は(min~max)
    def getLinelog(self, logs, min, max):
        self.linelog = u"<br>-----------------会話履歴----------------<br>"
        for x in logs[min:max]:         # logsリストのminからmaxまでを取り出し
            self.linelog = self.linelog + x + "<br>"
        return self.linelog

    def say(self, words):

        # wordが空なら、言葉を入れてもらう
        if not words:
            words.append(u"僕はまだ言葉を知らないです")
        #文字列をランダムに選び、発言
        if self.str:     # youのstrが空でないなら
            self.kimi = random.choice(words)
            self.insertLog('you',self.str)
            print (screen.html_body % (self.kimi, self.getLinelog(self.getLogs(),0,15))).encode('utf-8')    # kimiの発言と会話履歴を出力
            self.insertLog('kimi', self.kimi)

        else :      # 空なら
            self.kimi = random.choice(words)
            print (screen.html_body % (u'', self.getLinelog(self.getLogs(),0,15))).encode('utf-8')    # 会話履歴のみ出力



        """
        #入力文字列をデータベースのlogテーブルに保存
        if str:     #youのstrが空なら入れない
            d = datetime.datetime.today()   #時間の読み込み
            now = d.strftime(u'%Y/%m/%d %H:%M:%S')      #日付と時刻に対応する文字列(例:2008/06/06 11:50:25)
            sql = "insert into log values('%s', '%s', '%s')" % (u"kimi",kimi, now)
            con.execute(sql)
        """

screen = Screen()
db = DB()
db.say(db.getWords())
db.close()








