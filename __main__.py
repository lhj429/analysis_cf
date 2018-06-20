from itertools import count
from bs4 import BeautifulSoup
import collect.crawler as cw

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
# result = cw.crawling(url='https://movie.naver.com/movie/sdb/rank/rmovie.nhn', encoding='cp949', proc=proc, store=store

def crawling_pelicana():
    results = []
    for page in count(start=1):
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

    print(results)

if __name__ == '__main__':

    # pelicana
    crawling_pelicana()