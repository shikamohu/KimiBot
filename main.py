#! c:/Python27/python.exe
#coding: UTF-8

import sqlite3
import random
import sys


if __name__ == "__main__":

    #データベースと接続、無ければ作成
    con = sqlite3.connect("memory.db")

    # cursorオブジェクトを作る
    cur = con.cursor()

    #テーブルの作成(存在しなければ）
    sql = "create table if not exists person(name text, sex text, age integer)"   #個人情報
    con.execute(sql)
    sql = "create table if not exists greeting(word text, situation text)"        #挨拶
    con.execute(sql)
    sql = "create table if not exists unknown(word text)"                         #未分類
    con.execute(sql)

    # 無限ループ
    while 1:

        #キーボード入力の文字列を受け取る
        str = raw_input("you: ").decode(sys.stdin.encoding)   #.decode(sys.stdin.encoding)とすると、エラーがでない

        #入力文字列が「さようなら」なら終了
        if str == u"さようなら":
            print u"kimi: 絶望するな。では、失敬"
            print u"アプリケーションを終了しました"
            break

        #入力文字列をデータベースのunknownテーブルに保存
        sql = "insert into unknown values('%s')" % (str)
        con.execute(sql)

        # unknownテーブルのwordを取得
        cur.execute(u"select * from unknown")
        words = []
        # wordsリストにすべてのwordを入れる
        for row in cur: # rowはtuple
            words.append(row[0])        # row[0]は1列目のwordの列を意味する。

        # wordsリストからランダムに発言する
        print u"kimi: " + random.choice(words)

    # コミットして、とじる
    con.commit()
    con.close()

