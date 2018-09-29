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

    def id(self):
        return self.data.get('id', '?')

    def name(self):
        return self.data.get('name', '?')

    def start_time(self):
        return utils.timestamp_to_excel_date(self.data.get('start_time'))

    def end_time(self):
        return utils.timestamp_to_excel_date(self.data.get('end_time'))

    def province(self):
        return self.data.get('venue_info', {}).get('province_name')

    def city(self):
        return self.data.get('venue_info', {}).get('city_name')

    def district(self):
        return self.data.get('venue_info', {}).get('district_name')

    def venue_name(self):
        return self.data.get('venue_info', {}).get('name')

    def venue_info(self):
        return self.data.get('place_info', {}).get('name')

    def guest_count(self):
        return len(self.data.get('guests', []))

    def wish_count(self):
        return self.data.get('wish_info', {}).get('count')

    def market_price_low(self):
        return self.data.get('market_price_low', 0) / 100

    def market_price_high(self):
        return self.data.get('market_price_high', 0) / 100

    def cover(self):
        return self.data.get('cover')

    def description(self):
        return self.data.get('performance_desc', '')

    def images(self):
        return re.findall('<img src="([^"]+)"', self.description())


class Reporter:
    def __init__(self, path):
        self.path = path

    def make(self):
        dir_list = os.listdir(self.path)
        reader = ShowReader()
        workbook, sheet = utils.make_workbook()
        utils.set_columns_width(sheet, [6, 25, 25, 25, 8, 8, 8, 15, 10, 8, 8, 8, 8, 8, 8])
        sheet.append(['ID', '名称', '开始时间', '结束时间', '省级', '地级', '县级',
                      '场馆', '场馆号', '嘉宾数', '想去数', '起价', '止价'])
        for show_id in dir_list:
            reader.load(utils.get_json_file('{}/{}/index.json'.format(self.path, show_id)))
            sheet.append([
                reader.id(), reader.name(), reader.start_time(), reader.end_time(),
                reader.province(), reader.city(), reader.district(), reader.venue_name(), reader.venue_info(),
                reader.guest_count(), reader.wish_count(), reader.market_price_low(), reader.market_price_high()])
        utils.save_workbook(workbook, 'Report.xlsx')


if __name__ == '__main__':
    r = Reporter('json/')
    r.make()
