import utils
import threading
import requests


class PageDownloader:
    def __init__(self, request, dist, pattern):
        """

        :param requests request:
        :param str dist:
        :param str pattern:
        """
        self.request = request
        self.dist = dist
        self.pattern = pattern

    def download(self, show_id):
        show_id = str(show_id)
        url = self.pattern.format(show_id)
        response = self.request.get(url)
        content = response.content.decode('utf-8')
        if '该展会不存在，或者被删除' in content:
            print('{}: 不存在'.format(show_id))
        else:
            print('{}: OK'.format(show_id))
            utils.save_file('{}/{}.html'.format(self.dist, show_id), content)


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
    service = PageDownloader(utils.requests_retry_session(), 'nyato', 'https://www.nyato.com/manzhan/{}/')
    start = int(input('Start ID:'))
    end = int(input('End ID:'))
    if start > end or start <= 0:
        print('Start - End is invalid')
        exit(1)
    chunks = utils.make_chunks(range(start, end), 10)
    for chunk in chunks:
        pool = []
        for show_id in chunk:
            thread = CollectThread(service, show_id)
            thread.start()
            pool.append(thread)
        for thread in pool:
            thread.join()
