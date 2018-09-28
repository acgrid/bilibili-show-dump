import utils
import threading
import os
import report


class DownloadThread(threading.Thread):
    def __init__(self, path):
        """

        :param str path:
        """
        threading.Thread.__init__(self)
        self.path = path

    def download(self, image, filename=None):
        """

        :param str image:
        :param str filename:
        :return:
        """
        if filename is None:
            filename = os.path.basename(image)
        local = self.path + '/' + filename
        if os.path.exists(local):
            print('Skipping ' + filename)
            return
        if image.startswith('//'):
            image = "https:" + image
        resp = utils.requests_retry_session().get(image)
        with open(local, 'wb') as f:
            f.write(resp.content)

    def run(self):
        reader = report.ShowReader()
        reader.load(utils.get_json_file('{}/index.json'.format(self.path)))
        cover = reader.cover()
        if len(cover):
            self.download(cover, 'cover.jpg')
        images = reader.images()
        if len(images):
            for image in images:
                self.download(image)


class ImageDownloader:
    def __init__(self, path):
        self.path = path

    def download(self):
        chunks = utils.make_chunks(os.listdir(self.path), 8)
        batch = len(chunks)
        current = 1
        for chunk in chunks:
            print('Batch {}/{} started'.format(current, batch))
            pool = []
            for show_id in chunk:
                thread = DownloadThread('{}{}'.format(self.path, show_id))
                thread.start()
                pool.append(thread)
                print('Show ID {} started'.format(show_id))
            for thread in pool:
                thread.join()
            current += 1
        print('Finished')


if __name__ == '__main__':
    r = ImageDownloader('json/')
    r.download()
