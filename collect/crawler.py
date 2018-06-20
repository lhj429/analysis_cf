import sys
from urllib.request import Request, urlopen
from datetime import datetime

# err=error
# def error(e):
#     print('%s : %s' % (e, datetime.now()), file=sys.stderr)

def crawling(
        url = '',
        encoding = 'utf-8',
        proc=lambda html:html,
        store=lambda html:html,
        err=lambda e : print('%s : %s' % (e, datetime.now()), file=sys.stderr)):

    try:
        request = Request(url)
        resp = urlopen(request)

        try:
            receive = resp.read()
            result = store(proc(receive.decode(encoding)))

            # def crawling(url = '', encoding = 'utf-8', proc=None, err=lambda e : print('%s : %s' % (e, datetime.now()), file=sys.stderr)):
            # receive = resp.read()
            # result = receive.decode(encoding)
            # if proc is not None:
            #     result = proc(result)
            #                               -> processing : if문 없애고 함수 파라미터에서 람다로 처리

            # def crawling(url = '', encoding = 'utf-8', proc=lambda html:html, store=None, err=lambda e : print('%s : %s' % (e, datetime.now()), file=sys.stderr)):
            # receive = resp.read()
            # result = receive.decode(encoding)
            # if store is not None :
            #     result = store(result)
            #                               -> saving : if문 없애고 함수 파라미터에서 람다로 처리


            # receive = resp.read()
            # result = receive.decode(encoding)
            # result = proc(result)
            # result = store(result)
            #                               -> processing, saving : 모두 람다로 처리

        except UnicodeDecodeError:
            result = receive.decode(encoding, 'replace')

        print('%s: success for request [%s]' % (datetime.now(), url))
        return result
    except Exception as e:
        err(e)
