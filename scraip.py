import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import chromedriver_binary
from item import ItemInfo


def login(url, id, pw, id_sel, pw_sel, display):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from bs4 import BeautifulSoup

    # chromeドライバーのパス
    chrome_path = "./driver/chromedriver.exe"

    # Selenium用オプション
    if display == '0':
        # 「0」が設定されている場合は、ブラウザを表示して実行する
        op = Options()
        op.add_argument("--disable-gpu")
        op.add_argument("--disable-extensions")
        op.add_argument("--proxy-server='direct://'")
        op.add_argument("--proxy-bypass-list=*")
        op.add_argument("--start-maximized")
        op.add_argument("--headless")
        #driver = webdriver.Chrome(chrome_options=op)
        driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=op)
    else:
        # 「0」以外の場合は、ブラウザを非表示にして実行する
        #driver = webdriver.Chrome()
        driver = webdriver.Chrome(executable_path=chrome_path)

    # ログインページアクセス
    driver.get(url)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, pw_sel))
    )
    driver.find_elements_by_css_selector(id_sel)[0].send_keys(id)
    driver.find_elements_by_css_selector(pw_sel)[0].send_keys(pw)
    driver.find_elements_by_css_selector(pw_sel)[0].send_keys(Keys.ENTER)

    return driver


