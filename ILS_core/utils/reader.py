# coding: utf-8

from config import *
import re


def state_reader():
    u"""ステータスファイルを読み込む"""
    f = open(INIT.STATE_FILE, 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()

    for s in lines:
        pos = s.find("state")
        if pos > 0:
            r = re.compile("\d+")
            m = r.search(s)  # マッチしたらMatchObjectのインスタンスを返す
    return int(m.group(0))