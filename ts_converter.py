import json
import os
import enum
import sys

# 타입 구분을 위한 Enum
class CCType(enum.Enum):
    s2t = 's2t'
    t2s = 't2s'

# 간체에서 번체로 변환
def s2t(text : str):
    return convert(text,loadDic(CCType.s2t))

# 번체에서 간체로 변환
def t2s(text : str):
    return convert(text,loadDic(CCType.t2s))

# 실질적으로 변환을 하는 함수
def convert(text : str , dic : dict):
    returnString = ''
    for c in text:
        returnString += dic[c] if c in dic else c
    return returnString

# dict.json파일에서 간체,번체를 읽어와 dictionary로 변환하는 함수
def loadDic(type : CCType):
    with open('{}/dict.json'.format(os.path.dirname(os.path.abspath( __file__ ))), 'r') as f:
        return_json = json.load(f)
        dic = {}

        if len(return_json['sc']) != len(return_json['tc']):
            print('cc dictionary error')
            return dic

        if type == CCType.s2t:
            for i,c in enumerate(return_json['sc']):
                dic[c] = return_json['tc'][i]

        elif type == CCType.t2s:
            for i,c in enumerate(return_json['tc']):
                dic[c] = return_json['sc'][i]
        return dic

def checkDic():
    with open('{}/dict.json'.format(os.path.dirname(os.path.abspath( __file__ ))), 'r') as f:
        return_json = json.load(f)
        redundance_count = 0

        print('Checking is tc_count sc_count equal : ',end='')
        if len(return_json['sc']) == len(return_json['tc']):
            print('OK - count : {}'.format(len(return_json['sc'])))
        else:
            print('FAILED - sc : {} , tc : {}'.format(len(return_json['sc']),len(return_json['tc'])))

        print('Checking sc redundance...')
        for c in return_json['sc']:
            c_count = return_json['sc'].count(c)
            if c_count > 1:
                print('{} is redundanted ({})'.format(c,c_count))
                redundance_count += 1
                
        if redundance_count == 0:
            print('no redundanted')

        redundance_count = 0
        print('Checking tc redundance...')
        for c in return_json['tc']:
            c_count = return_json['tc'].count(c)
            if c_count > 1:
                print('{} is redundanted ({})'.format(c,c_count))
                redundance_count += 1

        if redundance_count == 0:
            print('no redundanted')

        print('Checking if exist same charater sc,tc...')
        for c in return_json['sc']:
            c_count = return_json['tc'].count(c)
            if c_count > 1:
                print('{} is redundanted ({})'.format(c,c_count))
                redundance_count += 1

        if redundance_count == 0:
            print('no redundanted')

# 테스트용 메인함수
if __name__ == '__main__':
    # checkDic()
    # pass
    if len(sys.argv) <= 2:
        pass
    elif len(sys.argv) == 3:
        if CCType[sys.argv[1]] == CCType.s2t or CCType[sys.argv[1]] == CCType.t2s:
            if CCType.s2t == CCType[sys.argv[1]]:
                print(s2t(sys.argv[2]))
            elif CCType.t2s == CCType[sys.argv[1]]:
                print(t2s(sys.argv[2]))
        else:
            print('{} wrong type (s2t , t2s)'.format(sys.argv[1]))
    
