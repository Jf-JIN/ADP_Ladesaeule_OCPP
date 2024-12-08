
import os

dirpath = os.path.dirname(__file__)


def json2py():
    for i in os.listdir(dirpath):
        if i.endswith(".json") and i != os.path.basename(__file__):
            with open(os.path.join(dirpath, i), 'r', encoding='utf-8') as f:
                line = f.readline()
                line_list = []
                while line:
                    line_list.append(line.strip())
                    line = f.readline()
            text = ''.join(line_list)
            text = text.replace('false', 'False')
            text = text.replace('true', 'True')
            text = text.replace('null', 'None')
            text = f'_{os.path.splitext(i)[0]} = {text}'
            with open(os.path.join(dirpath, i.replace('.json', '.py')), 'w', encoding='utf-8') as f:
                f.write(text)


def all_in_one():
    all_text_list = []
    for i in os.listdir(dirpath):
        if i.endswith(".json") and i != os.path.basename(__file__):
            with open(os.path.join(dirpath, i), 'r', encoding='utf-8') as f:
                line = f.readline()
                line_list = []
                while line:
                    line_list.append(line.strip())
                    line = f.readline()
            text = ''.join(line_list)
            text = text.replace('false', 'False')
            text = text.replace('true', 'True')
            text = text.replace('null', 'None')
            text = f'_{os.path.splitext(i)[0]} = {text}'
            all_text_list.append(text)
    text = '\n'.join(all_text_list)
    with open(os.path.join(dirpath, 'OCPP_All_Standard.py'), 'w', encoding='utf-8') as f:
        f.write(text)


all_in_one()