def item_listing(driver, item, url):
    NAME_sel = "#itemDetail_name"                 # 商品名のCSSセレクタ
    PHOTO1_sel = ".m-uploadBox__input"            # 商品画像のCSSセレクタ
    PHOTO2_sel = ".fileInput_pEN_uRSd"            # 商品画像のCSSセレクタ
    DETAIL_sel = "#itemDetail_detail"             # 商品説明のCSSセレクタ
    PRICE_sel = "#itemDetail_price"               # 商品価格のCSSセレクタ
    STOCK_sel = "#itemDetail_stock"               # 商品在庫のCSSセレクタ
    ADDSTOCK_sel = "body > div.root > main > div > div.c-container-noPadding.itemDetailContainer_uZ_MGZcw > div > section:nth-child(4) > div.row_2mAscmNh > dl > div.body_KNpXtKXd > dd > button"
    #TYPE_name = "variationText"                   # 種類のname
    TYPE_xpath = "/html/body/div[3]/main/div/div[3]/div/section[4]/div[2]/dl/div[2]/dd/table/tbody/tr[{idx1}]/td[1]/div/input"                   # 種類のxpath
    #STOCK_name = "variationStock"                 # 在庫のname
    STOCK_xpath = "/html/body/div[3]/main/div/div[3]/div/section[4]/div[2]/dl/div[2]/dd/table/tbody/tr[{idx1}]/td[2]/div/input"                 # 在庫のxpath
    CHECK1_sel = "#orderfirst"                    # 一番上表示チェックボックスのCSSセレクタ
    CHECK2_sel = "#display"                       # 公開チェックボックスのCSSセレクタ
    ITEMCODE_sel = ".formInput_1foJxi9g input"    # 商品コードのCSSセレクタ

    driver.get(url)

    # ターゲット出現を待機
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, NAME_sel))
    )

    # 商品名
    if item.name == None:
        # 商品名がない場合、この商品は出品スキップ
        return False

    driver.find_elements_by_css_selector(NAME_sel)[0].send_keys(item.name)

    # 画像
    # ※１枚１枚画像を追加していると、１回で複数枚登録されてしまうので、パスを「\n」で結合した文字列を１回で渡す
    if len(item.photo_path_list) > 20:
        # ２０枚以上ある場合、２０枚になるまで削除
        count = len(item.photo_path_list) - 20
        for cnt in range(0, count):
            del item.photo_path_list[-1]

    join_photo_path_list = None
    if len(item.photo_path_list) == 1:
        driver.find_elements_by_css_selector(PHOTO1_sel)[0].send_keys(item.photo_path_list[0])
    elif len(item.photo_path_list) > 1:
        join_photo_path_list = '\n'.join(item.photo_path_list)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PHOTO1_sel))
        )
        driver.find_elements_by_css_selector(PHOTO1_sel)[0].send_keys(join_photo_path_list)
        # 画像アップロードするのに時間がかかるため、仕方なくsleepで一定時間待つ
        sleep_time = 1
        if len(item.photo_path_list) > 5:
            sleep_time = 3
        if len(item.photo_path_list) > 10:
            sleep_time += 3
        if len(item.photo_path_list) > 15:
            sleep_time += 3
        time.sleep(sleep_time)

    # 説明
    driver.find_elements_by_css_selector(DETAIL_sel)[0].send_keys(item.detail)
    # 価格
    if int(item.price) < 50 or int(item.price) > 500000:
        # 価格が49以下かまたは500,001円以上の場合、この商品は出品スキップ
        return False
    driver.find_elements_by_css_selector(PRICE_sel)[0].send_keys(item.price)
    # 税率は10%のまま
    # 在庫と種類
    if len(item.stockinfo_list) == 0:
        # 在庫がない場合、この商品は出品スキップ
        return False
    if len(item.stockinfo_list) == 1:
        # 商品が１つならそのまま
        driver.find_elements_by_css_selector(STOCK_sel)[0].send_keys(item.stockinfo_list[0].stock)
    elif len(item.stockinfo_list) > 1:
        # 商品が２つなら
        # １回行を追加する
        WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ADDSTOCK_sel))
        )
        driver.find_elements_by_css_selector(ADDSTOCK_sel)[0].click()

        # ターゲット出現を待機
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, TYPE_xpath.format(idx1=1)))
        )
        # １行目入力
        #driver.find_elements_by_name(TYPE_name + "0")[0].send_keys(item.stockinfo_list[0].type)
        #driver.find_elements_by_name(STOCK_name + "0")[0].send_keys(item.stockinfo_list[0].stock)
        driver.find_elements_by_xpath(TYPE_xpath.format(idx1=1))[0].send_keys(item.stockinfo_list[0].type)
        driver.find_elements_by_xpath(STOCK_xpath.format(idx1=1))[0].send_keys(item.stockinfo_list[0].stock)
        # ２行目入力
        driver.find_elements_by_xpath(TYPE_xpath.format(idx1=2))[0].send_keys(item.stockinfo_list[1].type)
        driver.find_elements_by_xpath(STOCK_xpath.format(idx1=2))[0].send_keys(item.stockinfo_list[1].stock)

    if len(item.stockinfo_list) > 2:
        # 商品が３つ以上なら
        for j in range(2, len(item.stockinfo_list)):
            # ターゲット出現を待機
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ADDSTOCK_sel))
            )
            driver.find_elements_by_css_selector(ADDSTOCK_sel)[0].click()

            # ターゲット出現を待機
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, TYPE_xpath.format(idx1=j)))
            )
            # 種類と在庫を入れる
            #driver.find_elements_by_name(TYPE_name + str(j))[0].send_keys(item.stockinfo_list[j].type)
            driver.find_elements_by_xpath(TYPE_xpath.format(idx1=j+1))[0].send_keys(item.stockinfo_list[j].type)
            #driver.find_elements_by_name(STOCK_name + str(j))[0].send_keys(item.stockinfo_list[j].stock)
            driver.find_elements_by_xpath(STOCK_xpath.format(idx1=j+1))[0].send_keys(item.stockinfo_list[j].stock)

    # 一番上に表示チェックボックスをONにする
    # ※pythonのsendkeyでは、「element not interactable」エラーが出るため、JavaScriptを使用してチェックボックスをクリックする
    chkbox_topdisplay = driver.find_elements_by_css_selector(CHECK1_sel)[0]
    if item.display_top_flg:
        # TOP表示フラグONの場合
        if chkbox_topdisplay.is_selected:
            pass
        else:
            driver.execute_script("arguments[0].click();",chkbox_topdisplay)
    else:
        # TOP表示フラグOFFの場合
        if chkbox_topdisplay.is_selected:
            driver.execute_script("arguments[0].click();",chkbox_topdisplay)
        else:
            pass

    # 公開するチェックボックスをONにする
    # ※pythonのsendkeyでは、「element not interactable」エラーが出るため、JavaScriptを使用してチェックボックスをクリックする
    chkbox_release = driver.find_elements_by_css_selector(CHECK2_sel)[0]
    if item.release_flg:
        # 公開フラグONの場合
        if chkbox_release.is_selected:
            pass
        else:
            driver.execute_script("arguments[0].click();",chkbox_release)
    else:
        # 公開フラグOFFの場合
        if chkbox_release.is_selected:
            driver.execute_script("arguments[0].click();",chkbox_release)
        else:
            pass

    # 商品コード（管理番号）
    driver.find_elements_by_css_selector(ITEMCODE_sel)[0].send_keys(item.unit_number)

    # カテゴリ選択
    if len(item.category_list) > 0:
        for category in item.category_list:
            category_checkbox_click(driver, category)

    # 登録ボタンを押下
    # TODO:セレクタの指定方法
    driver.find_elements_by_css_selector("body > div.root > main > div > div.buttonArea_2Riqfn9k > button.c-submitBtn.c-submitBtn--full.btn_2LTaF8Qc > div")[0].click()

    return True


#def button_click(driver, button_text):
#    buttons = driver.find_elements_by_tag_name("button")
#
#    for button in buttons:
#        if button.text == button_text:
#            button.click()
#            break

def category_checkbox_click(driver, chkbox_text):
    target_index = None
    # textが一致するwrapperのインデックスを取得する
    text_wrappers = driver.find_elements_by_css_selector(".c-checkbox__textWrapper")

    for idx in range(0, len(text_wrappers)):
        if text_wrappers[idx].text == chkbox_text:
            target_index = idx
            break

    # ※pythonのsendkeyでは、「element not interactable」エラーが出るため、JavaScriptを使用してチェックボックスをクリックする
    if not target_index == None:
        chkbox = driver.find_elements_by_css_selector(".c-checkbox__input")[target_index]
        driver.execute_script("arguments[0].click();",chkbox)

