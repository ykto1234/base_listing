import os
import traceback
import settings
import scraip
from item import ItemInfo

if __name__ == '__main__':

    try:
        # 出品商品リスト
        item_list = []

        # 出品成功した商品リスト
        success_list = []
        # 出品スキップした商品リスト
        skip_list = []

        print('処理を開始します')

        # 設定ファイル読み込み
        config_default = settings.read_config('DEFAULT')

        print('出品商品リストを読み込みます')

        # 出品用ファイルのパス取得
        path = config_default.get('ITEM_FILE_PATH')
        if path == None:
            # 値が存在しない場合
            raise Exception

        # 出品用ファイルのシート名取得
        sheet_name = config_default.get('ITEM_FILE_SHEET')
        if sheet_name == None:
            # 値が存在しない場合
            raise Exception

        # 出品商品リストファイルの読み込み（全て欠損値がある行は読み込まない）
        item_df = settings.read_item_list(path, sheet_name, 0, 'A:I')

        for i in range(0, len(item_df)):
            #print(str(i+1) + 'つ目のファイルの処理を開始します')

            _item = ItemInfo()
            _item.setFromExcelRow(item_df.iloc[i])

            # リストに追加
            item_list.append(_item)

            #print(str(i+1) + 'つ目のファイルの処理が完了しました')
            #print('----------------------------------------')

        print('出品商品リストの読み込みが完了しました')

        # 出品処理
        print('出品処理を開始します')
        URL      = "https://admin.thebase.in/shop_admin/items/add" # <= スクレイピングしたい対象URL
        ID_sel   = "#loginUserMailAddress"       # <= ログインID欄のCSSセレクタ
        PASS_sel = "#UserPassword"               # <= ログインパスワード欄のCSSセレクタ

        ID = config_default.get('ID')
        if ID == None:
            # 値が存在しない場合
            raise Exception
        PASS = config_default.get('PASSWORD')
        if PASS == None:
            # 値が存在しない場合
            raise Exception

        # ブラウザ表示オプションの取得
        DISPLAY = config_default.get('DISPLAY')

        # ログイン処理
        driver = scraip.login(URL, ID, PASS, ID_sel, PASS_sel, DISPLAY)

        for item in item_list:
            # 商品登録処理
            ret = scraip.item_listing(driver, item, URL)
            if ret:
                success_list.append(item.unit_number)
            else:
                skip_list.append(item.unit_number)

        # ブラウザを終了する。
        driver.close()

        print('出品処理が完了しました')
        #『続行するには何かキーを押してください . . .』と表示させる
        #os.system('PAUSE')

    except Exception as err:
        print('処理が失敗しました')
        print(err)
        print(traceback.format_exc())
        print(success_list)
        #『続行するには何かキーを押してください . . .』と表示させる
        os.system('PAUSE')

