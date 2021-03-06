import urllib
from itertools import count
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as et
import time
from selenium import webdriver
import collect.crawler as cw
from collect.data_dict import sido_dict, gungu_dict

# err=None
# def my_error():
#     print("myerror:" + str(e))

# 에러 처리 방법 3가지
# 1. crawling 함수 내부 : except Exception as e: print('%s : %s' % (e, datetime.now()), file=sys.stderr
# 2. main 함수 : def my_error(): print("myerror:" + str(e))
# 3. crawling 함수 parameter : err=lambda e : print('%s : %s' % (e, datetime.now()), file=sys.stderr

# def proc(html):
#     print('processing...' + html)
#
# def store(html):
#     pass

# result = cw.crawling(url='https://movie.naver.com/movie/sdb/rank/rmovie.nhn', encoding='cp949')
# result = cw.crawling(url='https://movie.naver.com/movie/sdb/rank/rmovie.nhn', encoding='cp949', proc=proc)
# result = cw.crawling(url='https://movie.naver.com/movie/sdb/rank/rmovie.nhn', encoding='cp949', proc=proc, store=store)

RESULT_DIRECTORY = '__result__/crawling'

def crawling_pelicana():
    results = []
    for page in count(start=1):
    # for page in range(1, 3):
        url = 'http://www.pelicana.co.kr/store/stroe_search.html?&gu=&si=&page=%d' %(page)
        html = cw.crawling(url=url)

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class':'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if len(tags_tr) == 0:
            break
        # print(page, len(tags_tr), sep=':')

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)

            name = strings[1]
            address = strings[3]
            sidogu = address.split()[:2]

            results.append( (name, address) + tuple(sidogu) )       # tuple 형태로 넣음; 순서가 정해져 있음, 변경 불가

    # save
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v:sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/pelicana_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)

def proc_nene(xml):
    root = et.fromstring(xml)
    results = []

    for el in root.findall('item'):
        name = el.findtext('aname1')
        sido = el.findtext('aname2')
        gungu = el.findtext('aname3')
        address = el.findtext('aname5')

        results.append((name, address, sido, gungu))

    return results

def store_nene(data):
    table = pd.DataFrame(data, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/nene_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)

# 강원강릉시내곡점,강원강릉시범일로579번길49-2,강원도,강릉시
def crawling_kyochon():
    results = []
    for sido1 in range(1, 18):
        for sido2 in count(start=1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' %(sido1, sido2)
            html = cw.crawling(url=url)
            if html == None:
                break

            bs = BeautifulSoup(html, 'html.parser')
            tag_div = bs.find('div', attrs={'class': 'shopSchList'})
            tag_ul = tag_div.find('ul', attrs={'class': 'list'})
            tags_li = tag_ul.findAll('li')


            for tag_li in tags_li:
                strings = list(tag_li.strings)
                if strings[0] == '검색결과가 없습니다.':
                    break
                name = strings[3]
                address = strings[5].replace('\n', '').replace('\t', '').replace('\r', '')
                sidogu = address.split()[:2]
                results.append((name, address) + tuple(sidogu))

    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/kyochon_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)

def crawling_goobne():
    url = 'https://www.goobne.co.kr/store/search_store.jsp'

    # 첫 페이지 로딩
    wd = webdriver.Chrome('D:/chromedriver/chromedriver.exe')
    wd.get(url)
    time.sleep(5)

    results = []
    for page in count(start=1):
        # 자바 스크립트 실행
        script = "store.getList(%d);" % page
        wd.execute_script(script)
        print('%s : success for script execute [%s]' %(datetime.now(), script))
        time.sleep(5)

        # 실행결과 HTML(rendering된 HTML) 가져오기
        html = wd.page_source

        # parsing
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id':'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # 마지막 검출
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]

            results.append((name, address) + tuple(sidogu))

    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/goobne_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)

if __name__ == '__main__':

    # pelicana
    # crawling_pelicana()

    # nene
    # cw.crawling(
    #     # url = 'http://nenechicken.com/subpage/where_list.asp?target_step2=%EC%A0%84%EC%B2%B4&proc_type=step1&target_step1=%EC%A0%84%EC%B2%B4'
    #     url = 'http://nenechicken.com/subpage/where_list.asp?target_step2=%s&proc_type=step1&target_step1=%s' % (urllib.parse.quote('전체'), urllib.parse.quote('전체')),
    #     proc=proc_nene,
    #     store=store_nene
    # )

    # kyochon
    crawling_kyochon()

    # goobne
    # crawling_goobne()
