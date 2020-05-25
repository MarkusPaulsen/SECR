from typing import *
import sqlite3
from sqlite3 import Cursor, Connection
from os import listdir
from os.path import isfile, join

_data_base: Connection = sqlite3.connect('../models/Model/DB.db')
_cursor: Cursor = _data_base.cursor()

def build_dataset_test(table: str):
    X = []
    Y = []
    sentence = ''
    relevance = 0
    query = "SELECT Word,TokenSet FROM " + table + " Order BY FileName, Line"
    table_contents = list(_cursor.execute(query))
    for table_content in table_contents:
        word = table_content[0]
        token_set = table_content[1]
        if len(word) == 0:
            if sentence != '':
                X.append(sentence)
                Y.append(relevance)
                sentence = ''
                relevance = 0
        else:
            if token_set == "" or token_set != 'O':
                relevance = 1
            if word in [",", "-", "."]:
                sentence = (sentence + word).strip()
            else:
                sentence = (sentence + ' ' + word).strip()
    return X, Y

train_X, train_Y = build_dataset_test(table="Train_Token")
dev_X, dev_Y = build_dataset_test(table="Dev_Token")
test_X, test_Y = build_dataset_test(table="Test_Token")