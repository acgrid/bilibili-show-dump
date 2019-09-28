import utils
import threading
import requests


class PageDownloader:
    def __init__(self, request, event_id):
        """

        :param requests request:
        :param int event_id:
        """
        self.request = request
        self.event_id = event_id

    def download(self, page):
        response = self.request.post("http://www.allcpp.cn/allcpp/event/getalldoujinshiforcircle.do", json=
            {"event": self.event_id, "param": "", "type": 3, "list": "",
             "num": page, "size": 30, "sectionid": ""}, headers={
                "errorWrap": "json",
                "Origin": "http://www.allcpp.cn",
                "Referer": "http://www.allcpp.cn/allcpp/event/eventorg.do?event=541",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Cookie": "JALKSJFJASKDFJKALSJDFLJSF=163174109124d099959a029e4a8eb3ecb0375c88e145106.83.117.214_20023679253; randomCode=cppb87dc95a932b4580b609fc4a6b31b7d0106.83.117.214_217552492183E44; token=736468D40FEDFD2D906E7871DAFE29655BC84E08F22FC4286716F3C333A3A7E652E4A916CD795DC0425EE14713F8B49CB2BB37802B200418BA5CD3BB6BA4BEB0; Hm_lvt_75e110b2a3c6890a57de45bd2882ec7c=1543823502,1543824278,1544323732,1544599641; JSESSIONID=382E62579BAA7A8B18AFF91B0ECB0C68; Hm_lpvt_75e110b2a3c6890a57de45bd2882ec7c=1544617040"})
        response = response.json()
        try:
            if response['isSuccess']:
                print('{}: OK'.format(page))
                utils.save_json('cpp/{}/{}.json'.format(self.event_id, page), response['result']['list'])
            else:
                print('{}: {}'.format(self.event_id, response['message']))
        except (KeyError, ValueError, TypeError, AttributeError) as e:
            print('{}: {}'.format(self.event_id, response.content))


class CollectThread(threading.Thread):
    def __init__(self, srv, show_id):
        """

        :param PageDownloader srv:
        :param show_id:
        """
        threading.Thread.__init__(self)
        self.service = srv
        self.id = show_id

    def run(self):
        self.service.download(self.id)


if __name__ == '__main__':
    service = PageDownloader(utils.requests_retry_session(), int(input('Event ID:')))
    start = int(input('Start ID:'))
    end = int(input('End ID:'))
    if start > end or start <= 0:
        print('Start - End is invalid')
        exit(1)
    chunks = utils.make_chunks(range(start, end + 1), 10)
    for chunk in chunks:
        pool = []
        for show_id in chunk:
            thread = CollectThread(service, show_id)
            thread.start()
            pool.append(thread)
        for thread in pool:
            thread.join()
