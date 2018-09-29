import utils
import os
import re


class ShowReader:
    def __init__(self):
        self.data = None

    def load(self, data):
        """

        :param dict data:
        :return:
        """
        self.data = data

    def name(self):
        return utils.match_single(self.data, '>([^<]+)</h2>', '') \
               or utils.match_single(self.data, '<title>([^<]+)</title>')

    def start_time(self):
        return utils.match_date(self.data, '(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) - \d{4}-\d{2}-\d{2} \d{2}:\d{2}</div>')

    def end_time(self):
        return utils.match_date(self.data, '\d{4}-\d{2}-\d{2} \d{2}:\d{2} - (\d{4}-\d{2}-\d{2} \d{2}:\d{2})</div>')

    def location(self):
        return utils.match_single(self.data, '<span class="fl mr10">([^<]+)</span>', '')\
            .replace('　', '').replace('海 外', '海外').replace('黑龙江省', '黑龙江').split(' ', 4)

    def went(self):
        return utils.match_single(self.data, '共(\d+)人参加', 0, int)

    def star(self):
        return utils.match_single(self.data, 'star-(\d\.\d)\.png', None, float)

    def guest_count(self):
        return utils.match_count(self.data, '<a class="fl cursor-no hidden guest" title="[^"]+" href="[^"]+">')

    def market_price(self):
        return utils.match_single(self.data, '现场票(\d+\.\d+)元</span>', None, float)

    def online_price(self):
        return utils.match_single(self.data, '<b class="f40">¥ (\d+\.\d+)</b>', None, float)


class Reporter:
    def __init__(self, path):
        self.path = path

    def make(self):
        files = os.listdir(self.path)
        reader = ShowReader()
        workbook, sheet = utils.make_workbook()
        utils.set_columns_width(sheet, [6, 25, 22, 22, 8, 8, 8, 25, 6, 8, 8, 8, 8])
        sheet.append(['ID', '名称', '开始时间', '结束时间', '省级', '地级', '县级',
                      '场馆', '星级', '嘉宾数', '去过数', '现场票价', '电子票价'])
        for file in files:
            reader.load(utils.get_json_file('{}/{}'.format(self.path, file)))
            location = reader.location()
            location += [''] * (4 - len(location))
            sheet.append([
                int(re.search('\d+', file).group(0)), reader.name(), reader.start_time(), reader.end_time(),
                location[0], location[1], location[2], location[3],
                reader.star(), reader.guest_count(), reader.went(), reader.market_price(), reader.online_price()])
        utils.save_workbook(workbook, 'Nyato.xlsx')


if __name__ == '__main__':
    r = Reporter('nyato/')
    r.make()
    print('OK')
