from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pit import Pit

import json
import codecs
import re
import os
import time
import datetime

# import io
# import sys
# import traceback

# # デバッグの文字出力の文字化け対応
# sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class forSurvey:
    def __init__(self, mode='None'):
        # Basic認証/ログイン情報を読み込む
        self.mode = mode
        self.config = Pit.get(self.mode)

    # ブラウジングモード設定
    def set_browser_mode(self, mode='normal'):
        try:
            if mode == 'normal':
                # 通常モードを有効にする
                self.driver = webdriver.Chrome('c:/driver/chromedriver.exe')
            elif mode == 'headless':
                # ヘッドレスモードを有効にする
                options = Options()
                options.add_argument('--headless')
                options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 6.1 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
                options.add_argument('--window-size=1280,4024')
                # ChromeのWebDriverオブジェクトを作成する。
                self.driver = webdriver.Chrome(executable_path='c:/driver/chromedriver.exe',chrome_options=options)
        except Exception as exc:
            print(exc)

    # mapps-core/forSurveyログイン
    def login(self, sub_domain=''):
        try:
            self.time = time
            if self.mode == 'dev4s':
                DOMAIN_MAPPS_CORE_PATH = 'https://' + self.config['domain_core']
                DOMAIN_4S_PATH = 'https://' + self.config['domain_4s']
                # 検証環境で Basic認証ページを通るときのパス
                parm = ('https://'
                    + str(self.config['basic_id'])
                    + ':' + str(self.config['basic_pw'])
                    + '@' + self.config['domain_core']
                    + '/')
                # MappsCore認証
                self.driver.get(parm)
                self.driver.find_element_by_name('email').send_keys(self.config['email'])
                self.driver.find_element_by_name('password').send_keys(self.config['password'])
                self.item_click('//input[starts-with(@class, "pure-button")]')
                self.driver.get(DOMAIN_MAPPS_CORE_PATH + '/menu')
                # forSurveyアクセス
                self.driver.get(DOMAIN_4S_PATH + '/admin/login/index.php?form=/admin/research/')
            elif self.mode == '4s26' or self.mode == '4s46' or self.mode == '4s90' or self.mode == '4s34' or self.mode == '4s23' or self.mode == '4s50' or self.mode == '4s19' or self.mode == '4s6' or self.mode == '4s42':
                DOMAIN_MAPPS_CORE_PATH = 'https://' + self.config['domain_core']
                DOMAIN_4S_PATH = 'https://' + self.config['domain_4s']
                # 商用環境は Basic認証ないからそのままのパス
                parm = ('https://' + self.config['domain_core'] + '/')
                # MappsCore認証
                self.driver.get(parm)
                self.driver.find_element_by_name('email').send_keys(self.config['email'])
                self.driver.find_element_by_name('password').send_keys(self.config['password'])
                self.item_click('//input[starts-with(@class, "pure-button")]')
                self.driver.get(DOMAIN_MAPPS_CORE_PATH + '/menu')
                # forSurveyアクセス
                self.driver.get(DOMAIN_4S_PATH + '/admin/login/index.php?form=/admin/research/')
            elif self.mode == 'gcp4s':
                # forSurveyアクセス
                DOMAIN_4S_PATH = 'http://' + str(sub_domain) + '.' + self.config['domain_4s']
                self.driver.get(DOMAIN_4S_PATH + '/admin/login/index2.php')
                self.driver.find_element_by_name('id').send_keys(self.config['email'])
                self.driver.find_element_by_name('pw').send_keys(self.config['password'])
                self.item_click('//td[starts-with(@class, "linkTypeA04")]')
        except Exception as exc:
            print(exc)

    # ブラウザ終了
    def browser_exit(self):
        try:
            # ブラウザを閉じる
            self.driver.close()
            self.driver.quit()
        except Exception as exc:
            print(exc)



    # [基本 - 共通]-------------------------------------------------------------------
    # 要素が表示されるまで待機
    def is_wait_until_element_displayed(self, xpath, timeout=500):
        try:
            count = 0
            while True:
                if len(self.driver.find_elements_by_xpath(xpath)) > 0 and self.driver.find_elements_by_xpath(xpath)[0].is_displayed():
                    return True
                    # break
                if count >= timeout:
                    print('[表示待機]-------------------------------')
                    print(xpath)
                    print('タイムアウト:' + str(count) + 'step')
                    return False
                count += 1
            print('[表示待機]-------------------------------')
            print(xpath)
            print('予想外の待ち:' + str(count) + 'step')
            return False
        except Exception as exc:
            print(exc)

    # 要素が消えるまで待機
    def is_wait_until_element_not_displayed(self, xpath, timeout=500):
        try:
            count = 0
            while True:
                if len(self.driver.find_elements_by_xpath(xpath)) > 0:
                    if self.driver.find_elements_by_xpath(xpath)[0].is_displayed() == False:
                            # self.time.sleep(0.5)
                            return True
                if count >= timeout:
                    print('[非表示待機]-------------------------------')
                    print(xpath)
                    print('タイムアウト:' + str(count) + 'step')
                    return False
                count += 1
            print('[非表示待機]-------------------------------')
            print(xpath)
            print('予想外の待ち:' + str(count) + 'step')
            return False
        except Exception as exc:
            print(exc)
            print('異常エラー')
            print(xpath)
            return True

    # ファイルを指定のディレクトリ内に保存(存在する時は上書き)
    def save_file_at_new_dir(self, new_dir_path, new_filename, new_file_content, mode='w'):
        try:
            os.makedirs(new_dir_path, exist_ok=True)
            with codecs.open(os.path.join(new_dir_path, new_filename), mode, encoding='utf-8') as f:
                # f.write(new_file_content)
                json.dump(new_file_content, f, ensure_ascii=False, indent=4, sort_keys=False, separators=(',', ': '))
        except Exception as exc:
            print(exc)

    # スクリーンショットを指定のディレクトリ内に保存(存在する時は上書き)
    def save_screenshot_at_new_dir(self, new_dir_path, new_filename):
        try:
            os.makedirs(new_dir_path, exist_ok=True)
            dir_path_name = str(new_dir_path) + '/' + str(new_filename)
            self.driver.save_screenshot(dir_path_name)
        except Exception as exc:
            print(exc)

    # [基本 - 入力]-------------------------------------------------------------------
    # DOM読み込み待機
    def dom_loading_wait(self, xpath, timeout=500):
        try:
            # self.time.sleep(0.5)
            if self.is_wait_until_element_displayed(xpath, timeout):
                if self.driver.find_elements_by_xpath(xpath)[0].is_enabled():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as exc:
            print(exc)

    # AJAX読み込み待機
    def ajax_loading_wait(self, xpath, timeout=500):
        try:
            xpath = '//div[@class="loading"]/img'
            if self.is_wait_until_element_not_displayed(xpath, timeout):
                pass
        except Exception as exc:
            print(exc)

    # 要素に文字を送信
    def item_send(self, xpath, value):
        try:
            if self.dom_loading_wait(xpath):
                # 前後の空白、改行は削除
                send_value = str(value).replace('\t', ' ').lstrip().rstrip()
                # 90番の終了ページメッセージ対策（空だと保存できない問題）
                if send_value == '':
                    send_value = value
                self.driver.find_element_by_xpath(xpath).send_keys(send_value)
        except Exception as exc:
            print(exc)

    # 要素の文字を削除
    def clear_text(self, xpath):
        try:
            if self.dom_loading_wait(xpath):
                self.driver.find_element_by_xpath(xpath).clear()
        except Exception as exc:
            print(exc)

    # 要素の文字を追記か上書きか判断して要素に文字を送信
    # mode -> i 文字を挿入（追加）
    # mode -> c 対象文字列を消して文字を挿入(つまり、変更)
    def item_send_text_appending_overwriting(self, xpath, value, mode='c'):
        try:
            if not value or mode == 'c':
                self.clear_text(xpath)
            self.item_send(xpath, value)
        except Exception as exc:
            print(exc)

    # [基本 - 選択]-------------------------------------------------------------------
    # 要素をクリック
    def item_click(self, xpath):
        try:
            if self.dom_loading_wait(xpath):
                self.driver.find_element_by_xpath(xpath).click()
        except Exception as exc:
            print(exc)

    # 要素をnameで検索してチェックボックスを全解除
    def clear_checkbox_all_by_name(self, value, key):
        try:
            xpath = '//input[starts-with(@name, "' + str(key) + '")]'
            if self.dom_loading_wait(xpath):
                elements = self.driver.find_elements_by_xpath(xpath)
                for element in elements:
                    if element.is_selected():
                        element.click()
        except Exception as exc:
            print(exc)

    # 要素をnameで検索して名称でプルダウンを選択
    def click_selectbox_by_name(self, value, key):
        try:
            xpath = '//select[@name="' + str(key) + '"]/option[text()="' + str(value) + '"]'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # 要素をnameで検索してvalueでプルダウンを選択
    def click_selectbox_by_value(self, value, key):
        try:
            xpath = '//select[@name="' + str(key) + '"]/option[@value="' + str(value) + '"]'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # 要素をidで検索してJavaScriptでスクロール
    def scroll_at_javascript_by_id(self, id, time=1):
        try:
            xpath = '//*[@id="' + str(id) + '"]'
            if self.dom_loading_wait(xpath):
                xpath = 'document.getElementById("' + str(id) + '").scrollIntoView(true)'
                self.driver.execute_script(xpath)
        except Exception as exc:
            print(exc)

    # [MYリサーチ一覧 - 選択]---------------------------------------------------------
    # MYリサーチ一覧 - アクセス
    def change_my_research(self):
        try:
            xpath = '//div[@class="navigationArea"]/div/ul/li[1]/a'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # MYリサーチ一覧 - 所属するグループ切り替え
    def change_select_group(self, value):
        try:
            self.click_selectbox_by_name(value, 'select_bumon_id')
        except Exception as exc:
            print(exc)

    # MYリサーチ一覧 - リサーチのアイコンメニューを押す
    def my_research_iconMenu_click(self, value):
        try:
            # 並び順はMYリサーチ一覧のリサーチのアイコンの並び順と合わせる
            menu = ['基本情報', 'アンケート画面編集', '回収状況と設定', 'データ集計', 'データ入出力', 'プレビュー', '配信追加']
            index = menu.index(value) + 1
            xpath = '//ul[starts-with(@class, "iconMenu")]/li[' + str(index) + ']/a'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # MYリサーチ一覧 - リサーチのアコーディオンを開く
    def research_accordion_open(self):
        try:
            xpath = '//a[starts-with(@id, "accordion-handler-")]'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # MYリサーチ一覧 - 検索オプションのアコーディオンを開く
    def click_search_button(self):
        try:
            xpath = '//span[@class="linkTypeA21"]/a'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # [MYリサーチ一覧 - 応用]---------------------------------------------------------
    # MYリサーチ一覧 - 検索オプション - キーワード検索
    def search_by_keyword(self, keyword):
        try:
            # MYリサーチ一覧アクセス
            self.change_my_research()
            # 検索アコーディオンopen
            xpath = '//div[@class="searchBoxTypeA01"]/form/dl/dt[@class="btn"]/a'
            self.item_click(xpath)
            # キーワード欄に入力
            xpath = '//input[@name="search_keyword"]'
            self.item_send(xpath, keyword)
            # 検索クリック
            self.click_search_button()
        except Exception as exc:
            print(exc)

    # MYリサーチ一覧 - 検索オプション - リサーチNo.検索
    def search_by_research_no(self, keyword):
        try:
            # MYリサーチ一覧アクセス
            self.change_my_research()
            # 検索アコーディオンopen
            xpath = '//div[@class="searchBoxTypeA01"]/form/dl/dt[@class="btn"]/a'
            self.item_click(xpath)
            # キーワード欄に入力
            xpath = '//input[@name="search_re_no"]'
            self.item_send(xpath, keyword)
            # 検索クリック
            self.click_search_button()
        except Exception as exc:
            print(exc)

    # [アンケート画面編集 - 選択]-----------------------------------------------------
    # アンケート画面編集 - 設問一括追加
    def open_add_confirm_window_click(self):
        try:
            xpath = '//ul[@class="listTypeB01"]/li[@class="linkTypeA15"]/a'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - 設問削除
    def open_delete_confirm_window_click(self):
        try:
            xpath = '//ul[@class="listTypeB01"]/li[@class="linkTypeA13"]/a'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - 設問の追加
    def add_question_last_click(self):
        try:
            xpath = '//tr[@class="utilityArea"]/td/ul/li[@class="linkTypeA11"]/a'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - 途中終了追加
    def open_add_end_page_window_click(self):
        try:
            xpath = '//ul[@class="listTypeB01"]/li[@class="linkTypeA16"]/a'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - 設問移動
    def open_move_confirm_window_click(self):
        try:
            xpath = '//ul[@class="listTypeB01"]/li[@class="linkTypeA14"]/a[@class="openwin"]'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - メッセージ編集
    def open_move_confirm_system_message_click(self):
        try:
            xpath = '//ul[@class="listTypeB01"]/li[@class="linkTypeA43"][2]/a[starts-with(@href, "javascript:openSystemMessage")]'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - ページ設定
    def open_move_confirm_setting_page_click(self):
        try:
            xpath = '//ul[@class="listTypeB01"]/li[@class="linkTypeA52"]/a[starts-with(@href, "javascript:openSettingPage")]'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # [設問編集 - 選択]---------------------------------------------------------------
    # 設問編集 - 名称で指定された設問タイプをクリック
    def change_question_type(self, value):
        try:
            xpath = '//div[@id="question_type"]/ul/li[text()="' + str(value) + '"]'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # [設問編集 - 応用]---------------------------------------------------------------
    # 設問編集 - 要素をnameで検索して文字を送信
    def item_send_element_key_by_name(self, element, value, keys, array, mode='c'):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                if isinstance(array_value, list):
                    count = -1
                    for array_value_child in array_value:
                        count += 1
                        key = keys[count]
                        xpath = '//' + str(element) + '[@name="' + str(key) + '"]'
                        self.item_send_text_appending_overwriting(xpath, array_value_child, mode)
                else:
                    xpath = '//' + str(element) + '[@name="' + str(keys) + '"]'
                    self.item_send_text_appending_overwriting(xpath, array_value, mode)
        except Exception as exc:
            print(exc)

    # 設問編集 - 要素をnameで検索して文字を送信（グループ対応版）
    def item_send_elements_key_by_name(self, element, value, keys, array, mode='c'):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                if isinstance(array_value, list):
                    pass
                else:
                    # グループ設定がONのとき
                    if array['グループ設定']['グループ設定する'] == 'on':
                        # 90番環境に「グループ数」は存在しないのでloop_countは[1]をセット
                        if self.mode == 'dev4s' or self.mode == '4s90':
                            loop_count = 1
                        else:
                            loop_count = int(array['グループ設定']['グループ数'])
                        for count in range(1, loop_count + 1):
                            key_value = keys.replace('1', str(count))
                            array_value = array.get(value)
                            if array_value is None:
                                pass
                            else:
                                self.item_send_element_key_by_name(element, value[loop_count - 1], key_value, array, mode)
                    else:
                        # グループ設定がOFFのとき
                        self.item_send_element_key_by_name(element, value, keys, array, mode)
        except Exception as exc:
            print(exc)

    # 設問編集 - グループ設定とグループ数の操作
    def edit_question_choice_group_by_name(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                if array_value['グループ設定する'] == 'on':
                    xpath = '//input[@name="' + str(key) + '"]'
                    self.item_click(xpath)
                    # 90番環境に「グループ数」は存在しないのでグループ数の設定は処理しない
                    if self.mode == 'dev4s' or self.mode == '4s90':
                        pass
                    else:
                        if key == 'choice[normal][useGroup]':
                            key = 'choice_num' 
                        elif key == 'choice[head][useGroup]':
                            key = 'choice_head_num' 
                        elif key == 'choice[side][useGroup]':
                            key = 'choice[side][blockNum]' 
                        self.click_selectbox_by_name(array_value['グループ数'], key)
                    # Ajax読み込み待機
                    self.ajax_loading_wait('//div[@class="loading"]/img')
        except Exception as exc:
            print(exc)

    # 設問編集 - グループ対応した設定（キャプション、選択肢）
    def edit_question_choice_text_group_by_name(self, element, value, key, array, q_no=[]):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                # グループ設定がONのとき
                if array['グループ設定']['グループ設定する'] == 'on':
                    # 90番環境に「グループ数」は存在しないのでloop_countは[1]をセット
                    if self.mode == 'dev4s' or self.mode == '4s90':
                        loop_count = 1
                    else:
                        loop_count = int(array['グループ設定']['グループ数'])
                    for count in range(1, loop_count + 1):
                        key_value = key.replace('1', str(count))
                        array_value_child = array_value[count-1]
                        # 選択肢パイピングの小文字大文字対策
                        if value.find('選択肢') >= 0:
                            array_value_child = self.convert_question_pipe(array_value_child)
                        if array_value_child is None:
                            pass
                        else:
                            xpath = '//' + str(element) + '[@name="' + str(key_value) + '"]'
                            self.clear_text(xpath)
                            self.item_send(xpath, array_value_child)
                else:
                    # グループ設定がOFFのとき
                    # 選択肢パイピングの小文字大文字対策
                    if value.find('選択肢') >= 0:
                        array_value = self.convert_question_pipe(array_value)
                        xpath = '//' + str(element) + '[@name="' + str(key) + '"]'
                        self.item_send_text_appending_overwriting(xpath, array_value, 'c')
                    else:
                        # 選択肢じゃない（キャプション）のときはパイピング変換処理しない
                        self.item_send_element_key_by_name(element, value, key, array, 'c')
        except Exception as exc:
            print(exc)

    # 設問編集 - プルダウン要素をnameで検索してリストの名称で項目を選択
    def item_pick_multiple_by_name(self, value, keys, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                if isinstance(array_value, list):
                    count = -1
                    for array_value_child in array_value:
                        count += 1
                        array_key = keys[count]
                        self.click_selectbox_by_name(array_value_child, array_key)
                else:
                    self.click_selectbox_by_name(array_value, keys)
        except Exception as exc:
            print(exc)

    # 設問編集 - プルダウン要素をvalueで検索してリストのvalue値で項目を選択　※MTXの絞り込み限定のメソッド
    def item_pick_multiple_by_value(self, value, keys, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                if isinstance(array_value, list):
                    count = -1
                    for array_value_child in array_value:
                        count += 1
                        array_key = keys[count]
                        xpath = '//select[@name="' + str(array_key) + '"]/option[@value="' + str(array_value_child) + '"]'
                        self.item_click(xpath)
                else:
                    xpath = '//select[@name="' + str(keys) + '"]/option[@value="' + str(array_value) + '"]'
                    self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - MTXの「絞り込み設定」をすべて解除
    def clear_matrix_mix_use_dynamic_filter_checkbox(self):
        try:
            xpath = '//input[starts-with(@name, "select_filter")]'
            if self.dom_loading_wait(xpath):
                elements = self.driver.find_elements_by_xpath(xpath)
                for element in elements:
                    element.click()
                xpath = '//input[@id="deleteFilter"]'
                self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - label要素をforで検索してlabelをクリック
    def item_check_by_label(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                xpath = '//label[@for="' + str(key) + '"]'
                self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - 名称がlabelで括られてないinputをクリック
    def choose_multiple_checkbox_not_label(self, value, key, array, element = 'parent::td[1]'):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                xpath = '//input[@name="' + str(key) + '"]/' + str(element)
                item_label = self.driver.find_element_by_xpath(xpath).text.split()
                for array_value_child in array_value:
                    xpath = '//input[@name="' + str(key) + '"]'
                    if self.dom_loading_wait(xpath):
                        elements = self.driver.find_elements_by_xpath(xpath)
                        comment = item_label.index(str(array_value_child))
                        if array_value[array_value_child] == 'on':
                            if elements[comment].is_selected() == False:
                                elements[comment].click()
                        elif array_value[array_value_child] == 'off':
                            if elements[comment].is_selected() == True:
                                elements[comment].click()
        except Exception as exc:
            print(exc)

    # 設問編集 - 名称がlabelで括られているinputをクリック　※labelで括られている時のnameはすべて名称が異なる
    def choose_multiple_checkbox(self, value, keys, array, element = 'label[@for='):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                for array_value_child in array_value:
                    key = keys.get(array_value_child)
                    xpath = '//' + str(element) + '"' + str(key) + '"]'
                    if self.dom_loading_wait(xpath):
                        element = self.driver.find_element_by_xpath(xpath)
                        if array_value[array_value_child] == 'on':
                            if element.is_selected() == False:
                                element.click()
                        elif array_value[array_value_child] == 'off':
                            if element.is_selected() == True:
                                element.click()
        except Exception as exc:
            print(exc)

    # 設問編集 - labelで括られたラジオボタン要素をnameで検索して設定項目をクリック
    def select_radio_button(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                xpath = '//input[@name="' + str(key) + '"]/following-sibling::label[text()="' + str(array_value) + '"]'
                self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - td内でlabel等で括られていないラジオボタン要素をnameで検索して設定項目をクリック
    def select_radio_button_by_name(self, value, key, array, element = 'parent::td[1]'):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                xpath = '//input[@name="' + str(key) + '"]/' + str(element)
                if self.dom_loading_wait(xpath):
                    item_label = self.driver.find_element_by_xpath(xpath).text.split()
                    # イレギュラー（いずれ分離したい）
                    if key == 'security' or key == 'replay':
                        item_label.pop(0)
                    xpath = '//input[@name="' + str(key) + '"]'
                    if self.dom_loading_wait(xpath):
                        elements = self.driver.find_elements_by_xpath(xpath)
                        comment = item_label.index(str(array_value))
                        elements[comment].click()
        except Exception as exc:
            print(exc)

    # 設問編集 - 登録情報設問の設問タイプ専用　※td内でlabel等で括られていないラジオボタン要素をnameで検索して設定項目をクリック
    def select_radio_button_by_attribute_type(self, value, key, array, element = 'parent::td[1]'):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                xpath = '//input[@name="' + str(key) + '"]/' + str(element)
                if self.dom_loading_wait(xpath):
                    item_label = self.driver.find_element_by_xpath(xpath).text.split()
                    xpath = '//input[@name="' + str(key) + '"]'
                    if self.is_wait_until_element_displayed(xpath):
                        elements = self.driver.find_elements_by_xpath(xpath)
                        comment = item_label.index(str(array_value))
                        elements[comment].click()
        except Exception as exc:
            print(exc)

    # 設問編集 - エラーチェック
    def set_error_check_process(self, value, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                count = 0
                for array_value_child in array_value:
                    count += 1
                    # 入力フォームをクリア
                    # self.clear_text_by_name('textarea', 'errorcheck_messages[' + str(count) + '][ja]')
                    # self.clear_text_by_name('textarea', 'errorcheck_syntaxes[' + str(count) + ']')
                    # 値をセット
                    self.item_send_element_key_by_name('textarea', 'メッセージ', 'errorcheck_messages[' + str(count) + '][ja]', array_value[array_value_child])
                    self.item_send_element_key_by_name('textarea', '条件式', 'errorcheck_syntaxes[' + str(count) + ']', array_value[array_value_child])
                    # 入力フォーム追加
                    xpath = '//tr[@class="tableMenu"]/th/div/div[2]/input[1]'
                    self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - MA(複数選択) - 選択個数制限の設定
    def selection_count_limit(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                if array_value == '制限なし':
                    xpath = '//input[@id="limit_off"]'
                    self.item_click(xpath)
                else:
                    count = -1
                    for array_value_child in array_value:
                        count += 1
                        if array_value_child == '制限あり':
                            xpath = '//input[@id="limit_on"]'
                            self.item_click(xpath)
                        elif count == 1:
                            self.item_send('//input[@name="limitNum"]', array_value_child)
                        elif count == 2:
                            xpath = '//select[@name="limitType"]/option[text()="' + str(array_value_child) + '"]'
                            self.item_click(xpath)
                        elif count == 3:
                            self.item_send('//input[@name="limitNum2"]', array_value_child)
        except Exception as exc:
            print(exc)

    # 設問編集 - 数値 - 合計値制限の設定
    def selection_total_count_limit(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                count = -1
                if array_value == '制限なし':
                    xpath = '//input[@name="' + str(key) + '"][@value="off"]'
                    self.item_click(xpath)
                else:
                    for array_value_child in array_value:
                        count += 1
                        if array_value_child == '制限あり':
                            xpath = '//input[@name="' + str(key) + '"][@value="on"]'
                            self.item_click(xpath)
                        elif count == 1:
                            self.item_send('//input[@name="limitTotalMin"]', array_value_child)
                        elif count == 2:
                            self.item_send('//input[@name="limitTotalMax"]', array_value_child)
        except Exception as exc:
            print(exc)

    # 設問編集 - 抽選機能の設定
    def set_lottery_count(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                if isinstance(array_value, list):
                    xpath = '//input[@name="' + str(key) + '"]/parent::td'
                    if self.dom_loading_wait(xpath):
                        item_list = self.driver.find_element_by_xpath(xpath).text.split()
                        xpath = '//input[@name="' + str(key) + '"]'
                        if self.dom_loading_wait(xpath):
                            elements = self.driver.find_elements_by_xpath(xpath)
                            comment = item_list.index(str(array_value[0]))
                            elements[comment].click()
                        xpath = '//input[@name="lotteryCount"]'
                        if self.dom_loading_wait(xpath):
                            self.clear_text(xpath)
                            self.item_send(xpath, array_value[1])
                        self.driver.find_element_by_xpath(xpath).send_keys(Keys.TAB)
                else:
                    self.select_radio_button_by_name(array_value, 'lottery', array)
        except Exception as exc:
            print(exc)

    # 設問編集 - 打切り連動設定
    def set_gate_interlock(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                self.clear_checkbox_all_by_name(value, str(key))
                if array_value == 'on':
                    xpath = '//input[@name="' + str(key) + '"]'
                    self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - COMPの自動リダイレクト設定
    def set_question_redirect(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                research_type = self.get_research_type_of_edit_question()
                # list型なら「設定あり」と判断する
                if isinstance(array_value, list):
                    if research_type == 'クローズドモニタ' or research_type == 'モニタプラス（Mapps Panel）':
                        # クローズドは「指定する/しない」ラジオボタンが無いのでボタン処理だけスキップ
                        pass
                    else:
                        # ラジオボタン選択
                        xpath = '//input[@name="' + str(key) + '"][@value="1"]'
                        if self.dom_loading_wait(xpath):
                            element = self.driver.find_element_by_xpath(xpath)
                            element.click()
                    # 経過秒
                    xpath = '//input[@name="redirect_timer"]'
                    if self.dom_loading_wait(xpath):
                        self.clear_text(xpath)
                        self.item_send(xpath, array_value[1])
                    # URL
                    xpath = '//input[@name="redirect_url"]'
                    if self.dom_loading_wait(xpath):
                        self.clear_text(xpath)
                        self.item_send(xpath, array_value[2])
                # なしに設定する
                else:
                    if research_type == 'クローズドモニタ' or research_type == 'モニタプラス（Mapps Panel）':
                        # クローズドは「指定する/しない」ラジオボタンが無いのでボタン処理だけスキップ
                        pass
                    else:
                        # ラジオボタン選択
                        xpath = '//input[@name="' + str(key) + '"][@value="0"]'
                        if self.dom_loading_wait(xpath):
                            element = self.driver.find_element_by_xpath(xpath)
                            element.click()
        except Exception as exc:
            print(exc)

    # 設問編集 - COMPの外部連結　終了通知API設定
    def set_question_redirect_api(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                research_type = self.get_research_type_of_edit_question()
                # list型なら「設定あり」と判断する
                if isinstance(array_value, list):
                    if research_type == 'クローズドモニタ' or research_type == 'モニタプラス（Mapps Panel）':
                        # クローズドは「指定する/しない」ラジオボタンが無いのでボタン処理だけスキップ
                        pass
                    else:
                        # ラジオボタン選択
                        xpath = '//input[@name="' + str(key) + '"][@value="1"]'
                        if self.dom_loading_wait(xpath):
                            element = self.driver.find_element_by_xpath(xpath)
                            element.click()
                    # URL
                    xpath = '//input[@name="api_url"]'
                    if self.dom_loading_wait(xpath):
                        self.clear_text(xpath)
                        self.item_send(xpath, array_value[1])
                # なしに設定する
                else:
                    if research_type == 'クローズドモニタ' or research_type == 'モニタプラス（Mapps Panel）':
                        # クローズドは「指定する/しない」ラジオボタンが無いのでボタン処理だけスキップ
                        pass
                    else:
                        # ラジオボタン選択
                        xpath = '//input[@name="' + str(key) + '"][@value="0"]'
                        if self.dom_loading_wait(xpath):
                            element = self.driver.find_element_by_xpath(xpath)
                            element.click()
        except Exception as exc:
            print(exc)

    # 設問編集 - 目的のページ(設問)へ移動する
    def jump_to_target_pages(self, page, quid=''):
        try:
            if page.find('START') == -1 and page.find('COMP') == -1 and page.find('END') == -1 and page.find('GATE') == -1:
                self.scroll_at_javascript_by_id(str(page))
            if len(quid) == 0:
                xpath = '//td[@class="pageNo"]/a[text()="' + str(page) + '"]'
            else:
                xpath = '//td[@class="pageNo"]/a[text()="' + str(page) + '"][contains(@href, ' + str(quid) + ')]'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - 画面編集に戻る
    def back_to_screen_edit(self):
        try:
            url_file_path = self.driver.current_url
            if url_file_path.find('editQuestion.php') != -1 or url_file_path.find('editStartPage.php') != -1 or url_file_path.find('editEndPage.php') != -1:
                self.scroll_at_javascript_by_id('contents')
                xpath = '//ul[@class="listTypeB01"][1]/li[@class="linkTypeA11"][1]/div[@class="linkTypeA51"]/a'
                self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - プロフィール専用
    def item_send_element_key_by_profile(self, element, value, keys, array, eq, mode='c'):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                count = 0
                for array_value_child in array_value:
                    if count == 0:
                        xpath = '//' + str(element) + '[@name="' + str(keys[0]) + '"]'
                        self.item_send_text_appending_overwriting(xpath, array_value_child, mode)
                    else:
                        # チェックを外す
                        xpath = '//' + str(element) + '[@name="' + str(keys[count]) + '"]'
                        if self.dom_loading_wait(xpath):
                            if self.driver.find_elements_by_xpath(xpath)[eq].is_selected():
                                self.driver.find_elements_by_xpath(xpath)[eq].click()
                        if array_value_child == 'on':
                            # チェックを付ける
                            xpath = '//' + str(element) + '[@name="' + str(keys[count]) + '"]'
                            if self.dom_loading_wait(xpath):
                                self.driver.find_elements_by_xpath(xpath)[eq].click()
                    count += 1
        except Exception as exc:
            print(exc)

    # 設問編集 - 保存する
    def question_save(self):
        try:
            xpath = '//ul[@class="listTypeQuestion"]/li[@class="linkTypeA03"]/a'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - 設定情報をキャプチャ
    def question_display_screenshot_by_page(self, page, array, dirpath='./', filename=''):
        try:
            if array.get('ディレクトリ名') is None:
                print('[エラー] 画像キャプチャに必要なディレクトリ名が存在しません。')
            else:
                dir_path = array.get('ディレクトリ名')
                if filename == '':
                    new_file_name = str(page) + '.png'
                else:
                    new_file_name = str(filename) + '.png'
                self.save_screenshot_at_new_dir(str(dir_path), new_file_name)
        except Exception as exc:
            print(exc)

    # 画面のURLを取得して同じかチェックする
    def check_browser_path(self, name):
        try:
            result = False
            url_file_path = self.driver.current_url
            if name == 'MYリサーチ一覧':
                # MYリサーチ一覧
                xpath = '//div[@id="project_button"]'
                if self.dom_loading_wait(xpath):
                    check_path_1 = '/admin/research/'
                    check_path_2 = '/admin/research/index.php'
                    if url_file_path.find(check_path_1) == -1 and url_file_path.find(check_path_2) == -1:
                        result = False
                    else:
                        result = True
            elif name == 'リサーチ新規作成':
                # リサーチ新規作成（作成/確認）
                check_path = '/admin/research/regResearch.php'
                if url_file_path.find(check_path) == -1:
                    result = False
                else:
                    result = True
            elif name == '基本情報':
                # 基本情報（閲覧）
                check_path_1 = '/admin/research/viewResearch.php'
                # 基本情報（編集/確認）
                check_path_2 = '/admin/research/editResearch.php'
                if url_file_path.find(check_path_1) == -1 and url_file_path.find(check_path_2) == -1:
                    result = False
                else:
                    result = True
            elif name == 'アンケート画面編集':
                # アンケート画面編集
                xpath = '//tr[@class="questions-list"]'
                if self.dom_loading_wait(xpath):
                    check_path = '/admin/research/enquete/editEnquete.php'
                    if url_file_path.find(check_path) == -1:
                        result = False
                    else:
                        result = True
            elif name == '設問編集':
                # 設問編集
                check_path = '/admin/research/enquete/editQuestion.php'
                if url_file_path.find(check_path) == -1:
                    result = False
                else:
                    result = True
            return result
        except Exception as exc:
            print(exc)

    # ランダムが引き継ぎかどうかチェックする
    def check_normal_random_decision(self, value):
        try:
            if value.find('on/') == -1:
                return True 
            else:
                return False
        except Exception as exc:
            print(exc)

    # パイピングの設問Noの小文字大文字対策
    def convert_question_pipe(self, value):
        try:
            item_values = value.splitlines()
            new_item_values = []
            for item_value in item_values:
                # 応急処置（設問Noは大文字がほとんどなのでパイピングの設問Noは大文字に置換）
                if item_value.find('<pipe') >= 0:
                    item_value = item_value.split('<pipe')[0] + '<pipe' + item_value.split('<pipe')[1].upper()
                    # 表頭、表側などの設問No以外の文字は小文字に戻す
                    item_value = item_value.replace('.ST', '.st')
                    item_value = item_value.replace('.HT', '.ht')
                    item_value = item_value.replace('.C', '.c')
                    item_value = item_value.replace('.S', '.s')
                    item_value = item_value.replace('.T', '.t')
                    item_value = item_value.replace('.NUM', '.num')
                    item_value = item_value.replace('ALL_ON', 'all_on')
                    item_value = item_value.replace('ALL_OFF', 'all_off')
                    item_value = item_value.replace('ANY_ON', 'any_on')
                    item_value = item_value.replace('ANY_OFF', 'any_off')
                    item_value = item_value.replace('ON', 'on')
                    item_value = item_value.replace('OFF', 'off')
                    new_item_values.append(item_value)
                else:
                    new_item_values.append(item_value)
            array_value = '\n'.join(new_item_values)
            return array_value
        except Exception as exc:
            print(exc)

    # sizeタグを埋め込んで作成可能な形式に加工
    def convert_size_tag(self, value):
        try:
            size_tag = '<size=10><must>'
            # ()、[]をsizeタグに変換
            # convert_value = re.sub('(\[|\(|［|（)+( |　)+(\]|\)|］|）)+' , size_tag, str(value))
            convert_value = re.sub(r'(\[|\(|［|（)+( |　)+(\]|\)|］|）)+' , size_tag, str(value))
            return convert_value
        except Exception as exc:
            print(exc)

    # [応用(操作) - 入力]---------------------------------------------------------
    # リサーチ新規作成（プロジェクトを検索してヒットしない場合は新規作成）
    def create_new_research_by_group(self, project, research):
        try:
            self.change_my_research()
            self.search_by_keyword(project['プロジェクト名'])
            if self.get_number_of_displayed_project() == 0:
                self.create_new_project(project)
            else:
                # 検索結果の１番上のプロジェクトの右端の「リサーチ新規作成」アイコンクリック
                # 90番と従来版でマイページ一覧の表示がちがう対応（アコーディオン）
                xpath = '//label[starts-with(@for, "rgrID_")]'
                if self.dom_loading_wait(xpath):
                    elements = self.driver.find_elements_by_xpath(xpath)
                    if len(elements) == 1:
                        # 従来版
                        pass
                    else:
                        # 90番のアコーディオン
                        xpath = '//label[starts-with(@for, "rgrID_")][2]'
                        self.item_click(xpath)
            self.create_new_research(research, project['プロジェクト名'])
        except Exception as exc:
            print(exc)

    # プロジェクト新規作成
    def create_new_project(self, array):
        try:
            self.item_click('//a[@id="create_new_project"]')
            self.item_send_element_key_by_name('input', 'プロジェクトNo', 'projectNo', array)
            self.item_send_element_key_by_name('input', 'プロジェクト名', 'projectName', array)
            # self.item_send_element_key_by_name('プロジェクトメンバー', 'project_member ※クラス名', array)　※未実装
            self.item_send_element_key_by_name('input', 'クライアント名', 'clientName', array)
            self.item_send_element_key_by_name('input', '期限日時', 'dueDate', array)
            self.item_send_element_key_by_name('textarea', '調査概要', 'projectOutline', array)
            self.item_click('//input[@name="save"]')
            self.time.sleep(1)
            Alert(self.driver).accept()
        except Exception as exc:
            print(exc)

    # リサーチ新規作成
    def create_new_research(self, array, name = ''):
        try:
            url_file_path = self.driver.current_url
            if url_file_path.find('regResearch.php') == -1:
                xpath = '//form[@name="reg_research"]/li/a[contains(@href, "regResearch.php")]'
                self.item_click(xpath)
            if url_file_path.find('intage') == -1:
                pass
            else:
                # 業務情報
                self.item_pick_multiple_by_name('サービス種別', 'intage_service_type', array)
                self.item_pick_multiple_by_name('モニター利用区分', ['intage_monitor_type', 'intage_research_type'], array)
                self.item_pick_multiple_by_name('アンケート回答ドメイン', 'intage_open_domain', array)
                self.clear_checkbox_all_by_name('デバイス', 'intage_device_types[]')
                self.choose_multiple_checkbox('デバイス', {'スマートフォン（SP）＆PC': 'intage_device_types_1', 'フィーチャーフォン（iモード）': 'intage_device_types_2'}, array)
                self.select_radio_button('メール配信有無', 'intage_use_mail_delivery', array)
                self.select_radio_button('アンケート一覧【表示】有無', 'intage_is_in_survey_list', array)
                self.select_radio_button('アンケート一覧【優先】有無', 'intage_survey_list_priority', array)
                self.select_radio_button('案内ページ有無', 'intage_use_guide_page', array)
                self.select_radio_button('開始ページの有無', 'intage_use_start_page', array)
                self.item_send_element_key_by_name('input', 'dポイントクラブ冒頭文言', 'intage_additional_title_words', array)
                self.item_send_element_key_by_name('input', 'アンケート設問カウント', ['intage_question_count_sc', 'intage_question_count_main'], array)
            # 基本情報
            array['プロジェクトNo/プロジェクト名'] = array['プロジェクトNo'] + ' ' + array['プロジェクト名']
            self.item_pick_multiple_by_name('プロジェクトNo/プロジェクト名', 'rgr_id', array)
            self.item_send_element_key_by_name('input', 'アンケートタイトル', 're_public_title', array)
            self.item_send_element_key_by_name('input', '内部管理メモ', 're_title', array)
            self.item_pick_multiple_by_name('リサーチ種別', ['re_rtm_id', 're_sub_type'], array)
            # self.clear_checkbox_all_by_name('端末', 're_device_multi[]')
            self.choose_multiple_checkbox_not_label('端末', 're_device_multi[]', array)
            # self.clear_checkbox_all_by_name('回答回収連動', 're_auto_close')
            # self.clear_checkbox_all_by_name('回答回収連動', 're_response_full_notification')
            # self.choose_multiple_checkbox('回答回収連動', {'GATEの回収目標数に達したらSCRの回答受付も終了': 're_auto_close', '回収目標数に達したらメールでお知らせ': 're_response_full_notification'}, array)
            # self.select_radio_button('回答端末情報(UserAgent)', 're_reuse_useragent', array)
            self.select_radio_button('表示および操作権限', 're_personal_use', array)
            self.select_radio_button('自動改行', 'auto_new_line', array)
            # URL
            self.item_send_element_key_by_name('input', '告知 URL', 're_announce_url', array)
            # オープンリサーチ設定
            self.choose_multiple_checkbox('重複排他', {'Cookie（モバイルでは端末識別番号）': 're_duplicate_check_id_cb', 'IPアドレス': 're_duplicate_check_ip_enabled_cb'}, array)
            # アンケート画面基本設定
            self.select_radio_button('作成方法', 'enqCreateType', array)
            self.item_pick_multiple_by_name('テンプレートデザイン', 're_designtpl_code', array)
            self.select_radio_button('回答者属性ファイル', 're_is_reg_respondent_attr', array)
            self.item_pick_multiple_by_name('進捗バー', 're_epm_id', array)
            # ここに設問Noのあるが、未開発
            self.item_pick_multiple_by_name('戻るボタン', 're_back_button_id', array)
            self.item_pick_multiple_by_name('最終確認ページ', 're_last_confirm_id', array)
            # 確認画面へ
            xpath = '//div[@class="sectionLv2"]/p[@class="linkTypeB01"]/a[@href="javascript: check(\'reg\');"]'
            self.item_click(xpath)
            # javascriptを実行してページの最下部へ移動
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # 保存
            xpath = '//div[@class="sectionLv2"]/div[@class="linkTypeA03"]/a'
            self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # 設問を編集（新規）
    def edit_new_question(self, page, array, options=[''], prev_page=''):
        try:
            # スクロール
            self.scroll_at_javascript_by_id('questions')
            # 設問を追加するかどうかの判断
            if self.get_count_unset_questions() == 0:
                if page == 'P1':
                    # P1 の場合（STARTに遷移して「設問の追加」を押下
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    self.add_question_last_click()
                    self.back_to_screen_edit()
                else:
                    # P2 以降の場合（「設問一括追加」で該当ページを追加
                    if page.find('P') == 0:
                        # 1つ前の設問のＱナンバーを抽出
                        xpath = '//td[@class="pageNo"]/a[text()="' + str(prev_page) + '"]'
                        q_number = self.driver.find_element_by_xpath(xpath).get_attribute('href')
                        q_number = q_number[29:33]
                        # 設問一括追加 - 指定の設問の下に設問を1つ追加する
                        self.sub_window_operation('設問一括追加', ['//select[@name="qu_id"]/option[starts-with(@value, "' + str(q_number) + '")]', '//input[starts-with(@value,"追加する")]'])
            if (page.find('END') >= 0 or page.find('GATE') >= 0) and len(prev_page) != 0:
                # END/GATE の場合（「途中終了追加」でENDページを追加
                self.sub_window_operation('途中終了追加', ['//select[@name="pg_id"]/option[contains(text(), "' + str(prev_page) + '")]', '//input[starts-with(@value,"追加する")]'])
            # 編集ページへ遷移
            self.jump_to_target_pages(page)
            if page.find('P') == 0:
                # 現在選択中設問タイプ
                self.change_question_type(array['設問タイプ'])
                # 設問編集
                if array['設問タイプ'] == 'SA(単一選択)':
                    self.edit_new_question_by_single_answer(array)
                elif array['設問タイプ'] == 'MA(複数選択)':
                    self.edit_new_question_by_multi_answer(array)
                elif array['設問タイプ'] == '数値':
                    self.edit_new_question_by_number_answer(array)
                elif array['設問タイプ'] == '隠し設問SA':
                    self.edit_new_question_by_hidden_single_answer(array)
                elif array['設問タイプ'] == '自由記入短文':
                    self.edit_new_question_by_freeshort_answer(array)
                elif array['設問タイプ'] == '自由記入長文':
                    self.edit_new_question_by_freelong_answer(array)
                elif array['設問タイプ'] == '隠し設問MA':
                    self.edit_new_question_by_hidden_multi_answer(array)
                elif array['設問タイプ'] == '画像アップロード':
                    self.edit_new_question_by_image_upload_answer(array)
                elif array['設問タイプ'] == 'マトリクスSA':
                    self.edit_new_question_by_matrix_single_answer(array)
                elif array['設問タイプ'] == 'マトリクスMA':
                    self.edit_new_question_by_matrix_multi_answer(array)
                elif array['設問タイプ'] == 'マトリクス混合':
                    self.edit_new_question_by_matrix_mix_answer(array)
                elif array['設問タイプ'] == '文章・画像のみ':
                    self.edit_new_question_by_through_answer(array)
                elif array['設問タイプ'] == 'プロフィール':
                    self.edit_new_question_by_profile_answer(array)
                elif array['設問タイプ'] == 'SD法':
                    self.edit_new_question_by_matrix_sd_answer(array)
                elif array['設問タイプ'] == '登録情報設問':
                    self.edit_new_question_by_attribute_answer(array)
                elif array['設問タイプ'] == '外部連携設問':
                    self.edit_new_question_by_post_external_answer(array)
            elif page.find('START') >= 0:
                self.edit_new_question_by_start_page_answer(array)
            elif page.find('COMP') >= 0 or page.find('END') >= 0 or page.find('GATE') >= 0:
                self.edit_new_question_by_end_page_answer(array)
            # 保存する
            self.question_save()
            # 必須回答にしない場合のアラート対応
            if '必須入力チェック' in array.keys():
                if array['必須入力チェック'] in '必須にしない':
                    self.time.sleep(1)
                    Alert(self.driver).accept()
            # 画面編集に戻る
            # self.back_to_screen_edit()
            xpath = '//form[@name="formAction"]/li[2]/a'
            self.item_click(xpath)
            # # 開いた設問単体プレビューを閉じる
            # if page.find('P') == 0:
            #     # 設問のＱナンバーを抽出
            #     xpath = '//td[@class="pageNo"]/a[text()="' + str(page) + '"]'
            #     if self.is_wait_until_element_displayed(xpath):
            #         if self.driver.find_elements_by_xpath(xpath)[0].is_enabled():
            #             q_number = self.driver.find_element_by_xpath(xpath).get_attribute('href')
            #             q_number = q_number[29:33]
            #     xpath = '//div[@id="preview_' + str(q_number) + '"]/ul[@class="listTypeB01"]/li[@class="linkTypeA14"]/a'
            #     self.item_click(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - ランダムのグループ対応版
    def edit_question_randomize_by_group(self, value, key, array, element = 'parent::td[1]'):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                # ランダマイズとグループランダマイズの設定
                if value == 'ランダマイズ' or value == '選択肢ランダマイズ':
                    # グループ設定がONのとき
                    if array['グループ設定']['グループ設定する'] == 'on':
                        # 90番環境に「グループ設定」時の「ランダマイズ」は存在しないので処理をスキップ
                        if self.mode == 'dev4s' or self.mode == '4s90':
                            pass
                        else:
                            loop_count = int(array['グループ設定']['グループ数'])
                            for count in range(1, loop_count + 1):
                                key_value = key.replace('1', str(count))
                                array_value = array[value][count-1]
                                if array_value is None:
                                    pass
                                else:
                                    # 表示順を引き継ぐのとき『表示順を引き継ぐ』にチェックをつけて引き継ぎ順を選ぶ
                                    if self.check_normal_random_decision(array_value) == False:
                                        key_value_child = key_value.replace('orderlogic', 'useOrderRef')
                                        xpath = '//input[@name="' + str(key_value_child) + '"]'
                                        self.item_click(xpath)
                                        array_value = array_value.replace('on/', '')
                                        key_value_child = key_value.replace('orderlogic', 'orderRef')
                                        self.click_selectbox_by_name(array_value, key_value_child)
                                    else:
                                        xpath = '//input[@name="' + str(key_value) + '"]/' + str(element)
                                        if self.dom_loading_wait(xpath):
                                            item_label = self.driver.find_element_by_xpath(xpath).text.split()
                                            xpath = '//input[@name="' + str(key_value) + '"]'
                                            if self.dom_loading_wait(xpath):
                                                elements = self.driver.find_elements_by_xpath(xpath)
                                                comment = item_label.index(str(array_value))
                                                elements[comment].click()
                    else:
                        # グループ設定がOFFのとき
                        # 表示順を引き継ぐのとき『表示順を引き継ぐ』にチェックをつけて引き継ぎ順を選ぶ
                        if self.check_normal_random_decision(array_value) == False:
                            key_value = key.replace('orderlogic', 'useOrderRef')
                            xpath = '//input[@name="' + str(key_value) + '"]'
                            self.item_click(xpath)
                            array_value = array_value.replace('on/', '')
                            key_value = key.replace('orderlogic', 'orderRef')
                            self.click_selectbox_by_name(array_value, key_value)
                        else:
                            xpath = '//input[@name="' + str(key) + '"]/' + str(element)
                            if self.dom_loading_wait(xpath):
                                item_label = self.driver.find_element_by_xpath(xpath).text.split()
                                xpath = '//input[@name="' + str(key) + '"]'
                                if self.dom_loading_wait(xpath):
                                    elements = self.driver.find_elements_by_xpath(xpath)
                                    comment = item_label.index(str(array_value))
                                    elements[comment].click()
                elif value == 'グループランダマイズ':
                    # 表示順を引き継ぐのとき『表示順を引き継ぐ』にチェックをつけて引き継ぎ順を選ぶ
                    if self.check_normal_random_decision(array_value) == False:
                        key_value = key.replace('orderlogic', 'useOrderRef')
                        xpath = '//input[@name="' + str(key_value) + '"]'
                        self.item_click(xpath)
                        array_value = array_value.replace('on/', '')
                        key_value = key.replace('orderlogic', 'orderRef')
                        self.click_selectbox_by_name(array_value, key_value)
                    else:
                        xpath = '//input[@name="' + str(key) + '"]/' + str(element)
                        if self.dom_loading_wait(xpath):
                            item_label = self.driver.find_element_by_xpath(xpath).text.split()
                            xpath = '//input[@name="' + str(key) + '"]'
                            if self.dom_loading_wait(xpath):
                                elements = self.driver.find_elements_by_xpath(xpath)
                                comment = item_label.index(str(array_value))
                                elements[comment].click()
        except Exception as exc:
            print(exc)

    # 設問編集 - i-タイル設定作成
    def edit_question_by_itile(self, value, key, array, element):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                # 作成予定のQナンバーの取得
                quid = array['Qナンバー']
                # 作成予定の設問タイプの取得
                question_type = array['設問タイプ']
                # i-タイル設定
                self.select_radio_button_by_name(value, key, array, element)
                array[value] = self.get_item_selected_radio_of_label(key)
                if array[value] == '利用する':
                    value = 'i-タイル設定詳細'
                    if question_type == 'SA(単一選択)':
                        self.select_radio_button_by_name('ページ自動遷移', 'i_tile[questions][' + str(quid) + '][auto_next]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('ラジオボタン表示', 'i_tile[questions][' + str(quid) + '][radio_display]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('テキストレイアウト', 'i_tile[questions][' + str(quid) + '][text_align]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('付属テキスト配置', 'i_tile[questions][' + str(quid) + '][text_place]', array[value], element='ancestor::td[1]')
                        self.item_send_element_key_by_name('input', '高さ', 'i_tile[questions][' + str(quid) + '][height]', array[value])
                        self.item_send_element_key_by_name('input', '幅', 'i_tile[questions][' + str(quid) + '][width]', array[value])
                        self.item_send_element_key_by_name('input', '回答の列数', 'i_tile[questions][' + str(quid) + '][column]', array[value])
                        self.click_selectbox_by_name(array[value]['並び順'], '//select[@name="i_tile[questions][' + str(quid) + '][alignment]"]')
                    elif question_type == 'MA(複数選択)':
                        self.select_radio_button_by_name('チェックボックス表示', 'i_tile[questions][' + str(quid) + '][checkbox_display]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('テキストレイアウト', 'i_tile[questions][' + str(quid) + '][text_align]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('付属テキスト配置', 'i_tile[questions][' + str(quid) + '][text_place]', array[value], element='ancestor::td[1]')
                        self.item_send_element_key_by_name('input', '高さ', 'i_tile[questions][' + str(quid) + '][height]', array[value])
                        self.item_send_element_key_by_name('input', '幅', 'i_tile[questions][' + str(quid) + '][width]', array[value])
                        self.item_send_element_key_by_name('input', '回答の列数', 'i_tile[questions][' + str(quid) + '][column]', array[value])
                        self.click_selectbox_by_name(array[value]['並び順'], '//select[@name="i_tile[questions][' + str(quid) + '][alignment]"]')
                    elif question_type == 'マトリクスSA':
                        self.select_radio_button_by_name('ページ自動遷移', 'i_tile[questions][' + str(quid) + '][auto_next]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('ラジオボタン表示', 'i_tile[questions][' + str(quid) + '][radio_display]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('戻るボタン表示', 'i_tile[questions][' + str(quid) + '][display_back_btn]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('次を表示ボタン', 'i_tile[questions][' + str(quid) + '][display_next_btn]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('テキストレイアウト', 'i_tile[questions][' + str(quid) + '][text_align]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('付属テキスト配置', 'i_tile[questions][' + str(quid) + '][text_place]', array[value], element='ancestor::td[1]')
                        self.item_send_element_key_by_name('input', '高さ', 'i_tile[questions][' + str(quid) + '][height]', array[value])
                        self.item_send_element_key_by_name('input', '幅', 'i_tile[questions][' + str(quid) + '][width]', array[value])
                        self.item_send_element_key_by_name('input', '回答の列数', 'i_tile[questions][' + str(quid) + '][column]', array[value])
                        self.click_selectbox_by_name(array[value]['並び順'], '//select[@name="i_tile[questions][' + str(quid) + '][alignment]"]')
                    elif question_type == 'マトリクスMA':
                        self.select_radio_button_by_name('ページ自動遷移', 'i_tile[questions][' + str(quid) + '][auto_next]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('チェックボックス表示', 'i_tile[questions][' + str(quid) + '][checkbox_display]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('戻るボタン表示', 'i_tile[questions][' + str(quid) + '][display_back_btn]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('テキストレイアウト', 'i_tile[questions][' + str(quid) + '][text_align]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('付属テキスト配置', 'i_tile[questions][' + str(quid) + '][text_place]', array[value], element='ancestor::td[1]')
                        self.item_send_element_key_by_name('input', '高さ', 'i_tile[questions][' + str(quid) + '][height]', array[value])
                        self.item_send_element_key_by_name('input', '幅', 'i_tile[questions][' + str(quid) + '][width]', array[value])
                        self.item_send_element_key_by_name('input', '回答の列数', 'i_tile[questions][' + str(quid) + '][column]', array[value])
                        self.click_selectbox_by_name(array[value]['並び順'], '//select[@name="i_tile[questions][' + str(quid) + '][alignment]"]')
                    elif question_type == 'マトリクス混合':
                        self.select_radio_button_by_name('ページ自動遷移', 'i_tile[questions][' + str(quid) + '][auto_next]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('ラジオボタン表示', 'i_tile[questions][' + str(quid) + '][radio_display]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('チェックボックス表示', 'i_tile[questions][' + str(quid) + '][checkbox_display]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('戻るボタン表示', 'i_tile[questions][' + str(quid) + '][display_back_btn]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('次を表示ボタン', 'i_tile[questions][' + str(quid) + '][display_next_btn]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('テキストレイアウト', 'i_tile[questions][' + str(quid) + '][text_align]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('付属テキスト配置', 'i_tile[questions][' + str(quid) + '][text_place]', array[value], element='ancestor::td[1]')
                        self.item_send_element_key_by_name('input', '高さ', 'i_tile[questions][' + str(quid) + '][height]', array[value])
                        self.item_send_element_key_by_name('input', '幅', 'i_tile[questions][' + str(quid) + '][width]', array[value])
                        self.item_send_element_key_by_name('input', '回答の列数', 'i_tile[questions][' + str(quid) + '][column]', array[value])
                        self.click_selectbox_by_name(array[value]['並び順'], '//select[@name="i_tile[questions][' + str(quid) + '][alignment]"]')
                    elif question_type == 'SD法':
                        self.select_radio_button_by_name('ページ自動遷移', 'i_tile[questions][' + str(quid) + '][auto_next]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('ラジオボタン表示', 'i_tile[questions][' + str(quid) + '][radio_display]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('戻るボタン表示', 'i_tile[questions][' + str(quid) + '][display_back_btn]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('次を表示ボタン', 'i_tile[questions][' + str(quid) + '][display_next_btn]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('テキストレイアウト', 'i_tile[questions][' + str(quid) + '][text_align]', array[value], element='ancestor::td[1]')
                        self.select_radio_button_by_name('付属テキスト配置', 'i_tile[questions][' + str(quid) + '][text_place]', array[value], element='ancestor::td[1]')
                        self.item_send_element_key_by_name('input', '高さ', 'i_tile[questions][' + str(quid) + '][height]', array[value])
                        self.item_send_element_key_by_name('input', '幅', 'i_tile[questions][' + str(quid) + '][width]', array[value])
                        self.item_send_element_key_by_name('input', '回答の列数', 'i_tile[questions][' + str(quid) + '][column]', array[value])
                        self.click_selectbox_by_name(array[value]['並び順'], '//select[@name="i_tile[questions][' + str(quid) + '][alignment]"]')
        except Exception as exc:
            print(exc)

    # 設問編集 - 画像作成
    def edit_question_by_image_setting(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                if array[value] != '表示しない':
                    self.select_radio_button_by_name('表示位置', 'insertImage', array['画像詳細設定'], element='ancestor::tr[1]')
                    self.select_radio_button_by_name('画像寄せ', 'alignImage', array['画像詳細設定'], element='ancestor::tr[1]')
                    self.select_radio_button_by_name('並び順', 'alignImageHorVer', array['画像詳細設定'], element='ancestor::tr[1]')
                    self.item_send_element_key_by_name('textarea', '上段コメント', 'upper_comment[ja]', array['画像詳細設定'])
                    # キャプション
                    if array['画像詳細設定'].get('キャプション') is None:
                        pass
                    else:
                        self.item_send_text_appending_overwriting('//textarea[@name="caption1[ja]"]', array['画像詳細設定']['キャプション'][0], 'c')
                        self.item_send_text_appending_overwriting('//textarea[@name="caption2[ja]"]', array['画像詳細設定']['キャプション'][1], 'c')
                        self.item_send_text_appending_overwriting('//textarea[@name="caption3[ja]"]', array['画像詳細設定']['キャプション'][2], 'c')
        except Exception as exc:
            print(exc)

    # 設問編集 - 動画貼付作成
    def edit_question_by_video_setting(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                self.select_radio_button_by_name('動画貼付', 'movieins', array, 'ancestor::div[1]')
                if array[value] != '動画を貼り付けない':
                    self.item_send_element_key_by_name('input', '回答できるようになるまでの時間', 'movietime', array['動画貼付詳細設定'])
                    self.select_radio_button_by_name('自動再生', 'autostart', array['動画貼付詳細設定'], element='ancestor::tr[1]')
                    self.select_radio_button_by_name('再再生の可否', 'replay', array['動画貼付詳細設定'], element='ancestor::tr[1]')
                    self.select_radio_button_by_name('セキュリティ設定', 'security', array['動画貼付詳細設定'], element='ancestor::tr[1]')
                    self.item_send_element_key_by_name('textarea', 'キャプション', 'captionmovie1[]', array['動画貼付詳細設定'])
        except Exception as exc:
            print(exc)

    # 設問編集 - 条件分岐作成
    def edit_question_condition_setting(self, value, question_number, question_type, question_quid, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                # 結合式から、結合数を算出
                if array_value['結合式'].find('~') >= 0:
                    conjunction = array_value['結合式'].replace('~OR~', '~').replace('~AND~', '~').replace('~(~', '~').replace('~)~', '~')
                    conjunction = len(conjunction.split('~'))
                else:
                    conjunction = 1
                count = -1
                while True:
                    count += 1
                    if count >= conjunction:
                        break
                    else:
                        name = 'condition[' + str(count) + ']'
                        if count < 9:
                            array_label = '条件【' + ('0' + str(count+1))[0:2] + '】'
                        else:
                            array_label = '条件【' + str(count+1) + '】'
                        # 設問文から設問番号を取得して設問タイプを判定する
                        now_question_number = array_value[array_label]['設問文'].split()[0]
                        now_question_type = question_type[question_number.index(now_question_number)]
                        now_question_quid = question_quid[question_number.index(now_question_number)]

                        # 設問文は改行を含んだりするので名前からselectのoptionを選べないのでvalueで選ぶ
                        # self.click_selectbox_by_name(array_value[array_label]['設問文'], name + '[refid]')
                        self.click_selectbox_by_value(now_question_quid, name + '[refid]')

                        # Ajax読み込み待機
                        self.ajax_loading_wait('//div[@class="loading"]/img')

                        # マトリクス混合は「設問文」→「項目」→「対象」の順に操作
                        if now_question_type == 'マトリクス混合':
                            # なのでここでは「対象」を操作せずに個別で操作
                            pass
                        # ほかは「設問文」→「対象」→「項目」の順に操作
                        else:
                            self.click_selectbox_by_name(array_value[array_label]['対象'], name + '[type]')
                            # Ajax読み込み待機
                            self.ajax_loading_wait('//div[@class="loading"]/img')

                        # print(now_question_number)
                        # print(now_question_type)
                        if now_question_type == 'シングル' or now_question_type == '隠しシングル':
                            self.edit_condition_setting_of_single_answer(name, array_value[array_label])
                        elif now_question_type == 'マルチ' or now_question_type == '隠しマルチ':
                            self.edit_condition_setting_of_multi_answer(name, array_value[array_label])
                        elif now_question_type == '数値入力' or now_question_type == 'フリー（小）' or now_question_type == 'フリー（大）':
                            self.edit_condition_setting_of_text_answer(name, array_value[array_label])
                        elif now_question_type == 'マトリクスシングル' or now_question_type == 'SD法':
                            self.edit_condition_setting_of_matrix_single_answer(name, array_value[array_label])
                        elif now_question_type == 'マトリクスマルチ':
                            self.edit_condition_setting_of_matrix_multi_answer(name, array_value[array_label])
                        elif now_question_type == 'マトリクス混合':
                            # マトリクス混合だけQナンバーを渡す（設問文の選択がメソッドの中にあるので）
                            self.edit_condition_setting_of_matrix_mix_answer(name, now_question_quid, array_value[array_label])
                    # Ajax読み込み待機
                    self.ajax_loading_wait('//div[@class="loading"]/img')
                # self.item_click('//input[@type="button"][@value="保存する"]')
        except Exception as exc:
            print(exc)

    # チェックボックス要素をonにする
    def edit_item_checkbox_on_value(self, xpath, array):
        try:
            if self.dom_loading_wait(xpath):
                elements = self.driver.find_elements_by_xpath(xpath)
                if len(elements) == 1:
                    if elements[0].get_attribute('value') in array:
                        elements[0].click()
                else:
                    for element in elements:
                        if element.get_attribute('value') in array:
                            element.click()
            return False
        except Exception as exc:
            print(exc)

    # 条件分岐 - シングル / 隠しシングル
    def edit_condition_setting_of_single_answer(self, name, array):
        try:
            # 条件【01】
            # なんか空白スペースが1つあるから対策
            array['条件'] = '　' + array['条件']
            self.click_selectbox_by_name(array['条件'], name + '[logic]')
            self.edit_item_checkbox_on_value('//input[@name="' + name + '[choice][normal][item][][refid]"]', array['選択肢'])
            if array['次の条件との関係'] is None:
                pass
            else:
                if array['次の条件との関係'] == '':
                    pass
                else:
                    self.select_radio_button_by_name('次の条件との関係', name + '[nextlogic]', array)
        except Exception as exc:
            print(exc)

    # 条件分岐 - マルチ / 隠しマルチ
    def edit_condition_setting_of_multi_answer(self, name, array):
        try:
            # 条件【01】
            if array['対象'] == '回答':
                # なんか空白スペースが1つあるから対策
                array['条件'] = '　' + array['条件']
                self.click_selectbox_by_name(array['条件'], name + '[target_logic]')
                self.edit_item_checkbox_on_value('//input[@name="' + name + '[choice][normal][item][][refid]"]', array['選択肢'])
            elif array['対象'] == '回答数':
                # array['入力値'] = self.get_item_text('//input[@name="' + name + '[value]"]')
                self.item_send_element_key_by_name('input', '入力値', name + '[value]', array)
                # array['条件式'] = self.get_item_select('//select[@name="' + name + '[operator]"]')
                # array['条件式'] = '　' + array['条件式']
                self.click_selectbox_by_name(array['条件式'], name + '[operator]')
            if array['次の条件との関係'] is None:
                pass
            else:
                if array['次の条件との関係'] == '':
                    pass
                else:
                    self.select_radio_button_by_name('次の条件との関係', name + '[nextlogic]', array)
        except Exception as exc:
            print(exc)

    # 条件分岐 - 数値入力 / フリー（小） / フリー（大）
    def edit_condition_setting_of_text_answer(self, name, array):
        try:
            # 条件【01】
            if array['対象'] == '回答値':
                self.click_selectbox_by_name(array['項目'], name + '[choice][normal][item][0][refid]')
                self.item_send_element_key_by_name('input', '入力値', name + '[value]', array)
                self.click_selectbox_by_name(array['条件文'], name + '[operator]')
            elif array['対象'] == '合計値':
                self.item_send_element_key_by_name('input', '入力値', name + '[value]', array)
                self.click_selectbox_by_name(array['条件文'], name + '[operator]')
            elif array['対象'] == '記入':
                self.click_selectbox_by_name(array['項目'], name + '[choice][normal][item][0][refid]')
                # optionのvalue値がない対策
                # array['条件文'] = self.get_item_text('//select[@name="' + name + '[operator]"]')
            elif array['対象'] == '未記入':
                self.click_selectbox_by_name(array['項目'], name + '[choice][normal][item][0][refid]')
                # optionのvalue値がない対策
                # array['条件文'] = self.get_item_text('//select[@name="' + name + '[operator]"]')
            if array['次の条件との関係'] is None:
                pass
            else:
                if array['次の条件との関係'] == '':
                    pass
                else:
                    self.select_radio_button_by_name('次の条件との関係', name + '[nextlogic]', array)
        except Exception as exc:
            print(exc)

    # 条件分岐 - マトリクスシングル / SD法
    def edit_condition_setting_of_matrix_single_answer(self, name, array):
        try:
            # 条件【01】
            self.click_selectbox_by_name(array['項目'], name + '[choice][side][item][0][refid]')

            # Ajax読み込み待機
            self.ajax_loading_wait('//div[@class="loading"]/img')

            # なんか空白スペースが1つあるから対策
            array['条件'] = '　' + array['条件']
            self.click_selectbox_by_name(array['条件'], name + '[logic]')
            self.edit_item_checkbox_on_value('//input[@name="' + name + '[choice][head][item][][refid]"]', array['選択肢'])
            if array['次の条件との関係'] is None:
                pass
            else:
                if array['次の条件との関係'] == '':
                    pass
                else:
                    self.select_radio_button_by_name('次の条件との関係', name + '[nextlogic]', array)
        except Exception as exc:
            print(exc)

    # 条件分岐 - マトリクスマルチ
    def edit_condition_setting_of_matrix_multi_answer(self, name, array):
        try:
            # 条件【01】
            if array['対象'] == '回答':
                self.click_selectbox_by_name(array['項目'], name + '[choice][side][item][0][refid]')

                # Ajax読み込み待機
                self.ajax_loading_wait('//div[@class="loading"]/img')

                # なんか空白スペースが1つあるから対策
                array['条件'] = '　' + array['条件']
                self.click_selectbox_by_name(array['条件'], name + '[target_logic]')
                self.edit_item_checkbox_on_value('//input[@name="' + name + '[choice][head][item][][refid]"]', array['選択肢'])
            elif array['対象'] == '回答数':
                self.click_selectbox_by_name(array['項目'], name + '[choice][side][item][0][refid]')

                # Ajax読み込み待機
                self.ajax_loading_wait('//div[@class="loading"]/img')

                self.item_send_element_key_by_name('input', '入力値', name + '[value]', array)
                self.click_selectbox_by_name(array['条件式'], name + '[operator]')
            if array['次の条件との関係'] is None:
                pass
            else:
                if array['次の条件との関係'] == '':
                    pass
                else:
                    self.select_radio_button_by_name('次の条件との関係', name + '[nextlogic]', array)
        except Exception as exc:
            print(exc)

    # 条件分岐 - マトリクス混合
    def edit_condition_setting_of_matrix_mix_answer(self, name, quid, array):
        try:
            # # マトリクス混合は「項目」→「対象」の順に操作する必要がある
            # self.click_selectbox_by_name(array['対象'], name + '[type]')

            # # Ajax読み込み待機
            # self.ajax_loading_wait('//div[@class="loading"]/img')

            # 条件【01】
            if array['対象'] == '回答':
                # 設問文は改行を含んだりするので名前からselectのoptionを選べないのでvalueで選ぶ
                # self.click_selectbox_by_name(array['項目'], name + '[choice][side][item][0][refid]')
                self.click_selectbox_by_value(quid, name + '[choice][side][item][0][refid]')

                # Ajax読み込み待機
                self.ajax_loading_wait('//div[@class="loading"]/img')

                # マトリクス混合は「項目」→「対象」の順に操作する必要がある
                self.click_selectbox_by_name(array['対象'], name + '[type]')

                # Ajax読み込み待機
                self.ajax_loading_wait('//div[@class="loading"]/img')

                # array['選択肢'] = self.get_item_select('//select[@name="' + name + '[choice][head][item][0][refid]"]')
                # なんか空白スペースが1つあるから対策
                array['条件'] = '　' + array['条件']
                # if array['条件'] == '':
                self.click_selectbox_by_name(array['条件'], name + '[logic]')
                # else:
                self.click_selectbox_by_name(array['条件'], name + '[target_logic]')
                self.edit_item_checkbox_on_value('//input[@name="' + name + '[choice][head][item][][refid]"]', array['選択肢'])
            elif array['対象'] == '回答値':
                # 設問文は改行を含んだりするので名前からselectのoptionを選べないのでvalueで選ぶ
                # self.click_selectbox_by_name(array['項目'], name + '[choice][side][item][0][refid]')
                self.click_selectbox_by_value(quid, name + '[choice][side][item][0][refid]')

                # Ajax読み込み待機
                self.ajax_loading_wait('//div[@class="loading"]/img')

                # マトリクス混合は「項目」→「対象」の順に操作する必要がある
                self.click_selectbox_by_name(array['対象'], name + '[type]')

                # Ajax読み込み待機
                self.ajax_loading_wait('//div[@class="loading"]/img')

                self.click_selectbox_by_name(array['選択肢'], name + '[choice][head][item][0][refid]')
                self.item_send_element_key_by_name('input', '入力値', name + '[value]', array)
                self.click_selectbox_by_name(array['条件文'], name + '[operator]')
            elif array['対象'] == '合計値':
                # 設問文は改行を含んだりするので名前からselectのoptionを選べないのでvalueで選ぶ
                # self.click_selectbox_by_name(array['項目'], name + '[choice][side][item][0][refid]')
                self.click_selectbox_by_value(quid, name + '[choice][side][item][0][refid]')

                # Ajax読み込み待機
                self.ajax_loading_wait('//div[@class="loading"]/img')

                # マトリクス混合は「項目」→「対象」の順に操作する必要がある
                self.click_selectbox_by_name(array['対象'], name + '[type]')

                # Ajax読み込み待機
                self.ajax_loading_wait('//div[@class="loading"]/img')
                self.item_send_element_key_by_name('input', '入力値', name + '[value]', array)
                self.click_selectbox_by_name(array['条件文'], name + '[operator]')
            elif array['対象'] == '記入':
                # 設問文は改行を含んだりするので名前からselectのoptionを選べないのでvalueで選ぶ
                # self.click_selectbox_by_name(array['項目'], name + '[choice][side][item][0][refid]')
                self.click_selectbox_by_value(quid, name + '[choice][side][item][0][refid]')

                # Ajax読み込み待機
                self.ajax_loading_wait('//div[@class="loading"]/img')

                # マトリクス混合は「項目」→「対象」の順に操作する必要がある
                self.click_selectbox_by_name(array['対象'], name + '[type]')

                # Ajax読み込み待機
                self.ajax_loading_wait('//div[@class="loading"]/img')

                self.click_selectbox_by_name(array['選択肢'], name + '[choice][head][item][0][refid]')
                # optionのvalue値がない対策
                # array['条件文'] = self.get_item_text('//select[@name="' + name + '[operator]"]')
            elif array['対象'] == '未記入':
                # 設問文は改行を含んだりするので名前からselectのoptionを選べないのでvalueで選ぶ
                # self.click_selectbox_by_name(array['項目'], name + '[choice][side][item][0][refid]')
                self.click_selectbox_by_value(quid, name + '[choice][side][item][0][refid]')

                # Ajax読み込み待機
                self.ajax_loading_wait('//div[@class="loading"]/img')

                # マトリクス混合は「項目」→「対象」の順に操作する必要がある
                self.click_selectbox_by_name(array['対象'], name + '[type]')

                # Ajax読み込み待機
                self.ajax_loading_wait('//div[@class="loading"]/img')

                self.click_selectbox_by_name(array['選択肢'], name + '[choice][head][item][0][refid]')
                # optionのvalue値がない対策
                # array['条件文'] = self.get_item_text('//select[@name="' + name + '[operator]"]')
            if array['次の条件との関係'] is None:
                pass
            else:
                if array['次の条件との関係'] == '':
                    pass
                else:
                    self.select_radio_button_by_name('次の条件との関係', name + '[nextlogic]', array)
        except Exception as exc:
            print(exc)






    # SA(単一選択)
    def edit_new_question_by_single_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array)
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            self.item_send_element_key_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # 選択肢
            self.edit_question_choice_group_by_name('グループ設定', 'choice[normal][useGroup]', array)
            self.edit_question_choice_text_group_by_name('textarea', 'キャプション', 'choice[normal][block][1][caption][ja]', array)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
            self.scroll_at_javascript_by_id('captionCO1')
            self.edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
            if array['グループ設定']['グループ設定する'] == 'on':
                self.select_radio_button_by_name('表示方向', 'choice[normal][direction]', array)
                self.item_send_element_key_by_name('input', 'グループ選択肢数,選択肢数,…', 'choice[normal][multiline]', array)
                self.item_send_element_key_by_name('input', '折り返し数', 'choice[normal][maxline]', array)
                self.item_send_element_key_by_name('input', '幅設定', 'choice[normal][linewidth]', array)
                self.edit_question_randomize_by_group('グループランダマイズ', 'choice[normal][orderlogic]', array, 'parent::span')
                self.item_send_element_key_by_name('input', 'グループ位置固定', 'choice[normal][fixBlock]', array)
            else:
                self.select_radio_button_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                self.item_send_element_key_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                self.item_send_element_key_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
            self.select_radio_button_by_name('必須入力チェック', 'must', array)
            self.select_radio_button_by_name('表示形式', 'choice[normal][controlType]', array)
            self.select_radio_button_by_name('設問文と選択肢表示', 'view_type', array)
            self.select_radio_button_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
            self.edit_question_by_itile('i-タイル設定', 'i_tile_setting_flag', array, 'parent::label/parent::td[1]')
            # 設問編集(2)
            self.item_send_element_key_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.edit_question_by_image_setting('画像', 'insertImage', array)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.set_error_check_process('エラーチェック', array)
        except Exception as exc:
            print(exc)

    # MA(複数選択)
    def edit_new_question_by_multi_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array)
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            self.item_send_element_key_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # 選択肢
            self.edit_question_choice_group_by_name('グループ設定', 'choice[normal][useGroup]', array)
            self.edit_question_choice_text_group_by_name('textarea', 'キャプション', 'choice[normal][block][1][caption][ja]', array)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
            self.scroll_at_javascript_by_id('captionCO1')
            self.edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
            if array['グループ設定']['グループ設定する'] == 'on':
                self.select_radio_button_by_name('表示方向', 'choice[normal][direction]', array)
                self.item_send_element_key_by_name('input', 'グループ選択肢数,選択肢数,…', 'choice[normal][multiline]', array)
                self.item_send_element_key_by_name('input', '折り返し数', 'choice[normal][maxline]', array)
                self.item_send_element_key_by_name('input', '幅設定', 'choice[normal][linewidth]', array)
                self.edit_question_randomize_by_group('グループランダマイズ', 'choice[normal][orderlogic]', array, 'parent::span')
                self.item_send_element_key_by_name('input', 'グループ位置固定', 'choice[normal][fixBlock]', array)
            else:
                self.select_radio_button_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                self.item_send_element_key_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                self.item_send_element_key_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
            self.select_radio_button_by_name('必須入力チェック', 'must', array)
            self.selection_count_limit('選択個数制限', 'limit', array)
            self.select_radio_button_by_name('設問文と選択肢表示', 'view_type', array)
            self.select_radio_button_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
            self.edit_question_by_itile('i-タイル設定', 'i_tile_setting_flag', array, 'parent::label/parent::td[1]')
            # 設問編集(2)
            self.item_send_element_key_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.edit_question_by_image_setting('画像', 'insertImage', array)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.set_error_check_process('エラーチェック', array)
        except Exception as exc:
            print(exc)

    # 隠し設問SA
    def edit_new_question_by_hidden_single_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array)
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            # 選択肢
            element = 'textarea'
            value = '選択肢'
            key = 'choice[normal][block][1][choiceText][ja]'
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                array_value = self.convert_question_pipe(array_value)
                xpath = '//' + str(element) + '[@name="' + str(key) + '"]'
                self.item_send_text_appending_overwriting(xpath, array_value, 'c')
            # 設問編集(2)
            # ローテーションパターンは未実装
            self.select_radio_button_by_name('抽選機能', 'lottery', array)
            self.set_gate_interlock('打切り設定連動機能', 'lotteryAbort', array)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
        except Exception as exc:
            print(exc)

    # 数値
    def edit_new_question_by_number_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array)
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            self.item_send_element_key_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # 選択肢
            self.edit_question_choice_group_by_name('グループ設定', 'choice[normal][useGroup]', array)
            self.edit_question_choice_text_group_by_name('textarea', 'キャプション', 'choice[normal][block][1][caption][ja]', array)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
            self.scroll_at_javascript_by_id('captionCO1')
            self.edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
            if array['グループ設定']['グループ設定する'] == 'on':
                self.select_radio_button_by_name('表示方向', 'choice[normal][direction]', array)
                self.item_send_element_key_by_name('input', 'グループ選択肢数,選択肢数,…', 'choice[normal][multiline]', array)
                self.item_send_element_key_by_name('input', '折り返し数', 'choice[normal][maxline]', array)
                self.item_send_element_key_by_name('input', '幅設定', 'choice[normal][linewidth]', array)
                self.edit_question_randomize_by_group('グループランダマイズ', 'choice[normal][orderlogic]', array, 'parent::span')
                self.item_send_element_key_by_name('input', 'グループ位置固定', 'choice[normal][fixBlock]', array)
            else:
                self.select_radio_button_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                self.item_send_element_key_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                self.item_send_element_key_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
            self.select_radio_button_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
            self.select_radio_button_by_name('設問文と選択肢表示', 'view_type', array)
            self.select_radio_button_by_name('合計値表示', 'showTotal', array)
            self.selection_total_count_limit('合計値制限', 'limitTotal', array)
            # 設問編集(2)
            self.item_send_element_key_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.edit_question_by_image_setting('画像', 'insertImage', array)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.set_error_check_process('エラーチェック', array)
        except Exception as exc:
            print(exc)

    # 自由記入短文
    def edit_new_question_by_freeshort_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array)
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            self.item_send_element_key_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # 選択肢
            self.edit_question_choice_group_by_name('グループ設定', 'choice[normal][useGroup]', array)
            self.edit_question_choice_text_group_by_name('textarea', 'キャプション', 'choice[normal][block][1][caption][ja]', array)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
            self.scroll_at_javascript_by_id('captionCO1')
            self.edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
            if array['グループ設定']['グループ設定する'] == 'on':
                self.select_radio_button_by_name('表示方向', 'choice[normal][direction]', array)
                self.item_send_element_key_by_name('input', 'グループ選択肢数,選択肢数,…', 'choice[normal][multiline]', array)
                self.item_send_element_key_by_name('input', '折り返し数', 'choice[normal][maxline]', array)
                self.item_send_element_key_by_name('input', '幅設定', 'choice[normal][linewidth]', array)
                self.edit_question_randomize_by_group('グループランダマイズ', 'choice[normal][orderlogic]', array, 'parent::span')
                self.item_send_element_key_by_name('input', 'グループ位置固定', 'choice[normal][fixBlock]', array)
            else:
                self.select_radio_button_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                self.item_send_element_key_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                self.item_send_element_key_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
            self.select_radio_button_by_name('設問文と選択肢表示', 'view_type', array)
            self.select_radio_button_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
            # 設問編集(2)
            self.item_send_element_key_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.edit_question_by_image_setting('画像', 'insertImage', array)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.set_error_check_process('エラーチェック', array)
        except Exception as exc:
            print(exc)

    # 自由記入長文
    def edit_new_question_by_freelong_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array)
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            self.item_send_element_key_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # 選択肢
            self.edit_question_choice_group_by_name('グループ設定', 'choice[normal][useGroup]', array)
            self.edit_question_choice_text_group_by_name('textarea', 'キャプション', 'choice[normal][block][1][caption][ja]', array)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
            self.scroll_at_javascript_by_id('captionCO1')
            self.edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
            if array['グループ設定']['グループ設定する'] == 'on':
                self.select_radio_button_by_name('表示方向', 'choice[normal][direction]', array)
                self.item_send_element_key_by_name('input', 'グループ選択肢数,選択肢数,…', 'choice[normal][multiline]', array)
                self.item_send_element_key_by_name('input', '折り返し数', 'choice[normal][maxline]', array)
                self.item_send_element_key_by_name('input', '幅設定', 'choice[normal][linewidth]', array)
                self.edit_question_randomize_by_group('グループランダマイズ', 'choice[normal][orderlogic]', array, 'parent::span')
                self.item_send_element_key_by_name('input', 'グループ位置固定', 'choice[normal][fixBlock]', array)
            else:
                self.select_radio_button_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                self.item_send_element_key_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                self.item_send_element_key_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
            self.select_radio_button_by_name('設問文と選択肢表示', 'view_type', array)
            self.select_radio_button_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
            # 設問編集(2)
            self.item_send_element_key_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.edit_question_by_image_setting('画像', 'insertImage', array)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.set_error_check_process('エラーチェック', array)
        except Exception as exc:
            print(exc)

    # 隠し設問MA
    def edit_new_question_by_hidden_multi_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array)
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            # 選択肢
            element = 'textarea'
            value = '選択肢'
            key = 'choice[normal][block][1][choiceText][ja]'
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                array_value = self.convert_question_pipe(array_value)
                xpath = '//' + str(element) + '[@name="' + str(key) + '"]'
                self.item_send_text_appending_overwriting(xpath, array_value, 'c')
            self.scroll_at_javascript_by_id('choice')
            # 設問編集(2)
            self.set_lottery_count('抽選機能', 'lottery', array)
            self.set_gate_interlock('打切り設定連動機能', 'lotteryAbort', array)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
        except Exception as exc:
            print(exc)

    # 画像アップロード
    def edit_new_question_by_image_upload_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array)
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            self.item_send_element_key_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # 選択肢
            self.edit_question_choice_group_by_name('グループ設定', 'choice[normal][useGroup]', array)
            self.edit_question_choice_text_group_by_name('textarea', 'キャプション', 'choice[normal][block][1][caption][ja]', array)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
            self.scroll_at_javascript_by_id('captionCO1')
            self.edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
            if array['グループ設定']['グループ設定する'] == 'on':
                self.select_radio_button_by_name('表示方向', 'choice[normal][direction]', array)
                self.item_send_element_key_by_name('input', 'グループ選択肢数,選択肢数,…', 'choice[normal][multiline]', array)
                self.item_send_element_key_by_name('input', '折り返し数', 'choice[normal][maxline]', array)
                self.item_send_element_key_by_name('input', '幅設定', 'choice[normal][linewidth]', array)
                self.edit_question_randomize_by_group('グループランダマイズ', 'choice[normal][orderlogic]', array, 'parent::span')
                self.item_send_element_key_by_name('input', 'グループ位置固定', 'choice[normal][fixBlock]', array)
            else:
                self.select_radio_button_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                self.item_send_element_key_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                self.item_send_element_key_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
            self.select_radio_button_by_name('設問文と選択肢表示', 'view_type', array)
            self.select_radio_button_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
            # 設問編集(2)
            self.item_send_element_key_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.edit_question_by_image_setting('画像', 'insertImage', array)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.set_error_check_process('エラーチェック', array)
        except Exception as exc:
            print(exc)

    # マトリクスSA
    def edit_new_question_by_matrix_single_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array)
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            self.item_send_element_key_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            self.clear_checkbox_all_by_name('表頭・表側の位置を入れ替え', 'transpose')
            self.choose_multiple_checkbox('表頭・表側の位置を入れ替え', {'表頭・表側の位置を入れ替える': 'transpose'}, array, 'input[@name=')
            # 選択肢[表上（選択肢側）]
            array_head = array['表上']
            self.edit_question_choice_group_by_name('グループ設定', 'choice[head][useGroup]', array_head)
            self.edit_question_choice_text_group_by_name('textarea', 'キャプション', 'choice[head][block][1][caption][ja]', array_head)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢', 'choice[head][block][1][choiceText][ja]', array_head)
            self.scroll_at_javascript_by_id('choiceSCO1')
            self.edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[head][block][1][orderlogic]', array_head, 'ancestor::td[1]')
            if array_head['グループ設定']['グループ設定する'] == 'on':
                self.edit_question_randomize_by_group('グループランダマイズ', 'choice[head][orderlogic]', array_head, 'ancestor::td[1]')
                self.item_send_element_key_by_name('input', 'グループ位置固定', 'choice[head][fixBlock]', array_head)
            self.select_radio_button_by_name('表示形式（PC/iPad）', 'choice[head][controlType]', array_head, 'ancestor::tr[1]')
            self.select_radio_button_by_name('文字列方向', 'choice[head][directstr]', array_head, 'ancestor::tr[1]')
            self.select_radio_button_by_name('選択肢番号', 'choice[head][showChoiceNo]', array_head, 'ancestor::tr[1]')
            # 選択肢[表左（項目側）]
            array_side = array['項目']
            self.edit_question_choice_group_by_name('グループ設定', 'choice[side][useGroup]', array_side)
            self.edit_question_choice_text_group_by_name('textarea', 'キャプション', 'choice[side][block][1][caption][ja]', array_side)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢', 'choice[side][block][1][choiceText][ja]', array_side)
            self.scroll_at_javascript_by_id('choiceHCO1')
            self.edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[side][block][1][orderlogic]', array_side, 'ancestor::td[1]')
            if array_side['グループ設定']['グループ設定する'] == 'on':
                self.edit_question_randomize_by_group('グループランダマイズ', 'choice[side][orderlogic]', array_side, 'ancestor::td[1]')
                self.item_send_element_key_by_name('input', 'グループ位置固定', 'choice[side][fixBlock]', array_side)
            self.select_radio_button_by_name('文字列方向', 'choice[side][directstr]', array_side, 'ancestor::tr[1]')
            self.select_radio_button_by_name('選択肢番号', 'choice[side][showChoiceNo]', array_side, 'ancestor::tr[1]')
            self.item_send_element_key_by_name('input', '左肩コメント', 'leftShoulderComment[ja]', array_side)
            # そのほか
            self.select_radio_button_by_name('必須入力チェック', 'must', array, 'ancestor::tr[1]')
            self.select_radio_button_by_name('設問文と選択肢表示', 'view_type', array)
            self.select_radio_button_by_name('同一回答チェック', 'straightcheck', array)
            # self.clear_checkbox_all_by_name('順位付けチェック', 'sequencecheck')
            self.choose_multiple_checkbox('順位付けチェック', {'順位付けチェックを行う': 'sequencecheck'}, array, 'input[@name=')
            self.item_send_element_key_by_name('input', '表上繰り返し', 'repeathead', array)
            self.item_send_element_key_by_name('input', '横幅指定', 'multilinewidth', array)
            # 表示指定
            self.select_radio_button_by_name('選択行反転表示', 'highlight', array, 'ancestor::tr[1]')
            # 色指定
            self.edit_question_by_itile('i-タイル設定', 'i_tile_setting_flag', array, 'parent::label/parent::td[1]')
            # 設問編集(2)
            self.item_send_element_key_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.edit_question_by_image_setting('画像', 'insertImage', array)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.set_error_check_process('エラーチェック', array)
        except Exception as exc:
            print(exc)

    # マトリクスMA
    def edit_new_question_by_matrix_multi_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array)
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            self.item_send_element_key_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            self.clear_checkbox_all_by_name('表頭・表側の位置を入れ替え', 'transpose')
            self.choose_multiple_checkbox('表頭・表側の位置を入れ替え', {'表頭・表側の位置を入れ替える': 'transpose'}, array, 'input[@name=')
            # 選択肢[表上（選択肢側）]
            array_head = array['表上']
            self.edit_question_choice_group_by_name('グループ設定', 'choice[head][useGroup]', array_head)
            self.edit_question_choice_text_group_by_name('textarea', 'キャプション', 'choice[head][block][1][caption][ja]', array_head)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢', 'choice[head][block][1][choiceText][ja]', array_head)
            self.scroll_at_javascript_by_id('choiceSCO1')
            self.edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[head][block][1][orderlogic]', array_head, 'ancestor::td[1]')
            if array_head['グループ設定']['グループ設定する'] == 'on':
                self.edit_question_randomize_by_group('グループランダマイズ', 'choice[head][orderlogic]', array_head, 'ancestor::td[1]')
                self.item_send_element_key_by_name('input', 'グループ位置固定', 'choice[head][fixBlock]', array_head)
            self.select_radio_button_by_name('文字列方向', 'choice[head][directstr]', array_head, 'ancestor::tr[1]')
            self.selection_count_limit('選択個数制限', 'limit', array_head)
            self.select_radio_button_by_name('選択肢番号', 'choice[head][showChoiceNo]', array_head, 'ancestor::tr[1]')
            # 選択肢[表左（項目側）]
            array_side = array['項目']
            self.edit_question_choice_group_by_name('グループ設定', 'choice[side][useGroup]', array_side)
            self.edit_question_choice_text_group_by_name('textarea', 'キャプション', 'choice[side][block][1][caption][ja]', array_side)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢', 'choice[side][block][1][choiceText][ja]', array_side)
            self.scroll_at_javascript_by_id('choiceHCO1')
            self.edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[side][block][1][orderlogic]', array_side, 'ancestor::td[1]')
            if array_side['グループ設定']['グループ設定する'] == 'on':
                self.edit_question_randomize_by_group('グループランダマイズ', 'choice[side][orderlogic]', array_side, 'ancestor::td[1]')
                self.item_send_element_key_by_name('input', 'グループ位置固定', 'choice[side][fixBlock]', array_side)
            self.select_radio_button_by_name('文字列方向', 'choice[side][directstr]', array_side, 'ancestor::tr[1]')
            self.select_radio_button_by_name('選択肢番号', 'choice[side][showChoiceNo]', array_side, 'ancestor::tr[1]')
            self.item_send_element_key_by_name('input', '左肩コメント', 'leftShoulderComment[ja]', array_side)
            # そのほか
            self.select_radio_button_by_name('必須入力チェック', 'must', array, 'ancestor::tr[1]')
            self.select_radio_button_by_name('設問文と選択肢表示', 'view_type', array)
            self.select_radio_button_by_name('同一回答チェック', 'straightcheck', array)
            self.item_send_element_key_by_name('input', '表上繰り返し', 'repeathead', array)
            self.item_send_element_key_by_name('input', '横幅指定', 'multilinewidth', array)
            # 表示指定
            self.select_radio_button_by_name('選択行反転表示', 'highlight', array, 'ancestor::tr[1]')
            # 色指定
            self.edit_question_by_itile('i-タイル設定', 'i_tile_setting_flag', array, 'parent::label/parent::td[1]')
            # 設問編集(2)
            self.item_send_element_key_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.edit_question_by_image_setting('画像', 'insertImage', array)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.set_error_check_process('エラーチェック', array)
        except Exception as exc:
            print(exc)

    # マトリクス混合
    def edit_new_question_by_matrix_mix_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array, 'c')
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array)
            self.item_send_element_key_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            self.clear_checkbox_all_by_name('表頭・表側の位置を入れ替え', 'transpose')
            self.choose_multiple_checkbox('表頭・表側の位置を入れ替え', {'表頭・表側の位置を入れ替える': 'transpose'}, array, 'input[@name=')
            # 選択肢[表上（選択肢側）]
            array_head = array['表上']
            self.edit_question_choice_group_by_name('グループ設定', 'choice[head][useGroup]', array_head)
            self.edit_question_choice_text_group_by_name('textarea', 'キャプション', 'choice[head][block][1][caption][ja]', array_head)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢', 'choice[head][block][1][choiceText][ja]', array_head)
            self.scroll_at_javascript_by_id('choiceSCO1')
            self.edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[head][block][1][orderlogic]', array_head, 'ancestor::td[1]')
            if array_head['グループ設定']['グループ設定する'] == 'on':
                self.edit_question_randomize_by_group('グループランダマイズ', 'choice[head][orderlogic]', array_head, 'ancestor::td[1]')
                self.item_send_element_key_by_name('input', 'グループ位置固定', 'choice[head][fixBlock]', array_head)
            self.select_radio_button_by_name('文字列方向', 'choice[head][directstr]', array_head, 'ancestor::tr[1]')
            self.selection_count_limit('選択個数制限', 'limit', array_head)
            self.select_radio_button_by_name('選択肢番号', 'choice[head][showChoiceNo]', array_head, 'ancestor::tr[1]')
            # 選択肢[表左（項目側）]
            array_side = array['項目']
            self.edit_question_choice_group_by_name('グループ設定', 'choice[side][useGroup]', array_side)
            self.edit_question_choice_text_group_by_name('textarea', 'キャプション', 'choice[side][block][1][caption][ja]', array_side)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢', 'choice[side][block][1][choiceText][ja]', array_side)
            self.scroll_at_javascript_by_id('choiceHCO1')
            self.edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[side][block][1][orderlogic]', array_side, 'ancestor::td[1]')
            if array_side['グループ設定']['グループ設定する'] == 'on':
                self.edit_question_randomize_by_group('グループランダマイズ', 'choice[side][orderlogic]', array_side, 'ancestor::td[1]')
                self.item_send_element_key_by_name('input', 'グループ位置固定', 'choice[side][fixBlock]', array_side)
            self.select_radio_button_by_name('文字列方向', 'choice[side][directstr]', array_side, 'ancestor::tr[1]')
            self.select_radio_button_by_name('選択肢番号', 'choice[side][showChoiceNo]', array_side, 'ancestor::tr[1]')
            self.item_send_element_key_by_name('input', '左肩コメント', 'leftShoulderComment[ja]', array_side)
            # そのほか
            self.select_radio_button_by_name('必須入力チェック', 'must', array, 'ancestor::tr[1]')
            self.select_radio_button_by_name('設問文と選択肢表示', 'view_type', array)
            # 90番のみ、動的絞り込みが実装してある
            if self.mode == 'dev4s' or self.mode == '4s90':
                self.clear_checkbox_all_by_name('絞り込み', 'useDynamicFilter')
                if array.get('絞り込み') is not None:
                    if array['絞り込み'] == '絞り込みを行う':
                        self.choose_multiple_checkbox('絞り込み', {'絞り込みを行う': 'useDynamicFilter'}, array, 'input[@name=')
                        self.clear_matrix_mix_use_dynamic_filter_checkbox()
                        count = -1
                        for array_value in array['絞り込み設定']:
                            count += 1
                            # 追加
                            xpath = '//input[@id="addFilter"]'
                            self.item_click(xpath)
                            # フィルタ設定
                            xpath =  'target_item[' + str(count) + ']'
                            array_temp = []
                            array_temp.append(array['絞り込み設定'][array_value][0])
                            array_temp.append(array['絞り込み設定'][array_value][1])
                            array_value_child = {'絞り込み設定': array_temp}
                            self.item_pick_multiple_by_value('絞り込み設定', ['target_item[' + str(count) + ']', 'trigger_item[' + str(count) + ']'], array_value_child)
                            # 表示/非表示
                            if array['絞り込み設定'][array_value][2] == '非表示':
                                xpath = '//input[@name="filterType[' + str(count) + ']"][@value="hide"]'
                                self.item_click(xpath)
                            # 排他も含む
                            if len(array['絞り込み設定'][array_value]) > 3:
                                if array['絞り込み設定'][array_value][3] == '排他も含む':
                                    xpath = '//input[@name="withExclusive[' + str(count) + ']"]'
                                    self.item_click(xpath)
            self.item_send_element_key_by_name('input', '表上繰り返し', 'repeathead', array)
            self.item_send_element_key_by_name('input', '横幅指定', 'multilinewidth', array)
            # 表示指定
            self.select_radio_button_by_name('選択行反転表示', 'highlight', array, 'ancestor::tr[1]')
            # 色指定
            self.edit_question_by_itile('i-タイル設定', 'i_tile_setting_flag', array, 'parent::label/parent::td[1]')
            # 設問編集(2)
            self.item_send_element_key_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.edit_question_by_image_setting('画像', 'insertImage', array)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.set_error_check_process('エラーチェック', array)
        except Exception as exc:
            print(exc)

    # 文章・画像のみ
    def edit_new_question_by_through_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array)
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            # 設問編集(2)
            self.item_send_element_key_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.edit_question_by_image_setting('画像', 'insertImage', array)
            self.edit_question_by_video_setting('動画貼付', 'movieins', array)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.set_error_check_process('エラーチェック', array)
        except Exception as exc:
            print(exc)

    # プロフィール
    def edit_new_question_by_profile_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array, 'c')
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            # 選択肢
            if self.mode == 'dev4s' or self.mode == '4s90':
                self.item_send_element_key_by_name('textarea', '選択肢', 'choice[normal][choiceText][1][ja]', array)
            else:
                # 氏名
                self.item_send_element_key_by_profile('input', '氏名', ['captionItemTypeAry[name][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 0)
                # 氏名（ふりがな）
                self.item_send_element_key_by_profile('input', '氏名（ふりがな）', ['captionItemTypeAry[name_k][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 1)
                # あなたの生年月日
                self.item_send_element_key_by_profile('input', 'あなたの生年月日', ['captionItemTypeAry[birthday][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 2)
                # あなたの性別
                self.item_send_element_key_by_profile('input', 'あなたの性別', ['captionItemTypeAry[sex][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 3)
                # 郵便番号
                self.item_send_element_key_by_profile('input', '郵便番号', ['captionItemTypeAry[postcode][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 4)
                # 住所（都道府県）
                self.item_send_element_key_by_profile('input', '住所（都道府県）', ['captionItemTypeAry[prefecture][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 5)
                # 住所（市区町村）
                self.item_send_element_key_by_profile('input', '住所（市区町村）', ['captionItemTypeAry[city][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 6)
                # 住所（町名・番地・ビル名など）
                self.item_send_element_key_by_profile('input', '住所（町名・番地・ビル名など）', ['captionItemTypeAry[street][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 7)
                # 電話番号
                self.item_send_element_key_by_profile('input', '電話番号', ['captionItemTypeAry[tel][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 8)
                # 携帯電話番号
                self.item_send_element_key_by_profile('input', '携帯電話番号', ['captionItemTypeAry[mobile_tel][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 9)
                # メールアドレス
                self.item_send_element_key_by_profile('input', 'メールアドレス', ['captionItemTypeAry[email][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 10)
                # メールアドレス確認用
                self.item_send_element_key_by_profile('input', 'メールアドレス確認用', ['captionItemTypeAry[email_c][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 11)
                # 会社名
                self.item_send_element_key_by_profile('input', '会社名', ['captionItemTypeAry[company][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 12)
                # 支店名・営業所名
                self.item_send_element_key_by_profile('input', '支店名・営業所名', ['captionItemTypeAry[branch][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 13)
                # 部署名
                self.item_send_element_key_by_profile('input', '部署名', ['captionItemTypeAry[post][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 14)
                # メールアドレス(＠区切り無し)
                self.item_send_element_key_by_profile('input', 'メールアドレス(＠区切り無し)', ['captionItemTypeAry[email_not_delimitation][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 15)
                # メールアドレス確認用(＠区切り無し)
                self.item_send_element_key_by_profile('input', 'メールアドレス確認用(＠区切り無し)', ['captionItemTypeAry[email_not_delimitation_c][ja]','useItemTypeAry[]','mustItemTypeAry[]'], array['選択肢'], 16)
            # self.scroll_at_javascript_by_id('captionCO1')
            self.select_radio_button_by_name('設問文と選択肢表示', 'view_type', array)
            # 設問編集(2)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
            self.edit_question_by_image_setting('画像', 'insertImage', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
        except Exception as exc:
            print(exc)

    # SD法
    def edit_new_question_by_matrix_sd_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array)
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            self.item_send_element_key_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            array_head = array['表上']
            self.edit_question_choice_group_by_name('グループ設定', 'choice[head][useGroup]', array_head)
            self.edit_question_choice_text_group_by_name('textarea', 'キャプション', 'choice[head][block][1][caption][ja]', array_head)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢', 'choice[head][block][1][choiceText][ja]', array_head)
            self.scroll_at_javascript_by_id('captionHCO1')
            self.edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[head][block][1][orderlogic]', array_head, 'ancestor::td[1]')
            if array_head['グループ設定']['グループ設定する'] == 'on':
                self.edit_question_randomize_by_group('グループランダマイズ', 'choice[head][orderlogic]', array_head, 'ancestor::td[1]')
                self.item_send_element_key_by_name('input', 'グループ位置固定', 'choice[head][fixBlock]', array_head)
            self.select_radio_button_by_name('文字列方向', 'choice[head][directstr]', array_head, 'ancestor::tr[1]')
            self.select_radio_button_by_name('選択肢番号', 'choice[head][showChoiceNo]', array_head, 'ancestor::tr[1]')
            # 選択肢[表左（項目側）]
            array_side = array['項目']
            self.edit_question_choice_group_by_name('グループ設定', 'choice[side][useGroup]', array_side)
            self.edit_question_choice_text_group_by_name('textarea', 'キャプション', 'choice[side][block][1][caption][left][ja]', array_side)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢（表左）', 'choice[side][block][1][choiceText][left][ja]', array_side)
            self.edit_question_choice_text_group_by_name('textarea', '選択肢（表右）', 'choice[side][block][1][choiceText][right][ja]', array_side)
            self.scroll_at_javascript_by_id('choiceSLCO1')
            self.edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[side][block][1][orderlogic]', array_side, 'ancestor::td[1]')
            if array_side['グループ設定']['グループ設定する'] == 'on':
                self.edit_question_randomize_by_group('グループランダマイズ', 'choice[side][orderlogic]', array_side, 'ancestor::td[1]')
                self.item_send_element_key_by_name('input', 'グループ位置固定', 'choice[side][fixBlock]', array_side)
            self.select_radio_button_by_name('選択肢番号', 'choice[side][showChoiceNo]', array_side, 'ancestor::tr[1]')
            self.item_send_element_key_by_name('input', '左肩コメント', 'leftShoulderComment[ja]', array_side)
            self.item_send_element_key_by_name('input', '右肩コメント', 'rightShoulderComment[ja]', array_side)
            # そのほか
            self.select_radio_button_by_name('必須入力チェック', 'must', array, 'ancestor::tr[1]')
            self.select_radio_button_by_name('設問文と選択肢表示', 'view_type', array)
            self.item_send_element_key_by_name('input', '表上繰り返し', 'repeathead', array)
            self.item_send_element_key_by_name('input', '横幅指定', 'multilinewidth', array)
            # 表示指定
            self.select_radio_button_by_name('選択行反転表示', 'highlight', array, 'ancestor::tr[1]')
            # 色指定
            self.edit_question_by_itile('i-タイル設定', 'i_tile_setting_flag', array, 'parent::label/parent::td[1]')
            # 設問編集(2)
            self.item_send_element_key_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.edit_question_by_image_setting('画像', 'insertImage', array)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.set_error_check_process('エラーチェック', array)
        except Exception as exc:
            print(exc)

    # 登録情報設問
    def edit_new_question_by_attribute_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array)
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.select_radio_button_by_attribute_type('属性タイプ', 'moniinfo', array)
            self.item_send_element_key_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            self.item_send_element_key_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            if array['属性タイプ'] == '年齢(数値FA)':
                # 選択肢
                self.item_send_element_key_by_name('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array, 'c')
                self.scroll_at_javascript_by_id('captionCO1')
                self.edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
                self.select_radio_button_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                self.item_send_element_key_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                self.item_send_element_key_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
                self.select_radio_button_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
                self.select_radio_button_by_name('設問文と選択肢表示', 'view_type', array)
                self.select_radio_button_by_name('合計値表示', 'showTotal', array)
                self.selection_total_count_limit('合計値制限', 'limitTotal', array)
            else:
                # 選択肢
                self.item_send_element_key_by_name('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array, 'c')
                self.scroll_at_javascript_by_id('captionCO1')
                self.edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
                self.select_radio_button_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                self.item_send_element_key_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                self.item_send_element_key_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
                self.select_radio_button_by_name('必須入力チェック', 'must', array)
                self.select_radio_button_by_name('表示形式', 'choice[normal][controlType]', array)
                self.select_radio_button_by_name('設問文と選択肢表示', 'view_type', array)
                self.select_radio_button_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
            # 設問編集(2)
            self.item_send_element_key_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.edit_question_by_image_setting('画像', 'insertImage', array)
            self.item_send_element_key_by_name('textarea', '備考', 'qu_remarks', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.set_error_check_process('エラーチェック', array)
        except Exception as exc:
            print(exc)

    # 外部連携設問
    def edit_new_question_by_post_external_answer(self, array):
        try:
            # 設問編集(1)
            self.item_send_element_key_by_name('input', '設問タイトル', 'qu_title', array)
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.item_send_element_key_by_name('input', '設問No', 'no', array)
                self.select_radio_button_by_name('設問No表示', 'numberView', array)
            self.item_send_element_key_by_name('textarea', '設問文', 'explain[ja]', array, 'c')
            # 行き先情報
            self.select_radio_button_by_name('設問文と選択肢表示', 'view_type', array)
            # 戻り先情報
            # 設問編集(2)
            self.item_send_element_key_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.item_send_element_key_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
        except Exception as exc:
            print(exc)

    # START
    def edit_new_question_by_start_page_answer(self, array):
        try:
            # 設問編集
            self.item_send_element_key_by_name('input', 'アンケートタイトル', 're_public_title[ja]', array, 'c')
            self.select_radio_button_by_name('スタートページ表示', 're_disp_start_page', array)
            self.item_send_element_key_by_name('textarea', 'スタート設問文', 're_explain[ja]', array, 'c')
            self.select_radio_button_by_name('「個人情報の取り扱いについて」同意欄', 're_ppa_id', array)
            self.item_send_element_key_by_name('textarea', 'スタート個人情報について', 're_policy[ja]', array, 'c')
            self.item_send_element_key_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array, 'c')
        except Exception as exc:
            print(exc)

    # END,GATE,COMP
    def edit_new_question_by_end_page_answer(self, array):
        try:
            # 設問編集
            self.item_send_element_key_by_name('textarea', 'メッセージ', 'message[ja]', array)
            self.set_question_redirect('自動リダイレクト', 'redirect_type', array)
            display_swtch = self.get_item_checkbox('//input[@name="link[useGroup]"]')
            # リンク設定をONにしたいとき
            if array['リンク']['リンク設定する'] == 'on':
                # 画面上の「リンク設定」はoffなので、onにする
                if display_swtch == 'off':
                    xpath = '//input[@name="link[useGroup]"]'
                    if self.dom_loading_wait(xpath):
                        element = self.driver.find_element_by_xpath(xpath)
                        element.click()
                        # Ajax読み込み待機
                        self.ajax_loading_wait('//div[@class="loading"]/img')
                # リンク数を設定する
                loop_count = int(array['リンク']['リンク数'])
                self.click_selectbox_by_name(loop_count, 'link[choice_num]')
                count = 0
                for array_value in array['リンク']['リンク設定']:
                    count = count + 1
                    # 表示条件
                    xpath = '//input[@name="link[conditions][' + str(count) + ']"]'
                    if self.dom_loading_wait(xpath):
                        self.clear_text(xpath)
                        self.item_send(xpath, array_value['表示条件'])
                    # ボタン上コメント
                    xpath = '//textarea[@name="link[message_top][' + str(count) + '][ja]"]'
                    if self.dom_loading_wait(xpath):
                        self.clear_text(xpath)
                        self.item_send(xpath, array_value['ボタン上コメント'])
                    # ボタン
                    if array_value['ボタン'] == '表示':
                        xpath = '//input[@name="link[linkshow][' + str(count) + ']"]'
                        if self.dom_loading_wait(xpath):
                            element = self.driver.find_element_by_xpath(xpath)
                            element.click()
                        # ボタン名称
                        xpath = '//input[@name="link[button_name][' + str(count) + '][ja]"]'
                        if self.dom_loading_wait(xpath):
                            self.clear_text(xpath)
                            self.item_send(xpath, array_value['ボタン名称'])
                    # URL
                    xpath = '//input[@name="link[link_address][' + str(count) + ']"]'
                    if self.dom_loading_wait(xpath):
                        self.clear_text(xpath)
                        self.item_send(xpath, array_value['URL'])
                    # ボタン下コメント
                    xpath = '//textarea[@name="link[message_bottom][' + str(count) + '][ja]"]'
                    if self.dom_loading_wait(xpath):
                        self.clear_text(xpath)
                        self.item_send(xpath, array_value['ボタン下コメント'])
            else:
                # 画面上の「リンク設定」はonなので、offにする
                if display_swtch == 'on':
                    xpath = '//input[@name="link[useGroup]"]'
                    if self.dom_loading_wait(xpath):
                        element = self.driver.find_element_by_xpath(xpath)
                        element.click()
                        # Ajax読み込み待機
                        self.ajax_loading_wait('//div[@class="loading"]/img')
            self.item_send_element_key_by_name('textarea', 'メッセージ下', 'message_bottom[ja]', array)
            self.set_question_redirect_api('外部連結　終了通知API', 'api_type', array)
            # GATEに設定するをONにしたいとき
            if array.get('GATE') is None:
                pass
            else:
                if array['GATE'].get('GATEに設定する') is None:
                    pass
                else:
                    if array['GATE']['GATEに設定する'] == 'on':
                        display_swtch = self.get_item_checkbox('//input[@name="uchikiri"]')
                        # 画面上の「GATEに設定する」はoffなので、onにする
                        if display_swtch == 'off':
                            xpath = '//input[@name="uchikiri"]'
                            if self.dom_loading_wait(xpath):
                                element = self.driver.find_element_by_xpath(xpath)
                                element.click()
        except Exception as exc:
            print(exc)










    # [基本 - 出力]---------------------------------------------------------------
    # 選択された要素のラベル名を取得
    def get_item_label(self, xpath, array):
        try:
            if self.dom_loading_wait(xpath):
                elements = self.driver.find_elements_by_xpath(xpath)
                count = 0
                for element in elements:
                    if element.is_selected():
                        return array[count]
                    count += 1
            return False
        except Exception as exc:
            print(exc)

    # チェックボックス要素の選択状況(on/off)を取得
    def get_item_checkbox(self, xpath, array=''):
        try:
            if self.dom_loading_wait(xpath):
                elements = self.driver.find_elements_by_xpath(xpath)
                count = 0
                if len(elements) == 1:
                    if elements[0].is_selected():
                        return 'on'
                    else:
                        return 'off'
                else:
                    for element in elements:
                        if element.is_selected():
                            array[count] = 'on'
                        else:
                            array[count] = 'off'
                        count += 1
                    return array
            return False
        except Exception as exc:
            print(exc)

    # チェックボックス要素の選択状況(on)のときValue値を返却
    def get_item_checkbox_on_value(self, xpath, array):
        try:
            if self.dom_loading_wait(xpath):
                elements = self.driver.find_elements_by_xpath(xpath)
                if len(elements) == 1:
                    element = self.driver.find_element_by_xpath(xpath)
                    if element.is_selected():
                        return array.append(element.get_attribute('value'))
                    else:
                        return array
                else:
                    for element in elements:
                        if element.is_selected():
                            array.append(element.get_attribute('value'))
                    return array
            return False
        except Exception as exc:
            print(exc)

    # 要素から文字(value)を取得する
    def get_item_text(self, xpath):
        try:
            content = ''
            if self.dom_loading_wait(xpath):
                elements = self.driver.find_elements_by_xpath(xpath)
                for element in elements:
                    content += str(element.get_attribute('value'))
                return content
            return False
        except Exception as exc:
            print(exc)

    # selct要素から文字(value値のプルダウン名)を取得する
    def get_item_select(self, xpath):
        try:
            content = ''
            # if self.dom_loading_wait(xpath):
            elements = self.driver.find_elements_by_xpath(xpath)
            for element in elements:
                xpath += '/option[@value="' + str(element.get_attribute('value')) + '"]'
                if self.dom_loading_wait(xpath):
                    content += str(self.driver.find_element_by_xpath(xpath).text)
            return content
            # return False
        except Exception as exc:
            print(exc)

    # [応用 - 出力]---------------------------------------------------------------
    # MYリサーチ一覧 - 表示されたプロジェクトを数える
    def get_number_of_displayed_project(self):
        try:
            xpath = '//label[starts-with(@for, "rgrID")]'
            return len(self.driver.find_elements_by_xpath(xpath))
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - 設定済みの設問を数える
    def get_count_set_questions(self):
        try:
            xpath = '//input[@name="qu_id_check[]"]'
            all_question_count = len(self.driver.find_elements_by_xpath(xpath))
            all_unset_question_count = self.get_count_unset_questions()
            all_set_question_count = all_question_count - all_unset_question_count
            return all_set_question_count
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - 未設定の設問を数える
    def get_count_unset_questions(self):
        try:
            xpath = '//span[starts-with(@class, "unsetting")]'
            unset_question_count = len(self.driver.find_elements_by_xpath(xpath))
            return unset_question_count
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - ENDページを数える
    def get_count_unset_end_pages(self):
        try:
            xpath = '//input[@type="checkbox"][@name="pg_id_check[]"]'
            return len(self.driver.find_elements_by_xpath(xpath))
        except Exception as exc:
            print(exc)

    # 設問編集 - リサーチNoを取得
    def get_research_number_of_edit_question(self):
        try:
            xpath = '//div[@class="tableBoxTypeA01"]/table/tbody/tr[@class="first"]/td[1]'
            item_text = self.get_item_text(xpath)
            if item_text == 'None' :
                item_text = self.driver.find_element_by_xpath(xpath).text
            elif item_text == False:
                item_text = 'C999012345'
                print('[エラー] リサーチNoの取得ができませんでした')
                # print(item_text)
            return item_text
        except Exception as exc:
            print(exc)

    # 設問編集 - リサーチ種別を取得
    def get_research_type_of_edit_question(self):
        try:
            xpath = '//div[@class="tableBoxTypeA01"]/table/tbody/tr[@class="end"]/td[1]'
            item_text = self.get_item_text(xpath)
            if item_text == 'None':
                item_text = self.driver.find_element_by_xpath(xpath).text
            return item_text
        except Exception as exc:
            print(exc)

    # 設問編集 - 選択されたラジオボタン要素のラベル名を取得
    def get_item_selected_radio(self, key, element='parent::td[1]'):
        try:
            content = ''
            xpath = '//input[@name="' + str(key) + '"]/' + str(element)
            if self.dom_loading_wait(xpath):
                item_label = self.driver.find_element_by_xpath(xpath).text.split()
                xpath = '//input[@name="' + str(key) + '"]'
                content = self.get_item_label(xpath, item_label)
                return content
            return False
        except Exception as exc:
            print(exc)

    # 設問編集 - 選択されたラジオボタン要素のラベル名を取得：labelで括られている
    def get_item_selected_radio_of_label(self, key):
        try:
            item_label = []
            xpath = '//input[@name="' + str(key) + '"]'
            if self.dom_loading_wait(xpath):
                elements = self.driver.find_elements_by_xpath(xpath)
                item_count = 0
                for element in elements:
                    item_count = item_count + 1
                    id_key = element.get_attribute('id')
                    if len(id_key) == 0:
                        xpath = '//input[@name="' + str(key) + '"]/ancestor::td[1]/label[' + str(item_count) + ']'
                    elif id_key == 'alignImage4' or id_key == 'alignImage5':
                        # 画像（旧式の画像を貼付けるやつ）「並び順」がなぜか他と同じ方法で取得できないからイレギュラー
                        xpath = '//input[@name="' + str(key) + '"]/ancestor::tr/td[' + str(item_count) + ']/label[1]'
                    else:
                        xpath = '//label[@for="' + str(id_key) + '"]'
                    if self.dom_loading_wait(xpath):
                        item_label.append(self.driver.find_element_by_xpath(xpath).text.strip())
                xpath = '//input[@name="' + str(key) + '"]'
                return self.get_item_label(xpath, item_label)
            return False
        except Exception as exc:
            print(exc)

    # 設問編集 - プロフィール設問固有の取得処理
    def get_item_profile(self, value, key, array):
        try:
            array_value = array.get('選択肢').get(value)
            if array_value is None:
                pass
            else:
                # プロフィールのテキスト欄
                xpath = '//input[@name="' + str(key) + '"]'
                array['選択肢'][value][0] = self.get_item_text(xpath)
                # プロフィールの「使用する」チェックボックス
                xpath = '//input[@name="useItemTypeAry[]"][@value="' + str(key[key.find('[') + 1:key.find(']')]) + '"]'
                array['選択肢'][value][1] = self.get_item_checkbox(xpath)
                # プロフィールの「必須にする」チェックボックス
                xpath = '//input[@name="mustItemTypeAry[]"][@value="' + str(key[key.find('[') + 1:key.find(']')]) + '"]'
                array['選択肢'][value][2] = self.get_item_checkbox(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - 現在選択中の設問タイプを取得
    def current_selecting_question_type_get(self):
        try:
            xpath = '//a[contains(@href, "openPreviewColumns")]/parent::li'
            if self.dom_loading_wait(xpath):
                return self.driver.find_element_by_xpath(xpath).text
            return False
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - START,COMPを含めた現在のページ番号を取得
    def get_my_research_page_number_all(self, pages=[], quids=[], pgids=[]):
        try:
            xpath = '//td[@class="pageNo"]/a'
            if self.dom_loading_wait(xpath):
                elements = self.driver.find_elements_by_xpath(xpath)
                for element in elements:
                    pages.append(str(element.text))
                    quid_value = element.get_attribute('href')[element.get_attribute('href').find('(') + 1:element.get_attribute('href').find(')')]
                    if element.text.find('START') == -1 and element.text.find('END') == -1 and element.text.find('COMP') == -1 and element.text.find('GATE') == -1:
                        quids.append(str(quid_value[1:5]))
                    else:
                        quids.append(str(quid_value))
                xpath = '//img[@alt="条"]/parent::a'
                pgids.append(quids[0])
                if self.dom_loading_wait(xpath):
                    elements = self.driver.find_elements_by_xpath(xpath)
                    for element in elements:
                        pgids.append(element.get_attribute('href')[element.get_attribute('href').find('(') + 2:element.get_attribute('href').find(')') - 1])
                pgids.append(quids[len(quids) - 1])
                return pages,quids,pgids
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - START,COMP,END,GATEを含めない現在のページ番号を取得：第一引数はQナンバー、第二はページ番号
    def get_my_research_page_number_only(self, quids=[], pages=[]):
        try:
            xpath = '//td[@class="pageNo"]/a'
            if self.dom_loading_wait(xpath):
                elements = self.driver.find_elements_by_xpath(xpath)
                for element in elements:
                    if element.text.find('START') == -1 and element.text.find('END') == -1 and element.text.find('COMP') == -1 and element.text.find('GATE') == -1:
                        pages.append(str(element.text))
                        quid_value = element.get_attribute('href')[element.get_attribute('href').find('(') + 1:element.get_attribute('href').find(')')]
                        quids.append(str(quid_value[1:5]))
                return quids,pages
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - START,COMP,END,GATEを含めない現在の設問番号と設問タイプを取得（未設定も含まない）
    def get_my_research_page_question_number_and_type(self, questionnumber=[], questiontype=[], quids=[]):
        try:
            xpath = '//td[@class="questionNo"]/a'
            if self.dom_loading_wait(xpath):
                elements = self.driver.find_elements_by_xpath(xpath)
                for element in elements:
                    if element.text.find('終了') == -1:
                        questionnumber.append(str(element.text))
            xpath = '//td[@class="type"]/label/img'
            if self.dom_loading_wait(xpath):
                elements = self.driver.find_elements_by_xpath(xpath)
                for element in elements:
                    if element.get_attribute('alt').find('終了') == -1:
                        questiontype.append(element.get_attribute('alt'))
            xpath = '//td[@class="pageNo"]/a'
            if self.dom_loading_wait(xpath):
                elements = self.driver.find_elements_by_xpath(xpath)
                for element in elements:
                    quid_value = element.get_attribute('href')[element.get_attribute('href').find('(') + 1:element.get_attribute('href').find(')')]
                    if element.text.find('START') == -1 and element.text.find('END') == -1 and element.text.find('COMP') == -1 and element.text.find('GATE') == -1:
                        quids.append(str(quid_value[1:5]))
            # 未設定の設問の questionnumber と quids を削除
            max_length = len(questionnumber)
            for count in range(max_length-1, -1, -1):
                if questionnumber[count] == ' ':
                    questionnumber.pop(count)
                    quids.pop(count)
            return questionnumber,questiontype,quids
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - 現在のQナンバーの中から最大値を取得
    def get_my_research_max_q_number(self):
        try:
            xpath = '//td[@class="pageNo"]/a'
            if self.dom_loading_wait(xpath):
                elements = self.driver.find_elements_by_xpath(xpath)
                max_quid = 0
                for element in elements:
                    quid_value = element.get_attribute('href')[element.get_attribute('href').find('(') + 1:element.get_attribute('href').find(')')]
                    if len(quid_value) >= 6:
                        quid_value = int(quid_value[1:5],10)
                        if max_quid < quid_value:
                            max_quid = quid_value
                return max_quid
        except Exception as exc:
            print(exc)

    # 設問編集 - グループ設定独自のチェックボックス要素を設問で作成可能な形式に加工
    def convert_edit_question_choice_group_by_name(self, value, keys, array, element='parent::td[1]'):
        try:
            # 設問編集 - チェックボックス要素を設問で作成可能な形式に加工
            self.convert_edit_question_checkbox_by_name(value, keys, array, element)
            key = keys['グループ設定する']
            if array[value]['グループ設定する'] == 'on':
                # 90番環境に「グループ数」は存在しないのでグループ数を作成しない
                if self.mode == 'dev4s' or self.mode == '4s90':
                    pass
                else:
                    # グループ設定がONの時グループ数も取得
                    if key == 'choice[normal][useGroup]':
                        xpath = '//select[@name="choice_num"]' 
                    elif key == 'choice[head][useGroup]':
                        xpath = '//select[@name="choice_head_num"]' 
                    elif key == 'choice[side][useGroup]':
                        xpath = '//select[@name="choice[side][blockNum]"]' 
                    array[value]['グループ数'] = self.get_item_select(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - リンク設定独自のチェックボックス要素を設問で作成可能な形式に加工
    def convert_edit_question_link_by_name(self, value, keys, array, element='parent::td[1]'):
        try:
            # 設問編集 - チェックボックス要素を設問で作成可能な形式に加工
            self.convert_edit_question_checkbox_by_name(value, keys, array, element)
            if array[value]['リンク設定する'] == 'on':
                # リンク設定がONの時リンク数も取得
                xpath = '//select[@name="link[choice_num]"]' 
                array[value]['リンク数'] = self.get_item_select(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - グループ対応したテキスト要素を設問で作成可能な形式に加工
    def convert_edit_question_choice_text_by_group(self, element, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                # グループ設定がONのとき
                if array['グループ設定']['グループ設定する'] == 'on':
                    # 90番環境に「グループ数」は存在しないのでloop_countは[1]をセット
                    if self.mode == 'dev4s' or self.mode == '4s90':
                        loop_count = 1
                    else:
                        loop_count = int(array['グループ設定']['グループ数'])
                    array[value] = []
                    for count in range(1, loop_count + 1):
                        key_value = key.replace('1', str(count))
                        array_value = array.get(value)
                        if array_value is None:
                            pass
                        else:
                            xpath = '//' + str(element) + '[@name="' + str(key_value) + '"]'
                            array[value].append(self.get_item_text(xpath))
                # グループ設定がOFFのとき
                else:
                    self.convert_edit_question_text_by_name(element, value, key, array)
        except Exception as exc:
            print(exc)

    # 設問編集 - 要素の文字(value)を設問で作成可能な形式に加工
    def convert_edit_question_text_by_name(self, element, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                xpath = '//' + str(element) + '[@name="' + str(key) + '"]'
                array[value] = self.get_item_text(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - ラジオボタン要素を設問で作成可能な形式に加工
    def convert_edit_question_radio_by_name(self, value, key, array, element='parent::td[1]'):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                array[value] = self.get_item_selected_radio(key, element)
        except Exception as exc:
            print(exc)

    # 設問編集 - ラジオボタン要素を設問で作成可能な形式に加工：labelで括られている
    def convert_edit_question_radio_by_name_of_label(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                array[value] = self.get_item_selected_radio_of_label(key)
        except Exception as exc:
            print(exc)

    # 設問編集 - i-タイル設定を設問で作成可能な形式に加工
    def convert_edit_question_by_itile(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                # 作成予定のQナンバーの取得
                quid = array['Qナンバー']
                # 作成予定の設問タイプの取得
                question_type = array['設問タイプ']
                array[value] = self.get_item_selected_radio_of_label(key)
                if array[value] == '利用する':
                    value = 'i-タイル設定詳細'
                    array[value] = {}
                    array[value]['ページ自動遷移'] = ''
                    if question_type == 'SA(単一選択)':
                        array[value]['ページ自動遷移'] = ''
                        self.convert_edit_question_radio_by_name_of_label('ページ自動遷移', 'i_tile[questions][' + str(quid) + '][auto_next]', array[value])
                        array[value]['ラジオボタン表示'] = ''
                        self.convert_edit_question_radio_by_name_of_label('ラジオボタン表示', 'i_tile[questions][' + str(quid) + '][radio_display]', array[value])
                        array[value]['テキストレイアウト'] = ''
                        self.convert_edit_question_radio_by_name_of_label('テキストレイアウト', 'i_tile[questions][' + str(quid) + '][text_align]', array[value])
                        array[value]['付属テキスト配置'] = ''
                        self.convert_edit_question_radio_by_name_of_label('付属テキスト配置', 'i_tile[questions][' + str(quid) + '][text_place]', array[value])
                        array[value]['高さ'] = ''
                        self.convert_edit_question_text_by_name('input', '高さ', 'i_tile[questions][' + str(quid) + '][height]', array[value])
                        array[value]['幅'] = ''
                        self.convert_edit_question_text_by_name('input', '幅', 'i_tile[questions][' + str(quid) + '][width]', array[value])
                        array[value]['回答の列数'] = ''
                        self.convert_edit_question_text_by_name('input', '回答の列数', 'i_tile[questions][' + str(quid) + '][column]', array[value])
                        array[value]['並び順'] = self.get_item_select('//select[@name="i_tile[questions][' + str(quid) + '][alignment]"]').strip()
                    elif question_type == 'MA(複数選択)':
                        array[value]['チェックボックス表示'] = ''
                        self.convert_edit_question_radio_by_name_of_label('チェックボックス表示', 'i_tile[questions][' + str(quid) + '][checkbox_display]', array[value])
                        array[value]['テキストレイアウト'] = ''
                        self.convert_edit_question_radio_by_name_of_label('テキストレイアウト', 'i_tile[questions][' + str(quid) + '][text_align]', array[value])
                        array[value]['付属テキスト配置'] = ''
                        self.convert_edit_question_radio_by_name_of_label('付属テキスト配置', 'i_tile[questions][' + str(quid) + '][text_place]', array[value])
                        array[value]['高さ'] = ''
                        self.convert_edit_question_text_by_name('input', '高さ', 'i_tile[questions][' + str(quid) + '][height]', array[value])
                        array[value]['幅'] = ''
                        self.convert_edit_question_text_by_name('input', '幅', 'i_tile[questions][' + str(quid) + '][width]', array[value])
                        array[value]['回答の列数'] = ''
                        self.convert_edit_question_text_by_name('input', '回答の列数', 'i_tile[questions][' + str(quid) + '][column]', array[value])
                        array[value]['並び順'] = self.get_item_select('//select[@name="i_tile[questions][' + str(quid) + '][alignment]"]').strip()
                    elif question_type == 'マトリクスSA':
                        array[value]['ページ自動遷移'] = ''
                        self.convert_edit_question_radio_by_name_of_label('ページ自動遷移', 'i_tile[questions][' + str(quid) + '][auto_next]', array[value])
                        array[value]['ラジオボタン表示'] = ''
                        self.convert_edit_question_radio_by_name_of_label('ラジオボタン表示', 'i_tile[questions][' + str(quid) + '][radio_display]', array[value])
                        array[value]['戻るボタン表示'] = ''
                        self.convert_edit_question_radio_by_name_of_label('戻るボタン表示', 'i_tile[questions][' + str(quid) + '][display_back_btn]', array[value])
                        array[value]['次を表示ボタン'] = ''
                        self.convert_edit_question_radio_by_name_of_label('次を表示ボタン', 'i_tile[questions][' + str(quid) + '][display_next_btn]', array[value])
                        array[value]['テキストレイアウト'] = ''
                        self.convert_edit_question_radio_by_name_of_label('テキストレイアウト', 'i_tile[questions][' + str(quid) + '][text_align]', array[value])
                        array[value]['付属テキスト配置'] = ''
                        self.convert_edit_question_radio_by_name_of_label('付属テキスト配置', 'i_tile[questions][' + str(quid) + '][text_place]', array[value])
                        array[value]['高さ'] = ''
                        self.convert_edit_question_text_by_name('input', '高さ', 'i_tile[questions][' + str(quid) + '][height]', array[value])
                        array[value]['幅'] = ''
                        self.convert_edit_question_text_by_name('input', '幅', 'i_tile[questions][' + str(quid) + '][width]', array[value])
                        array[value]['回答の列数'] = ''
                        self.convert_edit_question_text_by_name('input', '回答の列数', 'i_tile[questions][' + str(quid) + '][column]', array[value])
                        array[value]['並び順'] = self.get_item_select('//select[@name="i_tile[questions][' + str(quid) + '][alignment]"]').strip()
                    elif question_type == 'マトリクスMA':
                        array[value]['ページ自動遷移'] = ''
                        self.convert_edit_question_radio_by_name_of_label('ページ自動遷移', 'i_tile[questions][' + str(quid) + '][auto_next]', array[value])
                        array[value]['チェックボックス表示'] = ''
                        self.convert_edit_question_radio_by_name_of_label('チェックボックス表示', 'i_tile[questions][' + str(quid) + '][checkbox_display]', array[value])
                        array[value]['戻るボタン表示'] = ''
                        self.convert_edit_question_radio_by_name_of_label('戻るボタン表示', 'i_tile[questions][' + str(quid) + '][display_back_btn]', array[value])
                        array[value]['テキストレイアウト'] = ''
                        self.convert_edit_question_radio_by_name_of_label('テキストレイアウト', 'i_tile[questions][' + str(quid) + '][text_align]', array[value])
                        array[value]['付属テキスト配置'] = ''
                        self.convert_edit_question_radio_by_name_of_label('付属テキスト配置', 'i_tile[questions][' + str(quid) + '][text_place]', array[value])
                        array[value]['高さ'] = ''
                        self.convert_edit_question_text_by_name('input', '高さ', 'i_tile[questions][' + str(quid) + '][height]', array[value])
                        array[value]['幅'] = ''
                        self.convert_edit_question_text_by_name('input', '幅', 'i_tile[questions][' + str(quid) + '][width]', array[value])
                        array[value]['回答の列数'] = ''
                        self.convert_edit_question_text_by_name('input', '回答の列数', 'i_tile[questions][' + str(quid) + '][column]', array[value])
                        array[value]['並び順'] = self.get_item_select('//select[@name="i_tile[questions][' + str(quid) + '][alignment]"]').strip()
                    elif question_type == 'マトリクス混合':
                        array[value]['ページ自動遷移'] = ''
                        self.convert_edit_question_radio_by_name_of_label('ページ自動遷移', 'i_tile[questions][' + str(quid) + '][auto_next]', array[value])
                        array[value]['ラジオボタン表示'] = ''
                        self.convert_edit_question_radio_by_name_of_label('ラジオボタン表示', 'i_tile[questions][' + str(quid) + '][radio_display]', array[value])
                        array[value]['チェックボックス表示'] = ''
                        self.convert_edit_question_radio_by_name_of_label('チェックボックス表示', 'i_tile[questions][' + str(quid) + '][checkbox_display]', array[value])
                        array[value]['戻るボタン表示'] = ''
                        self.convert_edit_question_radio_by_name_of_label('戻るボタン表示', 'i_tile[questions][' + str(quid) + '][display_back_btn]', array[value])
                        array[value]['次を表示ボタン'] = ''
                        self.convert_edit_question_radio_by_name_of_label('次を表示ボタン', 'i_tile[questions][' + str(quid) + '][display_next_btn]', array[value])
                        array[value]['テキストレイアウト'] = ''
                        self.convert_edit_question_radio_by_name_of_label('テキストレイアウト', 'i_tile[questions][' + str(quid) + '][text_align]', array[value])
                        array[value]['付属テキスト配置'] = ''
                        self.convert_edit_question_radio_by_name_of_label('付属テキスト配置', 'i_tile[questions][' + str(quid) + '][text_place]', array[value])
                        array[value]['高さ'] = ''
                        self.convert_edit_question_text_by_name('input', '高さ', 'i_tile[questions][' + str(quid) + '][height]', array[value])
                        array[value]['幅'] = ''
                        self.convert_edit_question_text_by_name('input', '幅', 'i_tile[questions][' + str(quid) + '][width]', array[value])
                        array[value]['回答の列数'] = ''
                        self.convert_edit_question_text_by_name('input', '回答の列数', 'i_tile[questions][' + str(quid) + '][column]', array[value])
                        array[value]['並び順'] = self.get_item_select('//select[@name="i_tile[questions][' + str(quid) + '][alignment]"]').strip()
                    elif question_type == 'SD法':
                        array[value]['ページ自動遷移'] = ''
                        self.convert_edit_question_radio_by_name_of_label('ページ自動遷移', 'i_tile[questions][' + str(quid) + '][auto_next]', array[value])
                        array[value]['ラジオボタン表示'] = ''
                        self.convert_edit_question_radio_by_name_of_label('ラジオボタン表示', 'i_tile[questions][' + str(quid) + '][radio_display]', array[value])
                        array[value]['戻るボタン表示'] = ''
                        self.convert_edit_question_radio_by_name_of_label('戻るボタン表示', 'i_tile[questions][' + str(quid) + '][display_back_btn]', array[value])
                        array[value]['次を表示ボタン'] = ''
                        self.convert_edit_question_radio_by_name_of_label('次を表示ボタン', 'i_tile[questions][' + str(quid) + '][display_next_btn]', array[value])
                        array[value]['テキストレイアウト'] = ''
                        self.convert_edit_question_radio_by_name_of_label('テキストレイアウト', 'i_tile[questions][' + str(quid) + '][text_align]', array[value])
                        array[value]['付属テキスト配置'] = ''
                        self.convert_edit_question_radio_by_name_of_label('付属テキスト配置', 'i_tile[questions][' + str(quid) + '][text_place]', array[value])
                        array[value]['高さ'] = ''
                        self.convert_edit_question_text_by_name('input', '高さ', 'i_tile[questions][' + str(quid) + '][height]', array[value])
                        array[value]['幅'] = ''
                        self.convert_edit_question_text_by_name('input', '幅', 'i_tile[questions][' + str(quid) + '][width]', array[value])
                        array[value]['回答の列数'] = ''
                        self.convert_edit_question_text_by_name('input', '回答の列数', 'i_tile[questions][' + str(quid) + '][column]', array[value])
                        array[value]['並び順'] = self.get_item_select('//select[@name="i_tile[questions][' + str(quid) + '][alignment]"]').strip()
        except Exception as exc:
            print(exc)

    # 設問編集 - チェックボックス要素を設問で作成可能な形式に加工
    def convert_edit_question_checkbox_by_name(self, value, keys, array, element='parent::td[1]'):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                for key in keys:
                    xpath = '//input[@name="' + str(keys[key]) + '"]/' + str(element)
                    if self.dom_loading_wait(xpath):
                        item_list = self.driver.find_element_by_xpath(xpath).text.split()
                        for key in keys:
                            array[value] = {}
                            xpath = '//input[@name="' + str(keys[key]) + '"]'
                            array[value][key] = self.get_item_checkbox(xpath, item_list)
        except Exception as exc:
            print(exc)

    # 設問編集 - 設問タイプを設問で作成可能な形式に加工
    def convert_edit_question_selecting_question_type(self, value, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                array[value] = self.current_selecting_question_type_get()
        except Exception as exc:
            print(exc)

    # 設問編集 - 設問Noを設問で作成可能な形式に加工
    def convert_edit_question_selecting_question_number(self, value, array):
        try:
            element = self.driver.find_elements_by_xpath('//input[@name="no"]')
            if len(element) > 0:
                self.convert_edit_question_text_by_name('input', '設問No', 'no', array)
                # 設問No表示有無
                array['設問No表示'] = self.get_item_selected_radio('numberView')
            else:
                # 設問編集 - 設問番号を抽出
                xpath = '//span[@id="aId"]/parent::td'
                aId = self.driver.find_element_by_xpath(xpath).text.split()[0]
                array[value] = str(aId)
        except Exception as exc:
            print(exc)

    # 設問編集 - エラーチェックを設問で作成可能な形式に加工
    def convert_edit_question_error_check_process(self, value, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                xpath = '//tr[starts-with(@id, "errorcheck_")]'
                if self.dom_loading_wait(xpath):
                    elements = self.driver.find_elements_by_xpath(xpath)
                    for element in elements:
                        count = element.get_attribute('id')[11]
                        value_child = '条件 ' + str(count)
                        array[value][value_child] = {'メッセージ': '', '条件式': ''}
                        xpath = '//textarea[@name="errorcheck_messages[' + str(count) + '][ja]"]'
                        array[value][value_child]['メッセージ'] = self.get_item_text(xpath)
                        xpath = '//textarea[@name="errorcheck_syntaxes[' + str(count) + ']"]'
                        array[value][value_child]['条件式'] = self.get_item_text(xpath)
        except Exception as exc:
            print(exc)

    # 設問編集 - MA(複数選択) - 選択個数制限の設定を設問で作成可能な形式に加工
    def convert_edit_question_selection_count_limit(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                array_value = array.get(value)
                if array_value is None:
                    pass
                else:
                    content = self.get_item_selected_radio_of_label(key)
                    if content == False:
                        array[value] = ''
                    else:
                        array[value] = str(content)
                        if array[value] == '制限あり':
                            array[value] = [array[value], self.get_item_text('//input[@name="limitNum"]'), self.get_item_select('//select[@name="limitType"]')]
                            if array[value][2] == 'から':
                                array[value].append(self.get_item_text('//input[@name="limitNum2"]'))
        except Exception as exc:
            print(exc)

    # 設問編集 - 数値 - 合計値制限の設定を設問で作成可能な形式に加工
    def convert_edit_question_selection_total_count_limit(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                array_value = array.get(value)
                if array_value is None:
                    # return ''
                    pass
                else:
                    xpath = '//input[@name="' + str(key) + '"]'
                    item_label = ['制限あり', '制限なし']
                    array[value] = self.get_item_label(xpath, item_label)
                    if array[value] == '制限あり':
                        array[value] = [array[value], self.get_item_text('//input[@name="limitTotalMin"]'), self.get_item_text('//input[@name="limitTotalMax"]')]
        except Exception as exc:
            print(exc)

    # 設問編集 - 抽選機能の設定を設問で作成可能な形式に加工
    def convert_edit_question_lottery_count(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                self.convert_edit_question_radio_by_name('抽選機能', 'lottery', array)
                if array['抽選機能'] != '設定しない':
                    if array['設問タイプ'] == '隠し設問MA':
                        array[value] = [array[value], self.get_item_text('//input[@name="lotteryCount"]')]
                    array['打切り設定連動機能'] = ''
                elif array in '打切り設定連動機能':
                    array.remove('打切り設定連動機能')
        except Exception as exc:
            print(exc)

    # 設問編集 - 打切り連動設定
    def convert_edit_question_gate_interlock(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                if len(array['抽選機能']) > 1:
                    if array['抽選機能'][0] != '設定しない':
                        xpath = '//input[@name="' + str(key) + '"]'
                        if self.dom_loading_wait(xpath):
                            elements = self.driver.find_elements_by_xpath(xpath)
                            if elements[0].is_selected():
                                array[value] = 'on'
                            else:
                                array[value] = 'off'
                        else:
                            array[value] = False
                if len(array['打切り設定連動機能']) == 0:
                    array['打切り設定連動機能'] = 'off'
        except Exception as exc:
            print(exc)

    # 設問編集 - プロフィール設問の選択肢
    def convert_edit_question_choice_text_by_profile(self, value, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                for array_value_child in array_value:
                    if array_value_child == '氏名':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[name][ja]', array)
                    if array_value_child == '氏名（ふりがな）':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[name_k][ja]', array)
                    if array_value_child == 'あなたの生年月日':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[birthday][ja]', array)
                    if array_value_child == 'あなたの性別':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[sex][ja]', array)
                    if array_value_child == '郵便番号':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[postcode][ja]', array)
                    if array_value_child == '住所（都道府県）':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[prefecture][ja]', array)
                    if array_value_child == '住所（市区町村）':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[city][ja]', array)
                    if array_value_child == '住所（町名・番地・ビル名など）':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[street][ja]', array)
                    if array_value_child == '電話番号':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[tel][ja]', array)
                    if array_value_child == '携帯電話番号':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[mobile_tel][ja]', array)
                    if array_value_child == 'メールアドレス':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[email][ja]', array)
                    if array_value_child == 'メールアドレス確認用':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[email_c][ja]', array)
                    if array_value_child == '会社名':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[company][ja]', array)
                    if array_value_child == '支店名・営業所名':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[branch][ja]', array)
                    if array_value_child == '部署名':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[post][ja]', array)
                    if array_value_child == 'メールアドレス(＠区切り無し)':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[email_not_delimitation][ja]', array)
                    if array_value_child == 'メールアドレス確認用(＠区切り無し)':
                        self.get_item_profile(array_value_child, 'captionItemTypeAry[email_not_delimitation_c][ja]', array)
        except Exception as exc:
            print(exc)

    # 設問編集 - 外部連携の戻り先情報を設問で作成可能な形式に加工
    def convert_edit_question_external_status(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                xpath = '//input[@name="' + str(key) + '"]'
                if self.dom_loading_wait(xpath):
                    elements = self.driver.find_elements_by_xpath(xpath)
                    if len(elements) == 0:
                        array[value] = elements[0].get_attribute('value')
                    else:
                        array[value] = []
                        for element in elements:
                            array[value].append(element.get_attribute('value'))
                else:
                    array[value] = False
        except Exception as exc:
            print(exc)

    # 設問編集 - スタートページ表示の要素を設問で作成可能な形式に加工
    def convert_edit_question_radio_by_start_page(self, value, key, array, element='parent::td[1]'):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                array[value] = self.get_item_selected_radio(key, element)
                # false のときは「表示する」配列を削除
                if array[value] == False:
                    del array[value]
        except Exception as exc:
            print(exc)

    # 設問編集 - COMPの自動リダイレクトを設問で作成可能な形式に加工
    def convert_edit_question_redirect(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                research_type = self.get_research_type_of_edit_question()
                if research_type == 'クローズドモニタ' or research_type == 'モニタプラス（Mapps Panel）':
                    redirect_timer = self.get_item_text('//input[@name="redirect_timer"]')
                    redirect_url = self.get_item_text('//input[@name="redirect_url"]')
                    # クローズドは「指定する/しない」ラジオボタンが無いのでパラメータ値の有無でボタンを疑似セット
                    if len(redirect_timer) == 0 or len(redirect_url) == 0:
                        array[value] = '指定しない'
                    else:
                        array[value] = []
                        array[value].append('指定')
                    array[value].append(redirect_timer)
                    array[value].append(redirect_url)
                elif research_type == 'オープン':
                    xpath = '//input[@name="' + str(key) + '"]'
                    array[value] = self.get_item_label(xpath, ['指定しない', '指定'])
                    if array[value] == '指定':
                        array[value] = []
                        array[value].append('指定')
                        array[value].append(self.get_item_text('//input[@name="redirect_timer"]'))
                        array[value].append(self.get_item_text('//input[@name="redirect_url"]'))
        except Exception as exc:
            print(exc)

    # 設問編集 - COMPの外部連結　終了通知APIを設問で作成可能な形式に加工
    def convert_edit_question_redirect_api(self, value, key, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                research_type = self.get_research_type_of_edit_question()
                if research_type == 'クローズドモニタ' or research_type == 'モニタプラス（Mapps Panel）':
                    array[value] = '指定しない'
                if research_type == 'オープン':
                    xpath = '//input[@name="' + str(key) + '"]'
                    array[value] = self.get_item_label(xpath, ['指定しない', '指定'])
                    if array[value] == '指定':
                        array[value] = []
                        array[value].append('指定')
                        array[value].append(self.get_item_text('//input[@name="api_url"]'))
        except Exception as exc:
            print(exc)

    # 設問編集 - 設定情報を取得
    def convert_edit_question_by_page(self, page, array):
        try:
            if page == 'START':
                self.get_setting_information_of_start_page(array)
            elif page == 'COMP' or page.find('END') > -1:
                self.get_setting_information_of_comp_page(array)
            elif page == 'GATE':
                self.get_setting_information_of_gate_page(array)
            else:
                # 現在選択中設問タイプ
                question_type = self.current_selecting_question_type_get()
                # 設問編集
                if question_type == 'SA(単一選択)':
                    self.get_setting_information_of_single_answer(array)
                elif question_type == 'MA(複数選択)':
                    self.get_setting_information_of_multi_answer(array)
                elif question_type == '数値':
                    self.get_setting_information_of_number_answer(array)
                elif question_type == '隠し設問SA':
                    self.get_setting_information_of_hidden_single_answer(array)
                elif question_type == '自由記入短文':
                    self.get_setting_information_of_freeshort_answer(array)
                elif question_type == '自由記入長文':
                    self.get_setting_information_of_freelong_answer(array)
                elif question_type == '隠し設問MA':
                    self.get_setting_information_of_hidden_multi_answer(array)
                elif question_type == '画像アップロード':
                    self.get_setting_information_of_image_upload_answer(array)
                elif question_type == 'マトリクスSA':
                    self.get_setting_information_of_matrix_single_answer(array)
                elif question_type == 'マトリクスMA':
                    self.get_setting_information_of_matrix_multi_answer(array)
                elif question_type == 'マトリクス混合':
                    self.get_setting_information_of_matrix_mix_answer(array)
                elif question_type == '文章・画像のみ':
                    self.get_setting_information_of_through_answer(array)
                elif question_type == 'プロフィール':
                    self.get_setting_information_of_profile_answer(array)
                elif question_type == 'SD法':
                    self.get_setting_information_of_matrix_sd_answer(array)
                elif question_type == '登録情報設問':
                    self.get_setting_information_of_attribute_answer(array)
                elif question_type == '外部連携設問':
                    self.get_setting_information_of_post_external_answer(array)
        except Exception as exc:
            print(exc)

    # 設問編集 - 登録情報設問の属性タイプを設問で作成可能な形式に加工
    def convert_edit_question_attribute_type(self, value, key, array, element='parent::td[1]'):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                attribute_value = ''
                xpath = '//input[@name="' + str(key) + '"]/' + str(element)
                if self.dom_loading_wait(xpath):
                    item_label = self.driver.find_element_by_xpath(xpath).text.split()
                    xpath = '//input[@name="' + str(key) + '"]'
                    if self.is_wait_until_element_displayed(xpath):
                        elements = self.driver.find_elements_by_xpath(xpath)
                        for element in elements:
                            if element.is_selected():
                                attribute_value = element.get_attribute('value')
                        if attribute_value == 'sex_sa':
                            array[value] = item_label[0]
                        elif attribute_value == 'age_sa':
                            array[value] = item_label[1]
                        elif attribute_value == 'age_fa':
                            array[value] = item_label[2]
                        elif attribute_value == 'area_sa':
                            array[value] = item_label[3]
                    else:
                        array[value] = False
                else:
                    array[value] = False
        except Exception as exc:
            print(exc)

    # 設問編集 - ランダム引き継ぎ要素を設問で作成可能な形式に加工
    def convert_edit_question_randomize(self, value, key, array, element='parent::td[1]'):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                xpath = '//input[@name="' + str(key.replace('orderlogic', 'useOrderRef')) + '"]'
                randomize_check = self.get_item_checkbox(xpath)
                # 表示順を引き継ぐチェックがONのとき
                if randomize_check == 'on':
                    # array[value] = ['on', self.get_item_select('//select[@name="' + str(key.replace('orderlogic', 'orderRef')) + '"]')]
                    array[value] = 'on/' + self.get_item_select('//select[@name="' + str(key.replace('orderlogic', 'orderRef')) + '"]')
                # 表示順を引き継ぐチェックがOFFなので通常通りランダム取得
                else:
                    array[value] = self.get_item_selected_radio(key, element)
        except Exception as exc:
            print(exc)

    # 設問編集 - ランダマイズ要素を設問で作成可能な形式に加工
    def convert_edit_question_randomize_by_group(self, value, key, array, element='parent::td[1]'):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                # グループ設定がONのとき
                if array['グループ設定']['グループ設定する'] == 'on':
                    # 90番環境に「グループ設定」時の「ランダマイズ」は存在しないので処理をスキップ
                    if self.mode == 'dev4s' or self.mode == '4s90':
                        if array.get('ランダマイズ') is not None:
                            del array['ランダマイズ']
                    else:
                        loop_count = int(array['グループ設定']['グループ数'])
                        array[value] = []
                        for count in range(1, loop_count + 1):
                            xpath = '//input[@name="' + str(key.replace('orderlogic', 'useOrderRef')) + '"]'
                            xpath = xpath.replace('1', str(count))
                            randomize_check = self.get_item_checkbox(xpath)
                            # 表示順を引き継ぐチェックがONのとき
                            if randomize_check == 'on':
                                # key_value = key.replace('1', str(count))
                                # array[value].append(['on', self.get_item_select('//select[@name="' + str(key.replace('orderlogic', 'orderRef')) + '"]'.replace('1', str(count)))])
                                array[value].append('on/' + self.get_item_select('//select[@name="' + str(key.replace('orderlogic', 'orderRef')) + '"]'.replace('1', str(count))))
                            # 表示順を引き継ぐチェックがOFFなので通常通りランダム取得
                            else:
                                key_value = key.replace('1', str(count))
                                array_value = array.get(value)
                                if array_value is None:
                                    pass
                                else:
                                    array[value].append(self.get_item_selected_radio(key_value, element))
                else:
                    # グループ設定がOFFのとき
                    xpath = '//input[@name="' + str(key.replace('orderlogic', 'useOrderRef')) + '"]'
                    randomize_check = self.get_item_checkbox(xpath)
                    # 表示順を引き継ぐチェックがONのとき
                    if randomize_check == 'on':
                        # array[value] = ['on', self.get_item_select('//select[@name="' + str(key.replace('orderlogic', 'orderRef')) + '"]')]
                        array[value] = 'on/' + self.get_item_select('//select[@name="' + str(key.replace('orderlogic', 'orderRef')) + '"]')
                    # 表示順を引き継ぐチェックがOFFなので通常通りランダム取得
                    else:
                        array[value] = self.get_item_selected_radio(key, element)
        except Exception as exc:
            print(exc)

    # 設問編集 - 終了ページの終了タイプ要素を設問で作成可能な形式に加工
    def convert_edit_question_end_type(self, value, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                xpath = '//table[@class="tableBoxTypeD01"]/tbody/tr[2]/td'
                item_text = self.get_item_text(xpath)
                if item_text == 'None':
                    item_text = self.driver.find_element_by_xpath(xpath).text
                array[value] = item_text
        except Exception as exc:
            print(exc)

    # 設問編集 - ページ設定を設問で作成可能な形式に加工
    def convert_edit_question_setting_page(self, value, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                # サブウインドウをクリック
                self.action_sub_window_click(value)
                # 子ウインドウが表示されるまで待って切り替える
                count = 0
                retry = 1
                while True:
                    if len(self.driver.window_handles) > 1:
                        break
                    if count >= 150 and retry > 0:
                        # 15秒経過して window_handles が 1つのとき再度クリック
                        print('[子ウインドウ]-------------------------------')
                        print('リトライしました' + str(count) + 'ミリ秒')
                        retry -= 1
                        count = 0
                        # サブウインドウを再度クリック
                        self.action_sub_window_click(value)
                    if count >= 300:
                        print('[子ウインドウ]-------------------------------')
                        print('タイムアウト:' + str(count) + 'ミリ秒')
                        break
                    # self.time.sleep(0.1)
                    count += 1
                all_handles = self.driver.window_handles
                self.driver.switch_to_window(all_handles[1])
                # self.time.sleep(0.5)
                # 各サブウインドウ毎の操作
                # タグ
                if array_value.get('タグ') is None:
                    pass
                else:
                    array_value['タグ'] = self.get_item_text('//textarea[@name="data[tag]"]')
                # ページヘッダー文言
                if array_value.get('ページヘッダー文言') is None:
                    pass
                else:
                    array_value['ページヘッダー文言'] = self.get_item_text('//textarea[@name="data[header]"]')
                # ページフッター文言
                if array_value.get('ページフッター文言') is None:
                    pass
                else:
                    array_value['ページフッター文言'] = self.get_item_text('//textarea[@name="data[footer]"]')
                # 閉じる
                self.item_click('//span[@class="linkTypeA20"]/a')
                # 親ウインドウへ戻る
                self.driver.switch_to_window(all_handles[0])
                self.time.sleep(0.5)
        except Exception as exc:
            print(exc)

    # 設問編集 - メッセージ編集を設問で作成可能な形式に加工
    def convert_edit_question_system_message(self, value, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                # サブウインドウをクリック
                self.action_sub_window_click(value)
                # 子ウインドウが表示されるまで待って切り替える
                count = 0
                retry = 1
                while True:
                    if len(self.driver.window_handles) > 1:
                        break
                    if count >= 150 and retry > 0:
                        # 15秒経過して window_handles が 1つのとき再度クリック
                        print('[子ウインドウ]-------------------------------')
                        print('リトライしました' + str(count) + 'ミリ秒')
                        retry -= 1
                        count = 0
                        # サブウインドウを再度クリック
                        self.action_sub_window_click(value)
                    if count >= 300:
                        print('[子ウインドウ]-------------------------------')
                        print('タイムアウト:' + str(count) + 'ミリ秒')
                        break
                    # self.time.sleep(0.1)
                    count += 1
                all_handles = self.driver.window_handles
                self.driver.switch_to_window(all_handles[1])
                # self.time.sleep(0.5)
                # 各サブウインドウ毎の操作
                # システムエラーメッセージの編集
                if array_value.get('実査開始前アクセスエラー') is None:
                    pass
                else:
                    array_value['実査開始前アクセスエラー'] = self.get_item_text('//input[@name="data[research_not_yet_open]"]')
                # 実査中(打切り)エラー
                if array_value.get('実査中(打切り)エラー') is None:
                    pass
                else:
                    array_value['実査中(打切り)エラー'] = self.get_item_text('//input[@name="data[research_reached]"]')
                # 実査中(重複回答)エラー
                if array_value.get('実査中(重複回答)エラー') is None:
                    pass
                else:
                    array_value['実査中(重複回答)エラー'] = self.get_item_text('//input[@name="data[research_answered]"]')
                # 実査終了後アクセスエラー
                if array_value.get('実査終了後アクセスエラー') is None:
                    pass
                else:
                    array_value['実査終了後アクセスエラー'] = self.get_item_text('//input[@name="data[research_closed]"]')
                # -------------------------------------------------------------------------------------------------------------
                # アンケート回答の「次へ」「戻る」ボタン名称の編集
                if array_value.get('開始ページのボタン名称') is None:
                    pass
                else:
                    array_value['開始ページのボタン名称'] = self.get_item_text('//input[@name="data[start_next]"]')
                # 次へボタン名称
                if array_value.get('次へボタン名称') is None:
                    pass
                else:
                    array_value['次へボタン名称'] = self.get_item_text('//input[@name="data[next]"]')
                # 戻るボタン名称
                if array_value.get('戻るボタン名称') is None:
                    pass
                else:
                    array_value['戻るボタン名称'] = self.get_item_text('//input[@name="data[back]"]')
                # 閉じる
                self.item_click('//span[@class="linkTypeA51"]/a')
                # 親ウインドウへ戻る
                self.driver.switch_to_window(all_handles[0])
                self.time.sleep(0.5)
        except Exception as exc:
            print(exc)

    # 設問編集 - 画像の要素を設問で作成可能な形式に加工
    def convert_edit_question_image_setting(self, value, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                # 画像
                array[value] = self.get_item_selected_radio_of_label('insertImage')
                if array[value] != '表示しない':
                    array['画像詳細設定'] = {}
                    array['画像詳細設定']['表示位置'] = ''
                    array['画像詳細設定']['画像寄せ'] = ''
                    array['画像詳細設定']['並び順'] = ''
                    array['画像詳細設定']['上段コメント'] = ''
                    array['画像詳細設定']['画像ファイル'] = {}
                    array['画像詳細設定']['画像ファイル'] = ['','','']
                    array['画像詳細設定']['サムネイル画像'] = {}
                    array['画像詳細設定']['サムネイル画像'] = ['','','']
                    array['画像詳細設定']['キャプション'] = {}
                    array['画像詳細設定']['キャプション'] = ['','','']
                    self.convert_edit_question_radio_by_name_of_label('表示位置', 'insertImage', array['画像詳細設定'])
                    self.convert_edit_question_radio_by_name_of_label('画像寄せ', 'alignImage', array['画像詳細設定'])
                    self.convert_edit_question_radio_by_name_of_label('並び順', 'alignImageHorVer', array['画像詳細設定'])
                    self.convert_edit_question_text_by_name('textarea', '上段コメント', 'upper_comment[ja]', array['画像詳細設定'])
                    # アップロードボタンがあるかどうかで画像ファイル名の取得方法が違う
                    xpath = '//span[@class="btn-choose-file"]'
                    elements = self.driver.find_elements_by_xpath(xpath)
                    if len(elements) > 0:
                        # アップロード項目（画像ファイル、サムネイル画像、キャプション）の取得
                        xpath = '//span[@class="img-file"]/a'
                        elements = self.driver.find_elements_by_xpath(xpath)
                        for element in elements:
                            count = 0
                            if element.text.find('_1') >= 0:
                                count = 0
                            elif element.text.find('_2') >= 0:
                                count = 1
                            elif element.text.find('_3') >= 0:
                                count = 2
                            # サムネイルなのか判断
                            if element.text.find('thumb_') == -1:
                                # 画像ファイル
                                array['画像詳細設定']['画像ファイル'][count] = element.text
                            else:
                                # サムネイル画像
                                array['画像詳細設定']['サムネイル画像'][count] = element.text
                    else:
                        # 画像ファイル1番目
                        array['画像詳細設定']['画像ファイル'][0] = self.driver.find_element_by_xpath('//input[@name="changeImage0_name"]').get_attribute('value')
                        # サムネイル画像1番目
                        array['画像詳細設定']['サムネイル画像'][0] = self.driver.find_element_by_xpath('//input[@name="changeImage0_thumb_name"]').get_attribute('value')
                        # 画像ファイル2番目
                        array['画像詳細設定']['画像ファイル'][1] = self.driver.find_element_by_xpath('//input[@name="changeImage1_name"]').get_attribute('value')
                        # サムネイル画像2番目
                        array['画像詳細設定']['サムネイル画像'][1] = self.driver.find_element_by_xpath('//input[@name="changeImage1_thumb_name"]').get_attribute('value')
                        # 画像ファイル3番目
                        array['画像詳細設定']['画像ファイル'][2] = self.driver.find_element_by_xpath('//input[@name="changeImage2_name"]').get_attribute('value')
                        # サムネイル画像3番目
                        array['画像詳細設定']['サムネイル画像'][2] = self.driver.find_element_by_xpath('//input[@name="changeImage2_thumb_name"]').get_attribute('value')
                    # キャプション1番目
                    array['画像詳細設定']['キャプション'][0] = self.get_item_text('//textarea[@name="caption1[ja]"]')
                    # キャプション2番目
                    array['画像詳細設定']['キャプション'][1] = self.get_item_text('//textarea[@name="caption2[ja]"]')
                    # キャプション3番目
                    array['画像詳細設定']['キャプション'][2] = self.get_item_text('//textarea[@name="caption3[ja]"]')
        except Exception as exc:
            print(exc)

    # 設問編集 - 動画貼付の要素を設問で作成可能な形式に加工
    def convert_edit_question_video_setting(self, value, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                # 動画貼付
                array[value] = self.get_item_selected_radio_of_label('movieins')
                if array[value] == '動画を貼り付ける':
                    array['動画貼付詳細設定'] = {}
                    array['動画貼付詳細設定']['回答できるようになるまでの時間'] = ''
                    array['動画貼付詳細設定']['自動再生'] = ''
                    array['動画貼付詳細設定']['再再生の可否'] = ''
                    array['動画貼付詳細設定']['セキュリティ設定'] = ''
                    array['動画貼付詳細設定']['キャプション'] = ''
                    self.convert_edit_question_text_by_name('input', '回答できるようになるまでの時間', 'movietime', array['動画貼付詳細設定'])
                    self.convert_edit_question_radio_by_name_of_label('自動再生', 'autostart', array['動画貼付詳細設定'])
                    self.convert_edit_question_radio_by_name_of_label('再再生の可否', 'replay', array['動画貼付詳細設定'])
                    self.convert_edit_question_radio_by_name_of_label('セキュリティ設定', 'security', array['動画貼付詳細設定'])
                    if array['動画貼付詳細設定']['セキュリティ設定'] == False:
                        array['動画貼付詳細設定']['セキュリティ設定'] = 'on'
                    self.convert_edit_question_text_by_name('textarea', 'キャプション', 'captionmovie1[ja]', array['動画貼付詳細設定'])
        except Exception as exc:
            print(exc)

    # 設問編集 - 条件分岐を設問で作成可能な形式に加工
    def convert_edit_question_condition_setting(self, value, question_number, question_type, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                # print('###################################')
                # print(question_number)
                # print(question_type)
                self.convert_edit_question_text_by_name('input', '結合式', 'expression', array_value)
                # 結合式から、結合数を算出
                if array_value['結合式'].find('~') >= 0:
                    conjunction = array_value['結合式'].replace('~OR~', '~').replace('~AND~', '~').replace('~(~', '~').replace('~)~', '~')
                    conjunction = len(conjunction.split('~'))
                else:
                    conjunction = 1
                count = -1
                while True:
                    count += 1
                    if count >= conjunction:
                        return True
                    else:
                        name = 'condition[' + str(count) + ']'
                        if count < 9:
                            array_label = '条件【' + ('0' + str(count+1))[0:2] + '】'
                        else:
                            array_label = '条件【' + str(count+1) + '】'
                        # array_label = '条件【' + ('0' + str(count+1))[0:2] + '】'
                        array_value[array_label] = {}
                        array_value[array_label]['設問文'] = self.get_item_select('//select[@name="' + name + '[refid]"]')
                        array_value[array_label]['対象'] = self.get_item_select('//select[@name="' + name + '[type]"]')
                        array_value[array_label]['次の条件との関係'] = ''
                        # 設問文から設問番号を取得して設問タイプを判定する
                        # print('設問タイプ判定 -> ' + str(array_value[array_label]['設問文']))
                        now_question_number = array_value[array_label]['設問文'].split()[0]
                        now_question_type = question_type[question_number.index(now_question_number)]
                        # print('now_question_number -> ' + str(now_question_number))
                        # print('now_question_type -> ' + str(now_question_type))
                        if now_question_type == 'シングル' or now_question_type == '隠しシングル':
                            self.get_condition_setting_of_single_answer(name, array_value[array_label])
                        elif now_question_type == 'マルチ' or now_question_type == '隠しマルチ':
                            self.get_condition_setting_of_multi_answer(name, array_value[array_label])
                        elif now_question_type == '数値入力' or now_question_type == 'フリー（小）' or now_question_type == 'フリー（大）':
                            self.get_condition_setting_of_text_answer(name, array_value[array_label])
                        elif now_question_type == 'マトリクスシングル' or now_question_type == 'SD法':
                            self.get_condition_setting_of_matrix_single_answer(name, array_value[array_label])
                        elif now_question_type == 'マトリクスマルチ':
                            self.get_condition_setting_of_matrix_multi_answer(name, array_value[array_label])
                        elif now_question_type == 'マトリクス混合':
                            self.get_condition_setting_of_matrix_mix_answer(name, array_value[array_label])
        except Exception as exc:
            print(exc)

    # 90番forSurveyを従来基盤で作成可能な形式に加工
    def convert_new_forsurvey_to_old_forsurvey(self, steps):
        try:
            # print('# 変換前 -----------------------------------')
            # print(steps)
            for step in steps:
                if steps[step].get('ページ番号') is None:
                    pass
                else:
                    # 90番forSurveyの選択肢を従来基盤で作成可能な形式に加工
                    if steps[step].get('設問タイプ') is not None:
                        question_type = steps[step]['設問タイプ']
                        if question_type == 'SA(単一選択)':
                            self.convert_new_forsurvey_choice_to_old_forsurvey(steps[step], '選択肢', 'キャプション', 'ランダマイズ')
                        elif question_type == 'MA(複数選択)':
                            self.convert_new_forsurvey_choice_to_old_forsurvey(steps[step], '選択肢', 'キャプション', 'ランダマイズ')
                        elif question_type == '数値':
                            self.convert_new_forsurvey_choice_to_old_forsurvey(steps[step], '選択肢', 'キャプション', 'ランダマイズ')
                        elif question_type == '隠し設問SA':
                            pass
                        elif question_type == '自由記入短文':
                            self.convert_new_forsurvey_choice_to_old_forsurvey(steps[step], '選択肢', 'キャプション', 'ランダマイズ')
                        elif question_type == '自由記入長文':
                            self.convert_new_forsurvey_choice_to_old_forsurvey(steps[step], '選択肢', 'キャプション', 'ランダマイズ')
                        elif question_type == '隠し設問MA':
                            pass
                        elif question_type == '画像アップロード':
                            self.convert_new_forsurvey_choice_to_old_forsurvey(steps[step], '選択肢', 'キャプション', 'ランダマイズ')
                        elif question_type == 'マトリクスSA':
                            self.convert_new_forsurvey_choice_to_old_forsurvey(steps[step]['表上'], '選択肢', 'キャプション', '選択肢ランダマイズ')
                            self.convert_new_forsurvey_choice_to_old_forsurvey(steps[step]['項目'], '選択肢', 'キャプション', '選択肢ランダマイズ')
                        elif question_type == 'マトリクスMA':
                            self.convert_new_forsurvey_choice_to_old_forsurvey(steps[step]['表上'], '選択肢', 'キャプション', '選択肢ランダマイズ')
                            self.convert_new_forsurvey_choice_to_old_forsurvey(steps[step]['項目'], '選択肢', 'キャプション', '選択肢ランダマイズ')
                        elif question_type == 'マトリクス混合':
                            self.convert_new_forsurvey_choice_to_old_forsurvey(steps[step]['表上'], '選択肢', 'キャプション', '選択肢ランダマイズ')
                            self.convert_new_forsurvey_choice_to_old_forsurvey(steps[step]['項目'], '選択肢', 'キャプション', '選択肢ランダマイズ')
                        elif question_type == '文章・画像のみ':
                            pass
                        elif question_type == 'プロフィール':
                            pass
                        elif question_type == 'SD法':
                            self.convert_new_forsurvey_choice_to_old_forsurvey(steps[step]['表上'], '選択肢', 'キャプション', '選択肢ランダマイズ')
                            self.convert_new_forsurvey_choice_to_old_forsurvey(steps[step]['項目'], '選択肢（表左）', 'キャプション', '選択肢ランダマイズ')
                        elif question_type == '登録情報設問':
                            pass
                        elif question_type == '外部連携設問':
                            pass
                    # # 90番forSurveyにしか存在しないキーを削除
                    # self.delete_new_forsurvey_setting_information(steps[step])
        except Exception as exc:
            print(exc)

    # マトリクス混合を1つずつの設問にバラして作成可能な形式に加工
    def convert_matrix_mix_split(self, quid, array):
        try:
            quid_count = int(quid,10)
            if array.get('設問タイプ') is None:
                return False
            if array['設問タイプ'] != 'マトリクス混合':
                return False
            if array.get('項目') is None:
                return False
            if array['項目'].get('選択肢') is None:
                return False
            if array['項目'].get('グループ設定') is None:
                return False
            if array['項目']['グループ設定'].get('グループ設定する') is None:
                return False
            # グループがoffでも、グループonと処理を共通化したいので配列に変換
            if array['項目']['グループ設定']['グループ設定する'] == 'on':
                pass
            else:
                array_value = array['項目']['選択肢']
                array['項目']['選択肢'] = []
                array['項目']['選択肢'].append(array_value)
                array_value = ''
            # print('###################################################################################')
            # print(array['項目']['選択肢'])
            # print('###################################################################################')
            count = 0
            new_array = {}
            for array_value in array['項目']['選択肢']:
                # print('# [グループ単位]--')
                items = array_value.splitlines()
                for item_text in items:
                    # print(item_text)
                    # print(item_text.find('<fl='))
                    if item_text.find('<sa>') == -1 and item_text.find('<ma>') == -1 and item_text.find('<fs=') == -1 and item_text.find('<fl=') == -1:
                        return False
                    # 配列初期化
                    new_array[str(count)] = {}
                    # 設問タイプにあわせて初期化
                    if item_text.find('<sa>') != -1:
                        new_array[str(count)] = self.set_setting_information('<sa>')
                    elif item_text.find('<ma>') != -1:
                        new_array[str(count)] = self.set_setting_information('<ma>')
                    elif item_text.find('<fs=') != -1:
                        new_array[str(count)] = self.set_setting_information('<fs=')
                    elif item_text.find('<fl=') != -1:
                        new_array[str(count)] = self.set_setting_information('<fl=')
                    # 設問編集(1)
                    new_array[str(count)]['設問タイトル'] = array['設問タイトル']
                    new_array[str(count)]['設問No'] = str(array['設問No']) + '_' + str(count+1)
                    new_array[str(count)]['コメント上'] = array['コメント上']
                    new_array[str(count)]['設問文'] = item_text
                    new_array[str(count)]['コメント中'] = array['コメント中']

                    new_array[str(count)]['グループ設定'] = {}
                    new_array[str(count)]['グループ設定']['グループ設定する'] = 'on'
                    new_array[str(count)]['グループ設定']['グループ数'] = str(len(array['表上']['選択肢']))
                    new_array[str(count)]['選択肢'] = ''
                    new_array[str(count)]['選択肢'] = array['表上']['選択肢']

                    # 設問編集(2)
                    new_array[str(count)]['コメント下'] = array['コメント下']
                    new_array[str(count)]['画像'] = array['画像']
                    new_array[str(count)]['動画貼付'] = array['動画貼付']
                    new_array[str(count)]['備考'] = array['備考']
                    new_array[str(count)]['Javascript(設問表示時)'] = array['Javascript(設問表示時)']
                    new_array[str(count)]['Javascript(次へボタン押下時)'] = array['Javascript(次へボタン押下時)']
                    new_array[str(count)]['ページ情報(headの最後尾)'] = array['ページ情報(headの最後尾)']
                    new_array[str(count)]['エラーチェック'] = array['エラーチェック']
                    # Qナンバー発行
                    quid_count += 1
                    new_quid = ('0000' + str(quid_count))[-4:]
                    new_array[str(count)]['Qナンバー'] = new_quid
                    # ページ番号発行はココではできない
                    count += 1
            return new_array
        except Exception as exc:
            print(exc)

    # 90番forSurveyの選択肢を従来基盤で作成可能な形式に加工
    def convert_new_forsurvey_choice_to_old_forsurvey(self, array, choice_name, caption_name, randomize_name):
        try:
            # print('# 変換前 ' + str(choice_name) + '-----------------------------------')
            # print(array)
            if array.get('グループ設定') is not None:
                # 「グループ設定する」が、on かつ、最初の選択肢の先頭に // が設定されていないと90番ではない
                if array['グループ設定']['グループ設定する'] == 'on' and len(array[choice_name]) == 1 and array[choice_name][0].find('//') == 0:
                    group_count = 0
                    group_item = []
                    array[caption_name] = []
                    array[randomize_name] = []
                    # 選択肢の構造からグループ数、選択肢を再構築
                    for array_value in array[choice_name]:
                        items = array[choice_name][0].splitlines()
                        # グループの中の選択肢（グループ、小グループ含む）総数
                        max_length = len(items)
                        # 初期化
                        group_tmp_item = []
                        # itemsを後ろから走査し、選択肢からグループ、小グループを削除
                        for count in range(max_length-1, -1, -1):
                            if items[count].find('//') == 0:
                                # グループ数カウントUP
                                group_count += 1
                                # キャプション取得
                                temp_item_text = items[count][2:]
                                # ランダマイズ追加
                                if temp_item_text.find('<rand>') != -1:
                                    array[randomize_name].append('ランダム表示')
                                elif temp_item_text.find('<rand_rv>') != -1:
                                    array[randomize_name].append('昇順/降順ランダム表示')
                                else:
                                    array[randomize_name].append('ランダム表示しない')
                                # キャプション追加
                                array[caption_name].append(temp_item_text.replace('<rand>', '').replace('<rand_rv>', ''))
                                # 追加したので破棄
                                items.pop(count)
                                # 後ろから走査したので並び順を正しくする
                                group_tmp_item.reverse()
                                # 選択肢を格納
                                group_item.append('\n'.join(group_tmp_item))
                                # 再初期化
                                group_tmp_item = []
                            elif items[count].find('--') == 0:
                                items.pop(count)
                            else:
                                group_tmp_item.append(items[count])
                        # 後ろから走査したので並び順を正しくする
                        group_item.reverse()
                        array[caption_name].reverse()
                        array[randomize_name].reverse()
                        # 変換した選択肢を格納
                        array[choice_name] = group_item
                        # グループ数を追加
                        array['グループ設定']['グループ数'] = str(group_count)
                        # グループ位置固定
                        group_fix_count = 1
                        array['グループ位置固定'] = ''
                        for array_value in array[caption_name]:
                            if array_value.find('<fix>') != -1:
                                if array['グループ位置固定'] == '':
                                    array['グループ位置固定'] = str(group_fix_count)
                                else:
                                    array['グループ位置固定'] = ',' + str(group_fix_count)
                                # キャプションから<fix>を取り除く
                                array[caption_name][group_fix_count-1] = array[caption_name][group_fix_count-1].replace('<fix>', '')
                            group_fix_count += 1
                        # print('# キャプション ---------------')
                        # print(array[caption_name])
                        # print('# 選択肢 ---------------')
                        # print(array[choice_name])
                        # print('# ランダマイズ ---------------')
                        # print(array[randomize_name])
                        # print('# グループ数 -> ' + str(array['グループ設定']['グループ数']))
                        # print('# グループ位置固定 ---------------')
                        # print(array['グループ位置固定'])
            # print('# 変換後 ' + str(choice_name) + '-----------------------------------')
            # print(array)
            return array
        except Exception as exc:
            print(exc)

    # 従来forSurveyにしか存在しないキーを削除
    def delete_old_forsurvey_setting_information(self, array):
        try:
            # 「個人情報の取り扱いについて」同意欄
            if array.get('「個人情報の取り扱いについて」同意欄') is not None:
                del array['「個人情報の取り扱いについて」同意欄']
            # スタート個人情報について
            if array.get('スタート個人情報について') is not None:
                del array['スタート個人情報について']
            # キャプション
            if array.get('キャプション') is not None:
                del array['キャプション']
            if array.get('表上') is not None:
                if array['表上'].get('キャプション') is not None:
                    del array['表上']['キャプション']
            if array.get('項目') is not None:
                if array['項目'].get('キャプション') is not None:
                    del array['項目']['キャプション']
            # グループ位置固定
            if array.get('グループ位置固定') is not None:
                del array['グループ位置固定']
            if array.get('表上') is not None:
                if array['表上'].get('グループ位置固定') is not None:
                    del array['表上']['グループ位置固定']
            if array.get('項目') is not None:
                if array['項目'].get('グループ位置固定') is not None:
                    del array['項目']['グループ位置固定']
            if array.get('条件分岐') is not None:
                if array['条件分岐'].get('条件式') is not None:
                    del array['条件分岐']['条件式']
            return array
        except Exception as exc:
            print(exc)

    # 90番forSurveyにしか存在しないキーを削除
    def delete_new_forsurvey_setting_information(self, array):
        try:
            # i-タイル設定
            if array.get('i-タイル設定') is not None:
                del array['i-タイル設定']
            # i-タイル設定詳細
            if array.get('i-タイル設定詳細') is not None:
                del array['i-タイル設定詳細']
            # 抽選機能
            if array.get('抽選機能') is not None:
                del array['抽選機能']
            # # 条件分岐 - 条件式
            # if array.get('条件分岐') is not None:
            #     if array['条件分岐'].get('条件式') is not None:
            #         del array['条件分岐']['条件式']
            return array
        except Exception as exc:
            print(exc)

    # 条件分岐 - 次の条件との関係
    def get_condition_setting_of_nextlogic(self, value, name, array):
        try:
            array_value = array.get(value)
            if array_value is None:
                pass
            else:
                content = ''
                xpath = '//input[@name="' + name + '[nextlogic]"]/parent::td[1]'
                if self.dom_loading_wait(xpath):
                    item_label = self.driver.find_element_by_xpath(xpath).text.split()
                    xpath = '//input[@name="' + name + '[nextlogic]' + '"]'
                    content = self.get_item_label(xpath, item_label)
                    if content == False:
                        pass
                    else:
                        array[value] = content
        except Exception as exc:
            print(exc)

    # 条件分岐 - シングル / 隠しシングル
    def get_condition_setting_of_single_answer(self, name, array):
        try:
            # 条件【01】
            array['条件'] = self.get_item_select('//select[@name="' + name + '[logic]"]')
            array['選択肢'] = []
            self.get_item_checkbox_on_value('//input[@name="' + name + '[choice][normal][item][][refid]"]', array['選択肢'])
            self.get_condition_setting_of_nextlogic('次の条件との関係', name, array)
            return array
        except Exception as exc:
            print(exc)

    # 条件分岐 - マルチ / 隠しマルチ
    def get_condition_setting_of_multi_answer(self, name, array):
        try:
            # print('マルチ')
            # print(name)
            # 条件【01】
            if array['対象'] == '回答':
                array['条件'] = self.get_item_select('//select[@name="' + name + '[target_logic]"]')
                array['選択肢'] = []
                self.get_item_checkbox_on_value('//input[@name="' + name + '[choice][normal][item][][refid]"]', array['選択肢'])
            elif array['対象'] == '回答数':
                array['入力値'] = self.get_item_text('//input[@name="' + name + '[value]"]')
                array['条件式'] = self.get_item_select('//select[@name="' + name + '[operator]"]')
            self.get_condition_setting_of_nextlogic('次の条件との関係', name, array)
            return array
        except Exception as exc:
            print(exc)

    # 条件分岐 - 数値入力 / フリー（小） / フリー（大）
    def get_condition_setting_of_text_answer(self, name, array):
        try:
            # 条件【01】
            if array['対象'] == '回答値':
                array['項目'] = self.get_item_select('//select[@name="' + name + '[choice][normal][item][0][refid]"]')
                array['入力値'] = self.get_item_text('//input[@name="' + name + '[value]"]')
                array['条件文'] = self.get_item_select('//select[@name="' + name + '[operator]"]')
            elif array['対象'] == '合計値':
                array['入力値'] = self.get_item_text('//input[@name="' + name + '[value]"]')
                array['条件文'] = self.get_item_select('//select[@name="' + name + '[operator]"]')
            elif array['対象'] == '記入':
                array['項目'] = self.get_item_select('//select[@name="' + name + '[choice][normal][item][0][refid]"]')
                # optionのvalue値がない対策
                # array['条件文'] = self.get_item_text('//select[@name="' + name + '[operator]"]')
                array['条件文'] = '何か入力されている'
            elif array['対象'] == '未記入':
                array['項目'] = self.get_item_select('//select[@name="' + name + '[choice][normal][item][0][refid]"]')
                # optionのvalue値がない対策
                # array['条件文'] = self.get_item_text('//select[@name="' + name + '[operator]"]')
                array['条件文'] = '何も入力されていない'
            self.get_condition_setting_of_nextlogic('次の条件との関係', name, array)
            return array
        except Exception as exc:
            print(exc)

    # 条件分岐 - マトリクスシングル / SD法
    def get_condition_setting_of_matrix_single_answer(self, name, array):
        try:
            # 条件【01】
            array['項目'] = self.get_item_select('//select[@name="' + name + '[choice][side][item][0][refid]"]')
            array['条件'] = self.get_item_select('//select[@name="' + name + '[logic]"]')
            array['選択肢'] = []
            self.get_item_checkbox_on_value('//input[@name="' + name + '[choice][head][item][][refid]"]', array['選択肢'])
            self.get_condition_setting_of_nextlogic('次の条件との関係', name, array)
            return array
        except Exception as exc:
            print(exc)

    # 条件分岐 - マトリクスマルチ
    def get_condition_setting_of_matrix_multi_answer(self, name, array):
        try:
            # 条件【01】
            if array['対象'] == '回答':
                array['項目'] = self.get_item_select('//select[@name="' + name + '[choice][side][item][0][refid]"]')
                array['条件'] = self.get_item_select('//select[@name="' + name + '[target_logic]"]')
                array['選択肢'] = []
                self.get_item_checkbox_on_value('//input[@name="' + name + '[choice][head][item][][refid]"]', array['選択肢'])
            elif array['対象'] == '回答数':
                array['項目'] = self.get_item_select('//select[@name="' + name + '[choice][side][item][0][refid]"]')
                array['入力値'] = self.get_item_text('//input[@name="' + name + '[value]"]')
                array['条件式'] = self.get_item_select('//select[@name="' + name + '[operator]"]')
            self.get_condition_setting_of_nextlogic('次の条件との関係', name, array)
            return array
        except Exception as exc:
            print(exc)

    # 条件分岐 - マトリクス混合
    def get_condition_setting_of_matrix_mix_answer(self, name, array):
        try:
            # 条件【01】
            if array['対象'] == '回答':
                array['項目'] = self.get_item_select('//select[@name="' + name + '[choice][side][item][0][refid]"]')
                array['条件'] = self.get_item_select('//select[@name="' + name + '[logic]"]')
                if array['条件'] == '':
                    array['条件'] = self.get_item_select('//select[@name="' + name + '[target_logic]"]')
                array['選択肢'] = []
                self.get_item_checkbox_on_value('//input[@name="' + name + '[choice][head][item][][refid]"]', array['選択肢'])
            elif array['対象'] == '回答値':
                array['項目'] = self.get_item_select('//select[@name="' + name + '[choice][side][item][0][refid]"]')
                array['選択肢'] = self.get_item_select('//select[@name="' + name + '[choice][head][item][0][refid]"]')
                array['入力値'] = self.get_item_text('//input[@name="' + name + '[value]"]')
                array['条件文'] = self.get_item_select('//select[@name="' + name + '[operator]"]')
            elif array['対象'] == '合計値':
                array['項目'] = self.get_item_select('//select[@name="' + name + '[choice][side][item][0][refid]"]')
                array['入力値'] = self.get_item_text('//input[@name="' + name + '[value]"]')
                array['条件文'] = self.get_item_select('//select[@name="' + name + '[operator]"]')
            elif array['対象'] == '記入':
                array['項目'] = self.get_item_select('//select[@name="' + name + '[choice][side][item][0][refid]"]')
                array['選択肢'] = self.get_item_select('//select[@name="' + name + '[choice][head][item][0][refid]"]')
                # optionのvalue値がない対策
                # array['条件文'] = self.get_item_text('//select[@name="' + name + '[operator]"]')
                array['条件文'] = '何か入力されている'
            elif array['対象'] == '未記入':
                array['項目'] = self.get_item_select('//select[@name="' + name + '[choice][side][item][0][refid]"]')
                array['選択肢'] = self.get_item_select('//select[@name="' + name + '[choice][head][item][0][refid]"]')
                # optionのvalue値がない対策
                # array['条件文'] = self.get_item_text('//select[@name="' + name + '[operator]"]')
                array['条件文'] = '何も入力されていない'
            self.get_condition_setting_of_nextlogic('次の条件との関係', name, array)
            return array
        except Exception as exc:
            print(exc)

    # SA(単一選択)
    def get_setting_information_of_single_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # 選択肢
            self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[normal][useGroup]'}, array)
            self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[normal][block][1][caption][ja]', array)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
            self.scroll_at_javascript_by_id('captionCO1')
            self.convert_edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
            if array['グループ設定']['グループ設定する'] == 'on':
                self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][direction]', array)
                self.convert_edit_question_text_by_name('input', 'グループ選択肢数,選択肢数,…', 'choice[normal][multiline]', array)
                self.convert_edit_question_text_by_name('input', '折り返し数', 'choice[normal][maxline]', array)
                self.convert_edit_question_text_by_name('input', '幅設定', 'choice[normal][linewidth]', array)
                self.convert_edit_question_randomize('グループランダマイズ', 'choice[normal][orderlogic]', array, 'parent::span')
                self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[normal][fixBlock]', array)
            else:
                self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                self.convert_edit_question_text_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                self.convert_edit_question_text_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
            self.convert_edit_question_radio_by_name('必須入力チェック', 'must', array)
            self.convert_edit_question_radio_by_name('表示形式', 'choice[normal][controlType]', array)
            self.convert_edit_question_radio_by_name('設問文と選択肢表示', 'view_type', array)
            self.convert_edit_question_radio_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
            self.convert_edit_question_by_itile('i-タイル設定', 'i_tile_setting_flag', array)
            # 設問編集(2)
            self.convert_edit_question_text_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.convert_edit_question_image_setting('画像', array)
            self.convert_edit_question_video_setting('動画貼付', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.convert_edit_question_error_check_process('エラーチェック', array)
            return array
        except Exception as exc:
            print(exc)

    # MA(複数選択)
    def get_setting_information_of_multi_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # 選択肢
            self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[normal][useGroup]'}, array)
            self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[normal][block][1][caption][ja]', array)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
            self.scroll_at_javascript_by_id('captionCO1')
            self.convert_edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
            if array['グループ設定']['グループ設定する'] == 'on':
                self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][direction]', array)
                self.convert_edit_question_text_by_name('input', 'グループ選択肢数,選択肢数,…', 'choice[normal][multiline]', array)
                self.convert_edit_question_text_by_name('input', '折り返し数', 'choice[normal][maxline]', array)
                self.convert_edit_question_text_by_name('input', '幅設定', 'choice[normal][linewidth]', array)
                self.convert_edit_question_randomize('グループランダマイズ', 'choice[normal][orderlogic]', array, 'parent::span')
                self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[normal][fixBlock]', array)
            else:
                self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                self.convert_edit_question_text_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                self.convert_edit_question_text_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
            self.convert_edit_question_radio_by_name('必須入力チェック', 'must', array)
            self.convert_edit_question_selection_count_limit('選択個数制限', 'limit', array)
            self.convert_edit_question_radio_by_name('設問文と選択肢表示', 'view_type', array)
            self.convert_edit_question_radio_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
            self.convert_edit_question_by_itile('i-タイル設定', 'i_tile_setting_flag', array)
            # 設問編集(2)
            self.convert_edit_question_text_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.convert_edit_question_image_setting('画像', array)
            self.convert_edit_question_video_setting('動画貼付', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.convert_edit_question_error_check_process('エラーチェック', array)
            return array
        except Exception as exc:
            print(exc)

    # 隠し設問SA
    def get_setting_information_of_hidden_single_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            # 選択肢
            self.convert_edit_question_text_by_name('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
            # 設問編集(2)
            # ローテーションパターンは未実装　※以下、90番の為、後回し
            self.convert_edit_question_lottery_count('抽選機能', 'lottery', array)
            self.convert_edit_question_gate_interlock('打切り設定連動機能', 'lotteryAbort', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            return array
        except Exception as exc:
            print(exc)

    # 数値
    def get_setting_information_of_number_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # 選択肢
            self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[normal][useGroup]'}, array)
            self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[normal][block][1][caption][ja]', array)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
            self.scroll_at_javascript_by_id('captionCO1')
            self.convert_edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
            if array['グループ設定']['グループ設定する'] == 'on':
                self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][direction]', array)
                self.convert_edit_question_text_by_name('input', 'グループ選択肢数,選択肢数,…', 'choice[normal][multiline]', array)
                self.convert_edit_question_text_by_name('input', '折り返し数', 'choice[normal][maxline]', array)
                self.convert_edit_question_text_by_name('input', '幅設定', 'choice[normal][linewidth]', array)
                self.convert_edit_question_randomize('グループランダマイズ', 'choice[normal][orderlogic]', array, 'parent::span')
                self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[normal][fixBlock]', array)
            else:
                self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                self.convert_edit_question_text_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                self.convert_edit_question_text_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
            self.convert_edit_question_radio_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
            self.convert_edit_question_radio_by_name('設問文と選択肢表示', 'view_type', array)
            self.convert_edit_question_radio_by_name('合計値表示', 'showTotal', array, 'ancestor::tr[1]')
            self.convert_edit_question_selection_total_count_limit('合計値制限', 'limitTotal', array)
            # 設問編集(2)
            self.convert_edit_question_text_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.convert_edit_question_image_setting('画像', array)
            self.convert_edit_question_video_setting('動画貼付', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.convert_edit_question_error_check_process('エラーチェック', array)
            return array
        except Exception as exc:
            print(exc)

    # 自由記入短文
    def get_setting_information_of_freeshort_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # 選択肢
            self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[normal][useGroup]'}, array)
            self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[normal][block][1][caption][ja]', array)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
            self.scroll_at_javascript_by_id('captionCO1')
            self.convert_edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
            if array['グループ設定']['グループ設定する'] == 'on':
                self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][direction]', array)
                self.convert_edit_question_text_by_name('input', 'グループ選択肢数,選択肢数,…', 'choice[normal][multiline]', array)
                self.convert_edit_question_text_by_name('input', '折り返し数', 'choice[normal][maxline]', array)
                self.convert_edit_question_text_by_name('input', '幅設定', 'choice[normal][linewidth]', array)
                self.convert_edit_question_randomize('グループランダマイズ', 'choice[normal][orderlogic]', array, 'parent::span')
                self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[normal][fixBlock]', array)
            else:
                self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                self.convert_edit_question_text_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                self.convert_edit_question_text_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
            self.convert_edit_question_radio_by_name('設問文と選択肢表示', 'view_type', array)
            self.convert_edit_question_radio_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
            # 設問編集(2)
            self.convert_edit_question_text_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.convert_edit_question_image_setting('画像', array)
            self.convert_edit_question_video_setting('動画貼付', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.convert_edit_question_error_check_process('エラーチェック', array)
            return array
        except Exception as exc:
            print(exc)

    # 自由記入長文
    def get_setting_information_of_freelong_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # 選択肢
            self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[normal][useGroup]'}, array)
            self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[normal][block][1][caption][ja]', array)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
            self.scroll_at_javascript_by_id('captionCO1')
            self.convert_edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
            if array['グループ設定']['グループ設定する'] == 'on':
                self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][direction]', array)
                self.convert_edit_question_text_by_name('input', 'グループ選択肢数,選択肢数,…', 'choice[normal][multiline]', array)
                self.convert_edit_question_text_by_name('input', '折り返し数', 'choice[normal][maxline]', array)
                self.convert_edit_question_text_by_name('input', '幅設定', 'choice[normal][linewidth]', array)
                self.convert_edit_question_randomize('グループランダマイズ', 'choice[normal][orderlogic]', array, 'parent::span')
                self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[normal][fixBlock]', array)
            else:
                self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                self.convert_edit_question_text_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                self.convert_edit_question_text_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
            self.convert_edit_question_radio_by_name('設問文と選択肢表示', 'view_type', array)
            self.convert_edit_question_radio_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
            # 設問編集(2)
            self.convert_edit_question_text_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.convert_edit_question_image_setting('画像', array)
            self.convert_edit_question_video_setting('動画貼付', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.convert_edit_question_error_check_process('エラーチェック', array)
            return array
        except Exception as exc:
            print(exc)

    # 隠し設問MA
    def get_setting_information_of_hidden_multi_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            # 選択肢
            self.convert_edit_question_text_by_name('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
            # 設問編集(2)
            self.convert_edit_question_lottery_count('抽選機能', 'lottery', array)
            self.convert_edit_question_gate_interlock('打切り設定連動機能', 'lotteryAbort', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            return array
        except Exception as exc:
            print(exc)

    # 画像アップロード
    def get_setting_information_of_image_upload_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # 選択肢
            self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[normal][useGroup]'}, array)
            self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[normal][block][1][caption][ja]', array)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
            self.scroll_at_javascript_by_id('captionCO1')
            self.convert_edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
            if array['グループ設定']['グループ設定する'] == 'on':
                self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][direction]', array)
                self.convert_edit_question_text_by_name('input', 'グループ選択肢数,選択肢数,…', 'choice[normal][multiline]', array)
                self.convert_edit_question_text_by_name('input', '折り返し数', 'choice[normal][maxline]', array)
                self.convert_edit_question_text_by_name('input', '幅設定', 'choice[normal][linewidth]', array)
                self.convert_edit_question_randomize('グループランダマイズ', 'choice[normal][orderlogic]', array, 'parent::span')
                self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[normal][fixBlock]', array)
            else:
                self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                self.convert_edit_question_text_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                self.convert_edit_question_text_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
            self.convert_edit_question_radio_by_name('設問文と選択肢表示', 'view_type', array)
            self.convert_edit_question_radio_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
            # 設問編集(2)
            self.convert_edit_question_text_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.convert_edit_question_image_setting('画像', array)
            self.convert_edit_question_video_setting('動画貼付', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.convert_edit_question_error_check_process('エラーチェック', array)
            return array
        except Exception as exc:
            print(exc)

    # マトリクスSA
    def get_setting_information_of_matrix_single_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # イレギュラー（先に取得しないと「文字列方向」のname値が適切に取得できない
            self.convert_edit_question_checkbox_by_name('表頭・表側の位置を入れ替え', {'表頭・表側の位置を入れ替える': 'transpose'}, array)
            # 選択肢[表上（選択肢側）]
            array_head = array['表上']
            self.scroll_at_javascript_by_id('choiceSCO1')
            self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[head][useGroup]'}, array_head)
            self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[head][block][1][caption][ja]', array_head)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[head][block][1][choiceText][ja]', array_head)
            self.convert_edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[head][block][1][orderlogic]', array_head, 'ancestor::td[1]')
            if array_head['グループ設定']['グループ設定する'] == 'on':
                self.convert_edit_question_randomize('グループランダマイズ', 'choice[head][orderlogic]', array_head, 'parent::span')
                self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[head][fixBlock]', array_head)
            self.convert_edit_question_radio_by_name('表示形式（PC/iPad）', 'choice[head][controlType]', array_head, 'ancestor::tr[1]')
            if array['表頭・表側の位置を入れ替え']['表頭・表側の位置を入れ替える'] == 'off':
                self.convert_edit_question_radio_by_name('文字列方向', 'choice[head][directstr]', array_head, 'ancestor::tr[1]')
                del array['項目']['文字列方向']
            self.convert_edit_question_radio_by_name('選択肢番号', 'choice[head][showChoiceNo]', array_head, 'ancestor::tr[1]')
            # 選択肢[表左（項目側）]
            array_side = array['項目']
            self.scroll_at_javascript_by_id('choiceSCO1')
            self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[side][useGroup]'}, array_side)
            self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[side][block][1][caption][ja]', array_side)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[side][block][1][choiceText][ja]', array_side)
            self.convert_edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[side][block][1][orderlogic]', array_side, 'ancestor::td[1]')
            if array_side['グループ設定']['グループ設定する'] == 'on':
                self.convert_edit_question_randomize('グループランダマイズ', 'choice[side][orderlogic]', array_side, 'parent::span')
                self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[side][fixBlock]', array_side)
            if array['表頭・表側の位置を入れ替え']['表頭・表側の位置を入れ替える'] == 'on':
                self.convert_edit_question_radio_by_name('文字列方向', 'choice[side][directstr]', array_side, 'ancestor::tr[1]')
                del array['表上']['文字列方向']
            self.convert_edit_question_radio_by_name('選択肢番号', 'choice[side][showChoiceNo]', array_side, 'ancestor::tr[1]')
            self.convert_edit_question_text_by_name('input', '左肩コメント', 'leftShoulderComment[ja]', array_side)
            # そのほか
            self.convert_edit_question_radio_by_name('必須入力チェック', 'must', array,  'ancestor::tr[1]')
            self.convert_edit_question_radio_by_name('設問文と選択肢表示', 'view_type', array)
            self.convert_edit_question_radio_by_name('同一回答チェック', 'straightcheck', array)
            self.convert_edit_question_checkbox_by_name('順位付けチェック', {'順位付けチェックを行う': 'sequencecheck'}, array)
            self.convert_edit_question_text_by_name('input', '表上繰り返し', 'repeathead', array)
            self.convert_edit_question_text_by_name('input', '横幅指定', 'multilinewidth', array)
            # 表示指定
            self.convert_edit_question_radio_by_name('選択行反転表示', 'highlight', array, 'ancestor::tr[1]')
            # 色指定
            self.convert_edit_question_by_itile('i-タイル設定', 'i_tile_setting_flag', array)
            # 設問編集(2)
            self.convert_edit_question_text_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.convert_edit_question_image_setting('画像', array)
            self.convert_edit_question_video_setting('動画貼付', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.convert_edit_question_error_check_process('エラーチェック', array)
            return array
        except Exception as exc:
            print(exc)

    # マトリクスMA
    def get_setting_information_of_matrix_multi_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # イレギュラー（先に取得しないと「文字列方向」のname値が適切に取得できない
            self.convert_edit_question_checkbox_by_name('表頭・表側の位置を入れ替え', {'表頭・表側の位置を入れ替える': 'transpose'}, array)
            # 選択肢[表上（選択肢側）]
            array_head = array['表上']
            self.scroll_at_javascript_by_id('choiceSCO1')
            self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[head][useGroup]'}, array_head)
            self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[head][block][1][caption][ja]', array_head)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[head][block][1][choiceText][ja]', array_head)
            self.convert_edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[head][block][1][orderlogic]', array_head, 'ancestor::td[1]')
            if array_head['グループ設定']['グループ設定する'] == 'on':
                self.convert_edit_question_randomize('グループランダマイズ', 'choice[head][orderlogic]', array_head, 'parent::span')
                self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[head][fixBlock]', array_head)
            if array['表頭・表側の位置を入れ替え']['表頭・表側の位置を入れ替える'] == 'off':
                self.convert_edit_question_radio_by_name('文字列方向', 'choice[head][directstr]', array_head, 'ancestor::tr[1]')
                del array['項目']['文字列方向']
            self.convert_edit_question_selection_count_limit('選択個数制限', 'limit', array_head)
            self.convert_edit_question_radio_by_name('選択肢番号', 'choice[head][showChoiceNo]', array_head, 'ancestor::tr[1]')
            # 選択肢[表左（項目側）]
            array_side = array['項目']
            self.scroll_at_javascript_by_id('choiceSCO1')
            self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[side][useGroup]'}, array_side)
            self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[side][block][1][caption][ja]', array_side)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[side][block][1][choiceText][ja]', array_side)
            self.convert_edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[side][block][1][orderlogic]', array_side, 'ancestor::td[1]')
            if array_side['グループ設定']['グループ設定する'] == 'on':
                self.convert_edit_question_randomize('グループランダマイズ', 'choice[side][orderlogic]', array_side, 'parent::span')
                self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[side][fixBlock]', array_side)
            if array['表頭・表側の位置を入れ替え']['表頭・表側の位置を入れ替える'] == 'on':
                self.convert_edit_question_radio_by_name('文字列方向', 'choice[side][directstr]', array_side, 'ancestor::tr[1]')
                del array['表上']['文字列方向']
            self.convert_edit_question_radio_by_name('選択肢番号', 'choice[side][showChoiceNo]', array_side, 'ancestor::tr[1]')
            self.convert_edit_question_text_by_name('input', '左肩コメント', 'leftShoulderComment[ja]', array_side)
            # そのほか
            self.convert_edit_question_radio_by_name('必須入力チェック', 'must', array,  'ancestor::tr[1]')
            self.convert_edit_question_radio_by_name('設問文と選択肢表示', 'view_type', array)
            self.convert_edit_question_radio_by_name('同一回答チェック', 'straightcheck', array)
            self.convert_edit_question_text_by_name('input', '表上繰り返し', 'repeathead', array)
            self.convert_edit_question_text_by_name('input', '横幅指定', 'multilinewidth', array)
            # 表示指定
            self.convert_edit_question_radio_by_name('選択行反転表示', 'highlight', array, 'ancestor::tr[1]')
            # 色指定
            self.convert_edit_question_by_itile('i-タイル設定', 'i_tile_setting_flag', array)
            # 設問編集(2)
            self.convert_edit_question_text_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.convert_edit_question_image_setting('画像', array)
            self.convert_edit_question_video_setting('動画貼付', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.convert_edit_question_error_check_process('エラーチェック', array)
            return array
        except Exception as exc:
            print(exc)

    # マトリクス混合
    def get_setting_information_of_matrix_mix_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # イレギュラー（先に取得しないと「文字列方向」のname値が適切に取得できない
            self.convert_edit_question_checkbox_by_name('表頭・表側の位置を入れ替え', {'表頭・表側の位置を入れ替える': 'transpose'}, array)
            # 選択肢[表上（選択肢側）]
            array_head = array['表上']
            self.scroll_at_javascript_by_id('choiceSCO1')
            self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[head][useGroup]'}, array_head)
            self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[head][block][1][caption][ja]', array_head)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[head][block][1][choiceText][ja]', array_head)
            self.convert_edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[head][block][1][orderlogic]', array_head, 'ancestor::td[1]')
            if array_head['グループ設定']['グループ設定する'] == 'on':
                self.convert_edit_question_randomize('グループランダマイズ', 'choice[head][orderlogic]', array_head, 'parent::span')
                self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[head][fixBlock]', array_head)
            if array['表頭・表側の位置を入れ替え']['表頭・表側の位置を入れ替える'] == 'off':
                self.convert_edit_question_radio_by_name('文字列方向', 'choice[head][directstr]', array_head, 'ancestor::tr[1]')
                del array['項目']['文字列方向']
            self.convert_edit_question_selection_count_limit('選択個数制限', 'limit', array_head)
            self.convert_edit_question_radio_by_name('選択肢番号', 'choice[head][showChoiceNo]', array_head, 'ancestor::tr[1]')
            # 選択肢[表左（項目側）]
            array_side = array['項目']
            self.scroll_at_javascript_by_id('choiceSCO1')
            self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[side][useGroup]'}, array_side)
            self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[side][block][1][caption][ja]', array_side)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[side][block][1][choiceText][ja]', array_side)
            self.convert_edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[side][block][1][orderlogic]', array_side, 'ancestor::td[1]')
            if array_side['グループ設定']['グループ設定する'] == 'on':
                self.convert_edit_question_randomize('グループランダマイズ', 'choice[side][orderlogic]', array_side, 'parent::span')
                self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[side][fixBlock]', array_side)
            if array['表頭・表側の位置を入れ替え']['表頭・表側の位置を入れ替える'] == 'on':
                self.convert_edit_question_radio_by_name('文字列方向', 'choice[side][directstr]', array_side, 'ancestor::tr[1]')
                del array['表上']['文字列方向']
            self.convert_edit_question_radio_by_name('選択肢番号', 'choice[side][showChoiceNo]', array_side, 'ancestor::tr[1]')
            self.convert_edit_question_text_by_name('input', '左肩コメント', 'leftShoulderComment[ja]', array_side)
            # そのほか
            self.convert_edit_question_radio_by_name('必須入力チェック', 'must', array,  'ancestor::tr[1]')
            self.convert_edit_question_radio_by_name('設問文と選択肢表示', 'view_type', array)
            # self.clear_checkbox_all_by_name('絞り込み', 'useDynamicFilter')
            # if array['絞り込み'] == '絞り込みを行う':
            #     self.choose_multiple_checkbox('絞り込み', {'絞り込みを行う': 'useDynamicFilter'}, array, 'input[@name=')
            #     self.clear_matrix_mix_use_dynamic_filter_checkbox()
            #     count = -1
            #     for array_value in array['絞り込み設定']:
            #         count += 1
            #         # 追加
            #         xpath = '//input[@id="addFilter"]'
            #         self.item_click(xpath)
            #         # フィルタ設定
            #         xpath =  'target_item[' + str(count) + ']'
            #         array_temp = []
            #         array_temp.append(array['絞り込み設定'][array_value][0])
            #         array_temp.append(array['絞り込み設定'][array_value][1])
            #         array_value_child = {'絞り込み設定': array_temp}
            #         self.item_pick_multiple_by_value('絞り込み設定', ['target_item[' + str(count) + ']', 'trigger_item[' + str(count) + ']'], array_value_child)
            #         # 表示/非表示
            #         if array['絞り込み設定'][array_value][2] == '非表示':
            #             xpath = '//input[@name="filterType[' + str(count) + ']"][@value="hide"]'
            #             self.item_click(xpath)
            #         # 排他も含む
            #         if len(array['絞り込み設定'][array_value]) > 3:
            #              if array['絞り込み設定'][array_value][3] == '排他も含む':
            #                 xpath = '//input[@name="withExclusive[' + str(count) + ']"]'
            #                 self.item_click(xpath)
            self.convert_edit_question_text_by_name('input', '表上繰り返し', 'repeathead', array)
            self.convert_edit_question_text_by_name('input', '横幅指定', 'multilinewidth', array)
            # 表示指定
            self.convert_edit_question_radio_by_name('選択行反転表示', 'highlight', array, 'ancestor::tr[1]')
            # 色指定
            self.convert_edit_question_by_itile('i-タイル設定', 'i_tile_setting_flag', array)
            # 設問編集(2)
            self.convert_edit_question_text_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.convert_edit_question_image_setting('画像', array)
            self.convert_edit_question_video_setting('動画貼付', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.convert_edit_question_error_check_process('エラーチェック', array)
            return array
        except Exception as exc:
            print(exc)

    # 文章・画像のみ
    def get_setting_information_of_through_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            # 設問編集(2)
            self.convert_edit_question_text_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.convert_edit_question_image_setting('画像', array)
            self.convert_edit_question_video_setting('動画貼付', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.convert_edit_question_error_check_process('エラーチェック', array)
            return array
        except Exception as exc:
            print(exc)

    # プロフィール
    def get_setting_information_of_profile_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            # 選択肢
            if self.mode == 'dev4s' or self.mode == '4s90':
                self.convert_edit_question_text_by_name('textarea', '選択肢', 'choice[normal][choiceText][1][ja]', array)
            else:
                self.convert_edit_question_choice_text_by_profile('選択肢', array)
            self.convert_edit_question_radio_by_name('設問文と選択肢表示', 'view_type', array)
            # 設問編集(2)
            self.convert_edit_question_image_setting('画像', array)
            self.convert_edit_question_video_setting('動画貼付', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            return array
        except Exception as exc:
            print(exc)

    # SD法
    def get_setting_information_of_matrix_sd_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            # 選択肢[表上（選択肢側）]
            array_head = array['表上']
            self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[head][useGroup]'}, array_head)
            self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[head][block][1][caption][ja]', array_head)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[head][block][1][choiceText][ja]', array_head)
            self.scroll_at_javascript_by_id('captionHCP1')
            self.convert_edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[head][block][1][orderlogic]', array_head, 'ancestor::td[1]')
            if array_head['グループ設定']['グループ設定する'] == 'on':
                self.convert_edit_question_randomize('グループランダマイズ', 'choice[head][orderlogic]', array_head, 'parent::span')
                self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[head][fixBlock]', array_head)
            self.convert_edit_question_radio_by_name('文字列方向', 'choice[head][directstr]', array_head, 'ancestor::tr[1]')
            self.convert_edit_question_radio_by_name('選択肢番号', 'choice[head][showChoiceNo]', array_head, 'ancestor::tr[1]')
            # 選択肢[表左（項目側）]
            array_side = array['項目']
            self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[side][useGroup]'}, array_side)
            self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[side][block][1][caption][left][ja]', array_side)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢（表左）', 'choice[side][block][1][choiceText][left][ja]', array_side)
            self.convert_edit_question_choice_text_by_group('textarea', '選択肢（表右）', 'choice[side][block][1][choiceText][right][ja]', array_side)
            self.scroll_at_javascript_by_id('choiceSLCO1')
            self.convert_edit_question_randomize_by_group('選択肢ランダマイズ', 'choice[side][block][1][orderlogic]', array_side, 'ancestor::td[1]')
            if array_side['グループ設定']['グループ設定する'] == 'on':
                self.convert_edit_question_randomize('グループランダマイズ', 'choice[side][orderlogic]', array_side, 'parent::span')
                self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[side][fixBlock]', array_side)
            self.convert_edit_question_radio_by_name('選択肢番号', 'choice[side][showChoiceNo]', array_side, 'ancestor::tr[1]')
            self.convert_edit_question_text_by_name('input', '左肩コメント', 'leftShoulderComment[ja]', array_side)
            self.convert_edit_question_text_by_name('input', '右肩コメント', 'rightShoulderComment[ja]', array_side)
            # そのほか
            self.convert_edit_question_radio_by_name('必須入力チェック', 'must', array,  'ancestor::tr[1]')
            self.convert_edit_question_radio_by_name('設問文と選択肢表示', 'view_type', array)
            # 90番のみ、表上繰り返しが存在している
            if self.mode == 'dev4s' or self.mode == '4s90':
                self.convert_edit_question_text_by_name('input', '表上繰り返し', 'repeathead', array)
            # self.convert_edit_question_radio_by_name('表上下部表示', 'bottomhead', array)
            # ↑ 従来基盤のアホ仕様（ラジオボタンで同じnameが存在してる）
            self.convert_edit_question_text_by_name('input', '横幅指定', 'multilinewidth', array)
            # 表示指定
            self.convert_edit_question_radio_by_name('選択行反転表示', 'highlight', array, 'ancestor::tr[1]')
            # 色指定
            self.convert_edit_question_by_itile('i-タイル設定', 'i_tile_setting_flag', array)
            # 設問編集(2)
            self.convert_edit_question_text_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.convert_edit_question_image_setting('画像', array)
            self.convert_edit_question_video_setting('動画貼付', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.convert_edit_question_error_check_process('エラーチェック', array)
            return array
        except Exception as exc:
            print(exc)

    # 登録情報設問
    def get_setting_information_of_attribute_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_attribute_type('属性タイプ', 'moniinfo', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント上', 'comment1[ja]', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            self.convert_edit_question_text_by_name('textarea', 'コメント中', 'comment2[ja]', array)
            if array['属性タイプ'] == '年齢(数値FA)':
                # 選択肢
                self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[normal][useGroup]'}, array)
                self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[normal][block][1][caption][ja]', array)
                self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
                self.scroll_at_javascript_by_id('captionCO1')
                self.convert_edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
                if array['グループ設定']['グループ設定する'] == 'on':
                    self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][direction]', array)
                    self.convert_edit_question_text_by_name('input', 'グループ選択肢数,選択肢数,…', 'choice[normal][multiline]', array)
                    self.convert_edit_question_text_by_name('input', '折り返し数', 'choice[normal][maxline]', array)
                    self.convert_edit_question_text_by_name('input', '幅設定', 'choice[normal][linewidth]', array)
                    self.convert_edit_question_randomize('グループランダマイズ', 'choice[normal][orderlogic]', array, 'parent::span')
                    self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[normal][fixBlock]', array)
                else:
                    self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                    self.convert_edit_question_text_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                    self.convert_edit_question_text_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
                self.convert_edit_question_radio_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
                self.convert_edit_question_radio_by_name('設問文と選択肢表示', 'view_type', array)
                self.convert_edit_question_radio_by_name('合計値表示', 'showTotal', array, 'ancestor::tr[1]')
                self.convert_edit_question_selection_total_count_limit('合計値制限', 'limitTotal', array)
            else:
                # 選択肢
                self.convert_edit_question_choice_group_by_name('グループ設定', {'グループ設定する': 'choice[normal][useGroup]'}, array)
                self.convert_edit_question_choice_text_by_group('textarea', 'キャプション', 'choice[normal][block][1][caption][ja]', array)
                self.convert_edit_question_choice_text_by_group('textarea', '選択肢', 'choice[normal][block][1][choiceText][ja]', array)
                self.scroll_at_javascript_by_id('captionCO1')
                self.convert_edit_question_randomize_by_group('ランダマイズ', 'choice[normal][block][1][orderlogic]', array, 'parent::span')
                if array['グループ設定']['グループ設定する'] == 'on':
                    self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][direction]', array)
                    self.convert_edit_question_text_by_name('input', 'グループ選択肢数,選択肢数,…', 'choice[normal][multiline]', array)
                    self.convert_edit_question_text_by_name('input', '折り返し数', 'choice[normal][maxline]', array)
                    self.convert_edit_question_text_by_name('input', '幅設定', 'choice[normal][linewidth]', array)
                    self.convert_edit_question_randomize('グループランダマイズ', 'choice[normal][orderlogic]', array, 'parent::span')
                    self.convert_edit_question_text_by_name('input', 'グループ位置固定', 'choice[normal][fixBlock]', array)
                else:
                    self.convert_edit_question_radio_by_name('表示方向', 'choice[normal][block][1][direction]', array)
                    self.convert_edit_question_text_by_name('input', '選択肢数,選択肢数,…', 'choice[normal][block][1][multiline]', array)
                    self.convert_edit_question_text_by_name('input', '横幅指定', 'choice[normal][block][1][multilinewidth]', array)
                self.convert_edit_question_radio_by_name('必須入力チェック', 'must', array)
                self.convert_edit_question_radio_by_name('表示形式', 'choice[normal][controlType]', array)
                self.convert_edit_question_radio_by_name('設問文と選択肢表示', 'view_type', array)
                self.convert_edit_question_radio_by_name('選択肢番号', 'choice[normal][showChoiceNo]', array)
                self.convert_edit_question_radio_by_name('i-タイル設定', 'i_tile_setting_flag', array, 'parent::label/parent::td[1]')
            # 設問編集(2)
            self.convert_edit_question_text_by_name('textarea', 'コメント下', 'comment3[ja]', array)
            self.convert_edit_question_image_setting('画像', array)
            self.convert_edit_question_video_setting('動画貼付', array)
            self.convert_edit_question_text_by_name('textarea', '備考', 'qu_remarks', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            # エラーチェック
            self.convert_edit_question_error_check_process('エラーチェック', array)
            return array
        except Exception as exc:
            print(exc)

    # 外部連携設問
    def get_setting_information_of_post_external_answer(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', '設問タイトル', 'qu_title', array)
            self.convert_edit_question_selecting_question_type('設問タイプ', array)
            self.convert_edit_question_selecting_question_number('設問No', array)
            self.convert_edit_question_text_by_name('textarea', '設問文', 'explain[ja]', array)
            self.convert_edit_question_text_by_name('input', '行き先リサーチURL', 'url_research_external', array)
            self.convert_edit_question_text_by_name('input', '想定回答時間', 'time_post_external', array)
            self.convert_edit_question_radio_by_name('設問文と選択肢表示', 'view_type', array)
            self.convert_edit_question_external_status('戻り先情報', 'labelClientStatus[]', array)
            # 設問編集(2)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(設問表示時)', 'javascript_load', array)
            self.convert_edit_question_text_by_name('textarea', 'Javascript(次へボタン押下時)', 'javascript', array)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            return array
        except Exception as exc:
            print(exc)

    # STARTページ
    def get_setting_information_of_start_page(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_text_by_name('input', 'アンケートタイトル', 're_public_title[ja]', array)
            self.convert_edit_question_radio_by_start_page('スタートページ表示', 're_disp_start_page', array)
            self.convert_edit_question_text_by_name('textarea', 'スタート設問文', 're_explain[ja]', array)
            self.convert_edit_question_radio_by_name('「個人情報の取り扱いについて」同意欄', 're_ppa_id', array)
            self.convert_edit_question_text_by_name('textarea', 'スタート個人情報について', 're_policy[ja]', array)
            # 設問編集(2)
            self.convert_edit_question_text_by_name('textarea', 'ページ情報(headの最後尾)', 'headerinfo', array)
            return array
        except Exception as exc:
            print(exc)

    # END/COMPページ
    def get_setting_information_of_comp_page(self, array):
        try:
            # 設問編集(1)
            self.convert_edit_question_end_type('終了タイプ', array)
            self.convert_edit_question_text_by_name('textarea', 'メッセージ', 'message[ja]', array)
            self.convert_edit_question_redirect('自動リダイレクト', 'redirect_type', array)
            self.convert_edit_question_link_by_name('リンク', {'リンク設定する': 'link[useGroup]'}, array)
            # リンク設定がONのとき
            if array['リンク']['リンク設定する'] == 'on':
                loop_count = int(array['リンク']['リンク数'])
                array['リンク']['リンク設定'] = []
                for count in range(1, loop_count + 1):
                    array['リンク']['リンク設定'].append({
                        "表示条件": self.get_item_text('//input[@name="link[conditions][' + str(count) + ']"]'),
                        "ボタン上コメント": self.get_item_text('//textarea[@name="link[message_top][' + str(count) + '][ja]"]'),
                        "ボタン": self.get_item_label('//input[@name="link[linkshow][' + str(count) + ']"]',['表示', '非表示', '画像（バナー）にする']),
                        "ボタン名称": self.driver.find_elements_by_xpath('//input[@name="link[button_name][' + str(count) + '][ja]"]')[0].get_attribute('value'),
                        "URL": self.get_item_text('//input[@name="link[link_address][' + str(count) + ']"]'),
                        "ボタン下コメント": self.get_item_text('//textarea[@name="link[message_bottom][' + str(count) + '][ja]"]')
                    })
            self.convert_edit_question_text_by_name('textarea', 'メッセージ下', 'message_bottom[ja]', array)
            self.convert_edit_question_redirect_api('外部連結　終了通知API', 'api_type', array)
            return array
        except Exception as exc:
            print(exc)

    # GATEページ
    def get_setting_information_of_gate_page(self, array):
        try:
            self.get_setting_information_of_comp_page(array)
            self.convert_edit_question_checkbox_by_name('GATE', {'GATEに設定する': 'uchikiri'}, array)
            return array
        except Exception as exc:
            print(exc)


    # [出力]---------------------------------------------------------------
    # [初期値]---------------------------------------------------------------
    # SA(単一選択)
    def set_setting_information_of_single_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "グループ設定": "",
                    "キャプション": "",
                    "選択肢": "",
                    "ランダマイズ": "",
                    "表示方向": "",
                    "選択肢数,選択肢数,…": "",
                    "横幅指定": "",
                    "グループ選択肢数,選択肢数,…": "",
                    "折り返し数": "",
                    "幅指定": "",
                    "グループランダマイズ": "",
                    "グループ位置固定": "",
                    "必須入力チェック": "",
                    "表示形式": "",
                    "設問文と選択肢表示": "",
                    "選択肢番号": "",
                    "i-タイル設定": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "グループ設定": "",
                    "キャプション": "",
                    "選択肢": "",
                    "ランダマイズ": "",
                    "表示方向": "",
                    "選択肢数,選択肢数,…": "",
                    "横幅指定": "",
                    "グループ選択肢数,選択肢数,…": "",
                    "折り返し数": "",
                    "幅指定": "",
                    "グループランダマイズ": "",
                    "グループ位置固定": "",
                    "必須入力チェック": "",
                    "表示形式": "",
                    "設問文と選択肢表示": "",
                    "選択肢番号": "",
                    "i-タイル設定": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
        except Exception as exc:
            print(exc)

    # MA(複数選択)
    def set_setting_information_of_multi_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "グループ設定": "",
                    "キャプション": "",
                    "選択肢": "",
                    "ランダマイズ": "",
                    "表示方向": "",
                    "選択肢数,選択肢数,…": "",
                    "横幅指定": "",
                    "グループ選択肢数,選択肢数,…": "",
                    "折り返し数": "",
                    "幅指定": "",
                    "グループランダマイズ": "",
                    "グループ位置固定": "",
                    "必須入力チェック": "",
                    "選択個数制限": "",
                    "設問文と選択肢表示": "",
                    "選択肢番号": "",
                    "i-タイル設定": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "グループ設定": "",
                    "キャプション": "",
                    "選択肢": "",
                    "ランダマイズ": "",
                    "表示方向": "",
                    "選択肢数,選択肢数,…": "",
                    "横幅指定": "",
                    "グループ選択肢数,選択肢数,…": "",
                    "折り返し数": "",
                    "幅指定": "",
                    "グループランダマイズ": "",
                    "グループ位置固定": "",
                    "必須入力チェック": "",
                    "選択個数制限": "",
                    "設問文と選択肢表示": "",
                    "選択肢番号": "",
                    "i-タイル設定": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
        except Exception as exc:
            print(exc)

    # 隠し設問SA
    def set_setting_information_of_hidden_single_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "設問文": "",
                    # 選択肢
                    "選択肢": "",
                    "抽選機能": "",
                    # 設問編集(2)
                    "備考": "",
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "設問文": "",
                    # 選択肢
                    "選択肢": "",
                    "抽選機能": "",
                    # 設問編集(2)
                    "備考": "",
                }
        except Exception as exc:
            print(exc)

    # 数値
    def set_setting_information_of_number_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "グループ設定": "",
                    "キャプション": "",
                    "選択肢": "",
                    "ランダマイズ": "",
                    "表示方向": "",
                    "選択肢数,選択肢数,…": "",
                    "横幅指定": "",
                    "グループ選択肢数,選択肢数,…": "",
                    "折り返し数": "",
                    "幅指定": "",
                    "グループランダマイズ": "",
                    "グループ位置固定": "",
                    "選択肢番号": "",
                    "設問文と選択肢表示": "",
                    "合計値表示": "",
                    "合計値制限": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "グループ設定": "",
                    "キャプション": "",
                    "選択肢": "",
                    "ランダマイズ": "",
                    "表示方向": "",
                    "選択肢数,選択肢数,…": "",
                    "横幅指定": "",
                    "グループ選択肢数,選択肢数,…": "",
                    "折り返し数": "",
                    "幅指定": "",
                    "グループランダマイズ": "",
                    "グループ位置固定": "",
                    "選択肢番号": "",
                    "設問文と選択肢表示": "",
                    "合計値表示": "",
                    "合計値制限": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
        except Exception as exc:
            print(exc)

    # 自由記入短文
    def set_setting_information_of_freeshort_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "グループ設定": "",
                    "キャプション": "",
                    "選択肢": "",
                    "ランダマイズ": "",
                    "表示方向": "",
                    "選択肢数,選択肢数,…": "",
                    "横幅指定": "",
                    "グループ選択肢数,選択肢数,…": "",
                    "折り返し数": "",
                    "幅指定": "",
                    "グループランダマイズ": "",
                    "グループ位置固定": "",
                    "選択肢番号": "",
                    "設問文と選択肢表示": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "グループ設定": "",
                    "キャプション": "",
                    "選択肢": "",
                    "ランダマイズ": "",
                    "表示方向": "",
                    "選択肢数,選択肢数,…": "",
                    "横幅指定": "",
                    "グループ選択肢数,選択肢数,…": "",
                    "折り返し数": "",
                    "幅指定": "",
                    "グループランダマイズ": "",
                    "グループ位置固定": "",
                    "選択肢番号": "",
                    "設問文と選択肢表示": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
        except Exception as exc:
            print(exc)

    # 自由記入長文
    def set_setting_information_of_freelong_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "グループ設定": "",
                    "キャプション": "",
                    "選択肢": "",
                    "ランダマイズ": "",
                    "表示方向": "",
                    "選択肢数,選択肢数,…": "",
                    "横幅指定": "",
                    "グループ選択肢数,選択肢数,…": "",
                    "折り返し数": "",
                    "幅指定": "",
                    "グループランダマイズ": "",
                    "グループ位置固定": "",
                    "選択肢番号": "",
                    "設問文と選択肢表示": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "グループ設定": "",
                    "キャプション": "",
                    "選択肢": "",
                    "ランダマイズ": "",
                    "表示方向": "",
                    "選択肢数,選択肢数,…": "",
                    "横幅指定": "",
                    "グループ選択肢数,選択肢数,…": "",
                    "折り返し数": "",
                    "幅指定": "",
                    "グループランダマイズ": "",
                    "グループ位置固定": "",
                    "選択肢番号": "",
                    "設問文と選択肢表示": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
        except Exception as exc:
            print(exc)

    # 隠し設問MA
    def set_setting_information_of_hidden_multi_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "設問文": "",
                    # 選択肢
                    "選択肢": "",
                    "抽選機能": "",
                    # 設問編集(2)
                    "備考": "",
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "設問文": "",
                    # 選択肢
                    "選択肢": "",
                    "抽選機能": "",
                    # 設問編集(2)
                    "備考": "",
                }
        except Exception as exc:
            print(exc)

    # 画像アップロード
    def set_setting_information_of_image_upload_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "グループ設定": "",
                    "キャプション": "",
                    "選択肢": "",
                    "ランダマイズ": "",
                    "表示方向": "",
                    "選択肢数,選択肢数,…": "",
                    "横幅指定": "",
                    "グループ選択肢数,選択肢数,…": "",
                    "折り返し数": "",
                    "幅指定": "",
                    "グループランダマイズ": "",
                    "グループ位置固定": "",
                    "選択肢番号": "",
                    "設問文と選択肢表示": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "グループ設定": "",
                    "キャプション": "",
                    "選択肢": "",
                    "ランダマイズ": "",
                    "表示方向": "",
                    "選択肢数,選択肢数,…": "",
                    "横幅指定": "",
                    "グループ選択肢数,選択肢数,…": "",
                    "折り返し数": "",
                    "幅指定": "",
                    "グループランダマイズ": "",
                    "グループ位置固定": "",
                    "選択肢番号": "",
                    "設問文と選択肢表示": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
        except Exception as exc:
            print(exc)

    # マトリクスSA
    def set_setting_information_of_matrix_single_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "表上": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "表示形式（PC/iPad）": "",
                        "文字列方向": "",
                        "選択肢番号": ""
                    },
                    "項目": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "文字列方向": "",
                        "選択肢番号": "",
                        "左肩コメント": ""
                    },
                    "必須入力チェック": "",
                    "設問文と選択肢表示": "",
                    "同一回答チェック": "",
                    "順位付けチェック": "",
                    "表頭・表側の位置を入れ替え": "",
                    "表上繰り返し": "",
                    "横幅指定": "",
                    "選択行反転表示": "",
                    "i-タイル設定": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "表上": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "表示形式（PC/iPad）": "",
                        "文字列方向": "",
                        "選択肢番号": ""
                    },
                    "項目": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "文字列方向": "",
                        "選択肢番号": "",
                        "左肩コメント": ""
                    },
                    "必須入力チェック": "",
                    "設問文と選択肢表示": "",
                    "同一回答チェック": "",
                    "順位付けチェック": "",
                    "表頭・表側の位置を入れ替え": "",
                    "表上繰り返し": "",
                    "横幅指定": "",
                    "選択行反転表示": "",
                    "i-タイル設定": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
        except Exception as exc:
            print(exc)

    # マトリクスMA
    def set_setting_information_of_matrix_multi_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "表上": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "選択個数制限": "",
                        "文字列方向": "",
                        "選択肢番号": ""
                    },
                    "項目": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "文字列方向": "",
                        "選択肢番号": "",
                        "左肩コメント": ""
                    },
                    "必須入力チェック": "",
                    "設問文と選択肢表示": "",
                    "表頭・表側の位置を入れ替え": "",
                    "表上繰り返し": "",
                    "横幅指定": "",
                    "選択行反転表示": "",
                    "i-タイル設定": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "表上": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "選択個数制限": "",
                        "文字列方向": "",
                        "選択肢番号": ""
                    },
                    "項目": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "文字列方向": "",
                        "選択肢番号": "",
                        "左肩コメント": ""
                    },
                    "必須入力チェック": "",
                    "設問文と選択肢表示": "",
                    "表頭・表側の位置を入れ替え": "",
                    "表上繰り返し": "",
                    "横幅指定": "",
                    "選択行反転表示": "",
                    "i-タイル設定": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
        except Exception as exc:
            print(exc)

    # マトリクス混合
    def set_setting_information_of_matrix_mix_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "表上": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "文字列方向": "",
                        "選択個数制限": "",
                        "選択肢番号": ""
                    },
                    "項目": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "文字列方向": "",
                        "選択肢番号": "",
                        "左肩コメント": ""
                    },
                    "必須入力チェック": "",
                    "設問文と選択肢表示": "",
                    "矛盾チェック": "",
                    "表頭・表側の位置を入れ替え": "",
                    "表上繰り返し": "",
                    "横幅指定": "",
                    "選択行反転表示": "",
                    "i-タイル設定": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "表上": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "文字列方向": "",
                        "選択個数制限": "",
                        "選択肢番号": ""
                    },
                    "項目": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "文字列方向": "",
                        "選択肢番号": "",
                        "左肩コメント": ""
                    },
                    "必須入力チェック": "",
                    "設問文と選択肢表示": "",
                    "矛盾チェック": "",
                    "表頭・表側の位置を入れ替え": "",
                    "表上繰り返し": "",
                    "横幅指定": "",
                    "選択行反転表示": "",
                    "i-タイル設定": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
        except Exception as exc:
            print(exc)

    # 文章・画像のみ
    def set_setting_information_of_through_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    # 選択肢
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "設問文と選択肢表示": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    # 選択肢
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "設問文と選択肢表示": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
        except Exception as exc:
            print(exc)

    # プロフィール
    def set_setting_information_of_profile_answer(self, convert_question_type=''):
        try:
            if self.mode == 'dev4s' or self.mode == '4s90':
                if convert_question_type == '':
                    return {
                        # 設問編集(1)
                        "設問タイトル": "",
                        "設問タイプ": "",
                        "設問No": "",
                        "コメント上": "",
                        "設問文": "",
                        # 選択肢
                        "選択肢": "",
                        "設問文と選択肢表示": "",
                        # 設問編集(2)
                        "画像": "",
                        "動画貼付": "",
                        "備考": "",
                        "Javascript(設問表示時)": "",
                        "Javascript(次へボタン押下時)": "",
                        "ページ情報(headの最後尾)": "",
                        "エラーチェック": {}
                    }
                else:
                    return {
                        # 設問編集(1)
                        "設問タイトル": "",
                        "設問タイプ": convert_question_type,
                        "設問No": "",
                        "コメント上": "",
                        "設問文": "",
                        # 選択肢
                        "選択肢": "",
                        "設問文と選択肢表示": "",
                        # 設問編集(2)
                        "画像": "",
                        "動画貼付": "",
                        "備考": "",
                        "Javascript(設問表示時)": "",
                        "Javascript(次へボタン押下時)": "",
                        "ページ情報(headの最後尾)": "",
                        "エラーチェック": {}
                    }
            else:
                if convert_question_type == '':
                    return {
                        # 設問編集(1)
                        "設問タイトル": "",
                        "設問タイプ": "",
                        "設問No": "",
                        "コメント上": "",
                        "設問文": "",
                        # 選択肢
                        "選択肢": {
                            "氏名": ["", "", ""],
                            "氏名（ふりがな）": ["", "", ""],
                            "あなたの生年月日": ["", "", ""],
                            "あなたの性別": ["", "", ""],
                            "郵便番号": ["", "", ""],
                            "住所（都道府県）": ["", "", ""],
                            "住所（市区町村）": ["", "", ""],
                            "住所（町名・番地・ビル名など）": ["", "", ""],
                            "電話番号": ["", "", ""],
                            "携帯電話番号": ["", "", ""],
                            "メールアドレス": ["", "", ""],
                            "メールアドレス確認用": ["", "", ""],
                            "会社名": ["", "", ""],
                            "支店名・営業所名": ["", "", ""],
                            "部署名": ["", "", ""],
                            "メールアドレス(＠区切り無し)": ["", "", ""],
                            "メールアドレス確認用(＠区切り無し)": ["", "", ""],
                        },
                        "設問文と選択肢表示": "",
                        # 設問編集(2)
                        "画像": "",
                        "動画貼付": "",
                        "備考": "",
                        "Javascript(設問表示時)": "",
                        "Javascript(次へボタン押下時)": "",
                        "ページ情報(headの最後尾)": "",
                        "エラーチェック": {}
                    }
                else:
                    return {
                        # 設問編集(1)
                        "設問タイトル": "",
                        "設問タイプ": convert_question_type,
                        "設問No": "",
                        "コメント上": "",
                        "設問文": "",
                        # 選択肢
                        "選択肢": {
                            "氏名": ["", "", ""],
                            "氏名（ふりがな）": ["", "", ""],
                            "あなたの生年月日": ["", "", ""],
                            "あなたの性別": ["", "", ""],
                            "郵便番号": ["", "", ""],
                            "住所（都道府県）": ["", "", ""],
                            "住所（市区町村）": ["", "", ""],
                            "住所（町名・番地・ビル名など）": ["", "", ""],
                            "電話番号": ["", "", ""],
                            "携帯電話番号": ["", "", ""],
                            "メールアドレス": ["", "", ""],
                            "メールアドレス確認用": ["", "", ""],
                            "会社名": ["", "", ""],
                            "支店名・営業所名": ["", "", ""],
                            "部署名": ["", "", ""],
                            "メールアドレス(＠区切り無し)": ["", "", ""],
                            "メールアドレス確認用(＠区切り無し)": ["", "", ""],
                        },
                        "設問文と選択肢表示": "",
                        # 設問編集(2)
                        "画像": "",
                        "動画貼付": "",
                        "備考": "",
                        "Javascript(設問表示時)": "",
                        "Javascript(次へボタン押下時)": "",
                        "ページ情報(headの最後尾)": "",
                        "エラーチェック": {}
                    }
        except Exception as exc:
            print(exc)

    # SD法
    def set_setting_information_of_matrix_sd_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "表上": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "文字列方向": "",
                        "選択肢番号": ""
                    },
                    "項目": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢（表左）": "",
                        "選択肢（表右）": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "選択肢番号": "",
                        "左肩コメント": "",
                        "右肩コメント": ""
                    },
                    "必須入力チェック": "",
                    "設問文と選択肢表示": "",
                    "表上繰り返し": "",
                    # "表上下部表示": "",
                    "横幅指定": "",
                    "選択行反転表示": "",
                    "i-タイル設定": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "表上": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "文字列方向": "",
                        "選択肢番号": ""
                    },
                    "項目": {
                        "グループ設定": "",
                        "キャプション": "",
                        "選択肢（表左）": "",
                        "選択肢（表右）": "",
                        "選択肢ランダマイズ": "",
                        "グループランダマイズ": "",
                        "グループ位置固定": "",
                        "選択肢番号": "",
                        "左肩コメント": "",
                        "右肩コメント": ""
                    },
                    "必須入力チェック": "",
                    "設問文と選択肢表示": "",
                    "表上繰り返し": "",
                    # "表上下部表示": "",
                    "横幅指定": "",
                    "選択行反転表示": "",
                    "i-タイル設定": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
        except Exception as exc:
            print(exc)

    # 登録情報設問
    def set_setting_information_of_attribute_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "属性タイプ": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "グループ設定": "",
                    "キャプション": "",
                    "選択肢": "",
                    "ランダマイズ": "",
                    "表示方向": "",
                    "選択肢数,選択肢数,…": "",
                    "横幅指定": "",
                    "グループ選択肢数,選択肢数,…": "",
                    "折り返し数": "",
                    "幅指定": "",
                    "グループランダマイズ": "",
                    "グループ位置固定": "",
                    "必須入力チェック": "",
                    "表示形式": "",
                    "設問文と選択肢表示": "",
                    "選択肢番号": "",
                    "合計値表示": "",
                    "合計値制限": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "属性タイプ": "",
                    "コメント上": "",
                    "設問文": "",
                    "コメント中": "",
                    # 選択肢
                    "グループ設定": "",
                    "キャプション": "",
                    "選択肢": "",
                    "ランダマイズ": "",
                    "表示方向": "",
                    "選択肢数,選択肢数,…": "",
                    "横幅指定": "",
                    "グループ選択肢数,選択肢数,…": "",
                    "折り返し数": "",
                    "幅指定": "",
                    "グループランダマイズ": "",
                    "グループ位置固定": "",
                    "必須入力チェック": "",
                    "表示形式": "",
                    "設問文と選択肢表示": "",
                    "選択肢番号": "",
                    "合計値表示": "",
                    "合計値制限": "",
                    # 設問編集(2)
                    "コメント下": "",
                    "画像": "",
                    "動画貼付": "",
                    "備考": "",
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                    "エラーチェック": {}
                }
        except Exception as exc:
            print(exc)

    # 外部連携設問
    def set_setting_information_of_post_external_answer(self, convert_question_type=''):
        try:
            if convert_question_type == '':
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": "",
                    "設問No": "",
                    "設問文": "",
                    # 選択肢
                    "行き先リサーチURL": "",
                    "想定回答時間": "",
                    "設問文と選択肢表示": "",
                    "戻り先情報": "",
                    # 設問編集(2)
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                }
            else:
                return {
                    # 設問編集(1)
                    "設問タイトル": "",
                    "設問タイプ": convert_question_type,
                    "設問No": "",
                    "設問文": "",
                    # 選択肢
                    "行き先リサーチURL": "",
                    "想定回答時間": "",
                    "設問文と選択肢表示": "",
                    "戻り先情報": "",
                    # 設問編集(2)
                    "Javascript(設問表示時)": "",
                    "Javascript(次へボタン押下時)": "",
                    "ページ情報(headの最後尾)": "",
                }
        except Exception as exc:
            print(exc)

    # STARTページ
    def set_setting_information_of_start_page(self, convert_question_type=''):
        try:
            return {
                # 設問編集(1)
                "アンケートタイトル": "",
                "スタートページ表示": "",
                "スタート設問文": "",
                "「個人情報の取り扱いについて」同意欄": "",
                "スタート個人情報について": "",
                # 設問編集(2)
                "ページ情報(headの最後尾)": "",
            }
        except Exception as exc:
            print(exc)

    # END/COMPページ
    def set_setting_information_of_comp_page(self, convert_question_type=''):
        try:
            return {
                # 設問編集(1)
                "終了タイプ": "",
                "メッセージ": "",
                "自動リダイレクト": "",
                "リンク": "",
                "メッセージ下": "",
                "外部連結　終了通知API": ""
            }
        except Exception as exc:
            print(exc)

    # GATEページ
    def set_setting_information_of_gate_page(self, convert_question_type=''):
        try:
            return {
                # 設問編集(1)
                "終了タイプ": "",
                "メッセージ": "",
                "自動リダイレクト": "",
                "リンク": "",
                "メッセージ下": "",
                "外部連結　終了通知API": "",
                "GATE": ""
            }
        except Exception as exc:
            print(exc)

    # ページ設定
    def set_setting_information_of_setting_page(self, convert_question_type=''):
        try:
            return {
                "タグ": "",
                "ページヘッダー文言": "",
                "ページフッター文言": ""
            }
        except Exception as exc:
            print(exc)

    # メッセージ編集
    def set_setting_information_of_system_message(self, convert_question_type=''):
        try:
            return {
                "実査開始前アクセスエラー": "",
                "実査中(打切り)エラー": "",
                "実査中(重複回答)エラー": "",
                "実査終了後アクセスエラー": "",
                "開始ページのボタン名称": "",
                "次へボタン名称": "",
                "戻るボタン名称": ""
            }
        except Exception as exc:
            print(exc)

    # 初期値をセット
    def set_setting_information(self, question_type):
        try:
            convert_question_type = ''
            # 変換（変換対象のときは初期値をセットした後に「設問タイプ」も書き込む
            if question_type == 'SA':
                question_type = 'SA(単一選択)'
                convert_question_type = question_type
            elif question_type == 'MA':
                question_type = 'MA(複数選択)'
                convert_question_type = question_type
            elif question_type == 'NF':
                question_type = '数値'
                convert_question_type = question_type
            elif question_type == 'HSA':
                question_type = '隠し設問SA'
                convert_question_type = question_type
            elif question_type == 'FS':
                question_type = '自由記入短文'
                convert_question_type = question_type
            elif question_type == 'FL':
                question_type = '自由記入長文'
                convert_question_type = question_type
            elif question_type == 'HMA':
                question_type = '隠し設問MA'
                convert_question_type = question_type
            elif question_type == 'IUP':
                question_type = '画像アップロード'
                convert_question_type = question_type
            elif question_type == 'MTS':
                question_type = 'マトリクスSA'
                convert_question_type = question_type
            elif question_type == 'MTM':
                question_type = 'マトリクスMA'
                convert_question_type = question_type
            elif question_type == 'MTX':
                question_type = 'マトリクス混合'
                convert_question_type = question_type
            elif question_type == 'THR':
                question_type = '文章・画像のみ'
                convert_question_type = question_type
            elif question_type == 'PRO':
                question_type = 'プロフィール'
                convert_question_type = question_type
            elif question_type == 'SD':
                question_type = 'SD法'
                convert_question_type = question_type
            elif question_type == 'XXX':
                question_type = '登録情報設問'
                convert_question_type = question_type
            elif question_type == 'XXX2':
                question_type = '外部連携設問'
                convert_question_type = question_type
            elif question_type.find('<sa>') != -1:
                question_type = 'SA(単一選択)'
                convert_question_type = question_type
            elif question_type.find('<ma>') != -1:
                question_type = 'MA(複数選択)'
                convert_question_type = question_type
            elif question_type.find('<fs=') != -1:
                question_type = '自由記入短文'
                convert_question_type = question_type
            elif question_type.find('<fl=') != -1:
                question_type = '自由記入長文'
                convert_question_type = question_type
            # 初期値をセット
            if question_type == 'SA(単一選択)':
                return self.set_setting_information_of_single_answer(convert_question_type)
            elif question_type == 'MA(複数選択)':
                return self.set_setting_information_of_multi_answer(convert_question_type)
            elif question_type == '数値':
                return self.set_setting_information_of_number_answer(convert_question_type)
            elif question_type == '隠し設問SA':
                return self.set_setting_information_of_hidden_single_answer(convert_question_type)
            elif question_type == '自由記入短文':
                return self.set_setting_information_of_freeshort_answer(convert_question_type)
            elif question_type == '自由記入長文':
                return self.set_setting_information_of_freelong_answer(convert_question_type)
            elif question_type == '隠し設問MA':
                return self.set_setting_information_of_hidden_multi_answer(convert_question_type)
            elif question_type == '画像アップロード':
                return self.set_setting_information_of_image_upload_answer(convert_question_type)
            elif question_type == 'マトリクスSA':
                return self.set_setting_information_of_matrix_single_answer(convert_question_type)
            elif question_type == 'マトリクスMA':
                return self.set_setting_information_of_matrix_multi_answer(convert_question_type)
            elif question_type == 'マトリクス混合':
                return self.set_setting_information_of_matrix_mix_answer(convert_question_type)
            elif question_type == '文章・画像のみ':
                return self.set_setting_information_of_through_answer(convert_question_type)
            elif question_type == 'プロフィール':
                return self.set_setting_information_of_profile_answer(convert_question_type)
            elif question_type == 'SD法':
                return self.set_setting_information_of_matrix_sd_answer(convert_question_type)
            elif question_type == '登録情報設問':
                return self.set_setting_information_of_attribute_answer(convert_question_type)
            elif question_type == '外部連携設問':
                return self.set_setting_information_of_post_external_answer(convert_question_type)
            elif question_type == 'START':
                return self.set_setting_information_of_start_page(convert_question_type)
            elif question_type == 'COMP' or question_type.find('END') > -1:
                return self.set_setting_information_of_comp_page(convert_question_type)
            elif question_type == 'GATE':
                return self.set_setting_information_of_gate_page(convert_question_type)
            elif question_type == 'ページ設定':
                return self.set_setting_information_of_setting_page(convert_question_type)
            elif question_type == 'メッセージ編集':
                return self.set_setting_information_of_system_message(convert_question_type)
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - 画面上の設問/終了ページをすべて削除
    def initialize_research_question(self):
        try:
            # 設問を削除（初期化するために1問追加して削除）
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.add_question_last_click()
            xpath = '//div[@class="loading"]/img'
            if self.is_wait_until_element_not_displayed(xpath):
                xpath = '//input[@name="qu_id_check[]"]'
                if self.dom_loading_wait(xpath):
                    elements =self.driver.find_elements_by_xpath(xpath)
                    for element in elements:
                        element.click()
                    # 設問削除 - クリックした設問を削除する
                    self.sub_window_operation('設問削除', ['//input[starts-with(@value,"削除する")]'])
            # ENDページを削除
            if self.get_count_unset_end_pages() > 0:
                xpath = '//div[@class="loading"]/img'
                if self.is_wait_until_element_not_displayed(xpath):
                    # ENDページを削除
                    xpath = '//input[@type="checkbox"][@name="pg_id_check[]"]'
                    if self.dom_loading_wait(xpath):
                        elements =self.driver.find_elements_by_xpath(xpath)
                        for element in elements:
                            element.click()
                        # 設問削除 - クリックした設問を削除する
                        self.sub_window_operation('設問削除', ['//input[starts-with(@value,"削除する")]'])
            # Ajax読み込み待機
            self.ajax_loading_wait('//div[@class="loading"]/img')
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - 画面上の設問/終了ページをすべて削除　※設問/ENDにチェックがついてなければ処理をスキップ追加
    def sub_window_operation(self, operation, array):
        try:
            # サブウインドウをクリック
            self.action_sub_window_click(operation)
            # 子ウインドウが表示されるまで待って切り替える
            count = 0
            retry = 1
            while True:
                if len(self.driver.window_handles) > 1:
                    break
                if count >= 150 and retry > 0:
                    # 15秒経過して window_handles が 1つのとき再度クリック
                    print('[子ウインドウ]-------------------------------')
                    print('リトライしました' + str(count) + 'ミリ秒')
                    retry -= 1
                    count = 0
                    if operation == '設問削除':
                        # サブウインドウを再度クリック
                        self.action_sub_window_click(operation)
                if count >= 300:
                    print('[子ウインドウ]-------------------------------')
                    print('タイムアウト:' + str(count) + 'ミリ秒')
                    break
                # self.time.sleep(0.1)
                count += 1
            all_handles = self.driver.window_handles
            self.driver.switch_to_window(all_handles[1])
            # self.time.sleep(0.5)
            # 各サブウインドウ毎の操作
            if operation == '設問一括追加':
                action_count = 0
                for array_value in array:
                    if array_value == '':
                        pass
                    else:
                        # 追加する設問の数の操作
                        if action_count == 3:
                            self.clear_text(xpath)
                            self.item_send(xpath, array_value)
                        # プルダウンとかクリック系操作
                        else:
                            xpath = array_value
                            self.item_click(xpath)
                    action_count += 1
            elif operation == '途中終了追加':
                action_count = 0
                for array_value in array:
                    # 追加する設問の数の操作
                    if action_count == 2:
                        self.clear_text(xpath)
                        self.item_send(xpath, array_value)
                    # プルダウンとかクリック系操作
                    else:
                        xpath = array_value
                        self.item_click(xpath)
                    action_count += 1
            elif operation == 'ページ設定':
                self.item_send_element_key_by_name('textarea', 'タグ', 'data[tag]', array)
                self.item_send_element_key_by_name('textarea', 'ページヘッダー文言', 'data[header]', array)
                self.item_send_element_key_by_name('textarea', 'ページフッター文言', 'data[footer]', array)
                self.item_click('//span[@class="linkTypeA03"]/a')
            elif operation == 'メッセージ編集':
                self.item_send_element_key_by_name('input', '実査開始前アクセスエラー', 'data[research_not_yet_open]', array)
                self.item_send_element_key_by_name('input', '実査中(打切り)エラー', 'data[research_reached]', array)
                self.item_send_element_key_by_name('input', '実査中(重複回答)エラー', 'data[research_answered]', array)
                self.item_send_element_key_by_name('input', '実査終了後アクセスエラー', 'data[research_closed]', array)
                self.item_send_element_key_by_name('input', '開始ページのボタン名称', 'data[start_next]', array)
                self.item_send_element_key_by_name('input', '次へボタン名称', 'data[next]', array)
                self.item_send_element_key_by_name('input', '戻るボタン名称', 'data[back]', array)
                self.item_click('//li[@class="linkTypeA03"]/a')
            else:
                for array_value in array:
                    xpath = array_value
                    self.item_click(xpath)
            # 親ウインドウへ戻る
            self.driver.switch_to_window(all_handles[0])
            self.time.sleep(0.5)
        except Exception as exc:
            print(exc)

    # アンケート画面編集 - 下部の（設問コピーや削除ボタン）クリック
    def action_sub_window_click(self, operation):
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if operation == '設問削除':
                self.open_delete_confirm_window_click()
            elif operation == '設問一括追加':
                self.open_add_confirm_window_click()
            elif operation == '途中終了追加':
                self.open_add_end_page_window_click()
            elif operation == '設問移動':
                self.open_move_confirm_window_click()
            elif operation == 'メッセージ編集':
                self.open_move_confirm_system_message_click()
            elif operation == 'ページ設定':
                self.open_move_confirm_setting_page_click()
            return False
        except Exception as exc:
            print(exc)

