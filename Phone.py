# -*- coding: utf-8 -*-

import jsexe as js
import answer

JS_NAME='htt.json'
#js-脚本操作，ans--答题操作
OP_TYPE='ans'

def ans():
    answer.answer2()

def jsexe():
    js.jsexe('htt.json','httre.json')


def main():
    if OP_TYPE == 'js':
        jsexe()
    elif OP_TYPE =='ans':
        ans()
    else:
        print('操作类型错误')

if __name__ == '__main__':
    main()