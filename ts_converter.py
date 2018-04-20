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
                if c not in dic:
                    dic[c] = return_json['tc'][i]

        elif type == CCType.t2s:
            for i,c in enumerate(return_json['tc']):
                if c not in dic:
                    dic[c] = return_json['sc'][i]
        return dic

# dic파일 체크하는 함수
def checkDic(file_name):
    if file_name == None:
        file_name = 'dict.json'
    with open('{}/{}'.format(os.path.dirname(os.path.abspath( __file__ )),file_name), 'r') as f:
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
                print('sc {} is redundanted ({})'.format(c,c_count))
                redundance_count += 1
                
        if redundance_count == 0:
            print('no redundanted')

        redundance_count = 0
        print('Checking tc redundance...')
        for c in return_json['tc']:
            c_count = return_json['tc'].count(c)
            if c_count > 1:
                print('tc {} is redundanted ({})'.format(c,c_count))
                redundance_count += 1

        if redundance_count == 0:
            print('no redundanted')

        print('Checking if exist same charater sc,tc...')
        for c in return_json['sc']:
            c_count = return_json['tc'].count(c)
            if c_count > 1:
                print('{} is same ({})'.format(c,c_count))
                redundance_count += 1

        if redundance_count == 0:
            print('no same character')


# csv파일로부터 데이터를 읽어와 json 파일로 만드는 함수
def make_dic_from_csv(file_name):
    try:
        with open('{}/{}'.format(os.path.dirname(os.path.abspath( __file__ )),file_name), 'r') as f:
            count = 0
            sc_string = ''
            tc_string = ''

            while True:
                line = f.readline()
                if not line:
                    break
                line_tokenized = line.split(',')
                if (line_tokenized[0] != line_tokenized[1]) and (len(line_tokenized[0]) == 1):
                    if tc_string.count(line_tokenized[0]) > 0:
                        print(line_tokenized)
                    tc_string += line_tokenized[0]
                    sc_string += line_tokenized[1]
                    count += 1
            print('count : {}'.format(count))
            with open('{}/dict.json'.format(os.path.dirname(os.path.abspath( __file__ ))), 'w') as json_f:
                out_string = '''{{
    "sc" : "{0}",
    "tc" : "{1}"
}}'''.format(sc_string,tc_string)
                json_f.write(out_string)
    except FileNotFoundError:
        print('File Not Found')
    
# 딕셔너리간에 차이점 비교하는 함수
def dif_dict(first_file_name,second_file_name):
    f0 = open('{}/{}'.format(os.path.dirname(os.path.abspath( __file__ )),first_file_name), 'r')
    f1 = open('{}/{}'.format(os.path.dirname(os.path.abspath( __file__ )),second_file_name), 'r')
    json0 = json.load(f0)
    json1 = json.load(f1)
    f1.close()
    f0.close()

    json0_sc_unique = ''
    json0_tc_unique = ''
    json1_sc_unique = ''
    json1_tc_unique = ''

    for i, c in enumerate(json0['sc']):
        if json1['sc'].count(c) == 0:
            json0_sc_unique += c
        if json1['tc'].count(json0['tc'][i]) == 0:
            json0_tc_unique += json0['tc'][i]
    for i, c in enumerate(json1['sc']):
        if json1['sc'].count(c) == 0:
            json1_sc_unique += c
        if json1['tc'].count(json1['tc'][i]) == 0:
            json1_tc_unique += json1['tc'][i]
    print('''- {0} sc unique -
{1}
- {0} tc unique -
{2}

- {3} sc unique -
{4}
- {3} tc unique -
{5}
    '''.format(first_file_name,json0_sc_unique,json0_tc_unique,second_file_name,json1_sc_unique,json1_tc_unique))

# 테스트용 메인함수
if __name__ == '__main__':
    # checkDic()
    # pass
    if len(sys.argv) == 2:
        if 'check' == sys.argv[1]:
            checkDic(None)
    elif len(sys.argv) == 3:
        if 'check' == sys.argv[1]:
            checkDic(sys.argv[2])
        elif 'make' == sys.argv[1]:
            make_dic_from_csv(sys.argv[2])
        elif CCType.s2t.name == sys.argv[1]:
            print(s2t(sys.argv[2]))
        elif CCType.t2s.name == sys.argv[1]:
            print(t2s(sys.argv[2]))
        else :
            print('{} wrong type (s2t , t2s)'.format(sys.argv[1]))
    elif len(sys.argv) == 4:
        if 'dif' == sys.argv[1]:
            dif_dict(sys.argv[2],sys.argv[3])
    
