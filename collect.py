import utils
import threading
import requests


class ShowInfoDownloader:
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
        try:
            json = response.json()
            if json['errno'] == 0:
                print('{}: OK'.format(show_id))
                utils.save_json('{}/{}/index.json'.format(self.dist, show_id), json['data'])
            else:
                print('{}: {}'.format(show_id, json['msg']))
        except (KeyError, ValueError, TypeError, AttributeError) as e:
            print('{}: {}'.format(show_id, response.content))


class CollectThread(threading.Thread):
    def __init__(self, srv, show_id):
        """

        :param ShowInfoDownloader srv:
        :param show_id:
        """
        threading.Thread.__init__(self)
        self.service = srv
        self.id = show_id

    def run(self):
        self.service.download(self.id)


if __name__ == '__main__':
    service = ShowInfoDownloader(utils.requests_retry_session(), 'json',
                                 'https://show.bilibili.com/api/ticket/project/get?version=133&id={}')
    start = int(input('Start ID:'))
    end = int(input('End ID:'))
    if start > end or start <= 0:
        print('Start - End is invalid')
        exit(1)
    while start <= end:
        service.download(start)
        start += 1
