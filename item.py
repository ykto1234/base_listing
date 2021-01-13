import os
import glob
from os.path import join

class ItemInfo:
    def __init__(self):
        self.unit_number = None
        self.name = None
        self.photo_path_list = []
        self.detail = None
        self.price = None
        self.release_flg = False
        self.display_top_flg = True
        self.category_list = []
        self.size = None
        self.color = None
        self.stockinfo_list = []

    class StockInfo:
        def __init__(self, stock, item_type):
            self.stock = stock
            self.type = item_type


    def createStockInfo(size, color):
        stock_list = []
        size_list = []
        color_list = []

        size_list = size.split(',')
        color_list = color.split(',')

        for i in range(0, len(size_list)):
            for j in range(0, len(color_list)):
                # 在庫情報のインスタンスを生成、、値設定
                str_type = ''
                if color_list[j] == '':
                    str_type = size_list[i]
                elif size_list[i] == '':
                    str_type = color_list[j]
                else:
                    str_type = color_list[j] + " " + size_list[i]

                _stockinfo = ItemInfo.StockInfo(999, str_type)
                stock_list.append(_stockinfo)

        return stock_list


    def setFromExcelRow(self, item_row):
        self.unit_number = str(item_row['管理番号'])
        self.name = str(item_row['商品名'])
        self.photo_path_list = ItemInfo.create_photo_path(self.unit_number)
        self.detail = str(item_row['商品説明文'])
        self.price = str(round(item_row['商品価格']))
        self.release_flg = ItemInfo.get_release_flg(str(item_row['商品公開フラグ']))
        self.display_top_flg = True
        self.category_list = str(item_row['タグ']).split(',')
        self.size = str(item_row['商品サイズ'])
        self.color = str(item_row['商品カラー'])
        if not (self.size == None and self.color == None):
            # どちらかが空じゃなければ在庫情報を作成
            self.stockinfo_list = ItemInfo.createStockInfo(self.size, self.color)

    def create_photo_path(unit_number):
        path_list = []
        target_path = os.getcwd() + "/input/image/" + unit_number + "/ロゴ付き画像/"
        for ext in ('*.gif', '*.png', '*.jpg'):
            path_list.extend(glob.glob(join(target_path, ext)))
        return path_list

    def get_release_flg(release_str):
        flg = False
        if release_str == '公開':
            flg = True
        return flg
