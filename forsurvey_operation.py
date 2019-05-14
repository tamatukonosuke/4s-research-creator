from forsurvey_class import forSurvey

import datetime
import json
import codecs

class forSurveyOperation:
    def __init__(self, mode='None'):
        # Basic認証/ログイン情報を読み込む
        self.browser = forSurvey(mode)

    # mappsコアとforSurveyへのログイン
    def mappscore_and_forsurvey_login(self, group, research_no, value='normal'):
        try:
            # ブラウジングモード設定
            self.browser.set_browser_mode(value)
            # forSurveyログイン
            self.browser.login()
            # グループ切り替え
            self.browser.change_select_group(group)
            # 指定したリサーチへアクセス
            self.browser.search_by_research_no(research_no)
        except Exception as exc:
            print(exc)

    # headlessモードでログインしてすべての設問の設定情報を書き出す
    def get_forsurvey_setting_by_headless_mode(self, group, research_no, mode='None'):
        try:
            # headlessモードでログイン
            self.mappscore_and_forsurvey_login(group, research_no, 'headless')
            # 90番のみ、MYリサーチ一覧がアコーディオンになっている対応
            if self.browser.mode == 'dev4s' or self.browser.mode == '4s90':
                self.browser.research_accordion_open()
            # アンケート画面編集へ遷移
            self.browser.my_research_iconMenu_click('アンケート画面編集')
            # 設定取得して書き出し
            self.all_question_setting_information_file_write({
                '設問編集出力': 'on',
                '画面キャプチャ': 'on',
                'ページ設定': 'on',
                'メッセージ編集': 'on',
                '条件分岐出力': 'on',
                'ディレクトリ名': research_no
            })
        except Exception as exc:
            print(exc)

    # 通常モード（ブラウザ起動）でログインしてすべての設問の設定情報を書き出す
    def get_forsurvey_setting_by_browser_mode(self, group, research_no, mode='None'):
        try:
            # headlessモードでログイン
            self.mappscore_and_forsurvey_login(group, research_no, 'normal')
            # 90番のみ、MYリサーチ一覧がアコーディオンになっている対応
            if self.browser.mode == 'dev4s' or self.browser.mode == '4s90':
                self.browser.research_accordion_open()
            # アンケート画面編集へ遷移
            self.browser.my_research_iconMenu_click('アンケート画面編集')
            # 設定取得して書き出し
            self.all_question_setting_information_file_write({
                '設問編集出力': 'on',
                '画面キャプチャ': 'on',
                'ページ設定': 'on',
                'メッセージ編集': 'on',
                '条件分岐出力': 'on',
                'ディレクトリ名': research_no
            })
        except Exception as exc:
            print(exc)

    # 通常モード（ブラウザ起動）でログインしてすべての設問を作成する
    def edit_forsurvey_by_browser_mode(self, file_name, group, research_no, mode='None'):
        try:
            # headlessモードでログイン
            self.mappscore_and_forsurvey_login(group, research_no, 'normal')
            # 書き出した情報からリサーチを新規作成（コピー）する
            self.edit_new_research(str(file_name), str(research_no))
        except Exception as exc:
            print(exc)

    # リサーチのすべての設問の設定情報をファイルに書き出す
    def all_question_setting_information_file_write(self, array, dir_path='./', file_name=''):
        try:
            # アンケート画面編集に切り替わらなければ実行中断（終了）
            if self.browser.check_browser_path('アンケート画面編集') == False:
                print('[エラー] 実行中断しました')
                print('d:', datetime.datetime.today())
                return False

            body = {}
            page_numbers = []
            page_quids = []
            page_pgids = []
            page_count = -1
            prev_page = ''
            self.browser.get_my_research_page_number_all(page_numbers, page_quids, page_pgids)
            page_question_number = []
            page_question_type = []
            none_end_quids = []
            self.browser.get_my_research_page_question_number_and_type(page_question_number, page_question_type, none_end_quids)
            # ページを巡回して設定情報を取得
            print("[ページの巡回開始]-------------------------------")
            print('d:', datetime.datetime.today())
            for page_number in page_numbers:
                page_count += 1
                # 設定されていない設問のときは情報を収集しない
                javascript_code = "javascript:gotoEditQuestion('" + str(page_quids[page_count]) + "');"
                xpath = '//a[@href="' + javascript_code + '"]/ancestor::tr[@class="questions-list"]/td[@class="questionSentence"]/a/span[starts-with(@class, "unsetting")]'
                unset_question_count = len(self.browser.driver.find_elements_by_xpath(xpath))
                if unset_question_count > 0:
                    # 設問編集の設定情報を取得
                    if array.get('設問編集出力') is None:
                        pass
                    else:
                        if array['設問編集出力'] == 'on':
                            body[page_count] = self.browser.set_setting_information('SA(単一選択)')
                            body[page_count]['ページ番号'] = page_number
                            body[page_count]['Qナンバー'] = page_quids[page_count]
                            body[page_count]['設問文'] = self.browser.driver.find_element_by_xpath(xpath).text
                else:
                    # 目的のページへ遷移する
                    self.browser.jump_to_target_pages(page_number, page_quids[page_count])
                    # 設問編集の設定情報を取得
                    if array.get('設問編集出力') is None:
                        pass
                    else:
                        if array['設問編集出力'] == 'on':
                            if page_number.find('START') == -1 and page_number.find('COMP') == -1 and page_number.find('END') == -1 and page_number.find('GATE') == -1:
                                # 現在選択中設問タイプ
                                question_type = self.browser.current_selecting_question_type_get()
                                body[page_count] = self.browser.set_setting_information(question_type)
                                body[page_count]['Qナンバー'] = page_quids[page_count]
                            elif page_number == 'START' or page_number == 'COMP' or page_number.find('END') > -1 or page_number == 'GATE':
                                body[page_count] = self.browser.set_setting_information(page_number)
                            # 90番環境に「キャプション」は存在しないのでキーを削除
                            if self.browser.mode == 'dev4s' or self.browser.mode == '4s90':
                                self.browser.delete_old_forsurvey_setting_information(body[page_count])
                            # 90番環境以外は「i-タイル設定」は存在しないのでキーを削除
                            else:
                                self.browser.delete_new_forsurvey_setting_information(body[page_count])

                            # 設問編集 - 設定情報を取得
                            self.browser.convert_edit_question_by_page(page_number, body[page_count])
                            body[page_count]['ページ番号'] = page_number
                            print('[処理済み] 設定情報の取得が完了しました -> ' + str(body[page_count]['ページ番号']))
                            print('d:', datetime.datetime.today())
                        elif array['設問編集出力'] == 'off':
                            body[page_count] = {'設問No': ''}
                            self.browser.convert_edit_question_selecting_question_number('設問No', body[page_count])

                        # 設問編集のスクリーンショットを取得
                        # キャプチャのファイル名を設問Noにする（ENDやCOMPはページ番号）
                        pic_number = 'Error'
                        if body[page_count].get('設問No') is None:
                            pic_number = str(body[page_count]['ページ番号'])
                        else:
                            if body[page_count]['設問No'] == '':
                                pic_number = str(page_number)
                            else:
                                pic_number = body[page_count]['設問No']
                        if array.get('画面キャプチャ') is None:
                            pass
                        else:
                            if array['画面キャプチャ'] == 'on':
                                self.browser.question_display_screenshot_by_page(pic_number, array)
                                print('[処理済み] 画面キャプチャの取得が完了しました -> ' + str(pic_number))
                                print('d:', datetime.datetime.today())
                        # 画面編集に戻る
                        self.browser.back_to_screen_edit()
                        if page_number.find('START') == -1 and page_number.find('COMP') == -1 and page_number.find('END') == -1 and page_number.find('GATE') == -1:
                            # 開いた設問単体プレビューを閉じる
                            xpath = '//div[@id="preview_' + str(page_quids[page_count]) + '"]/ul[@class="listTypeB01"]/li[@class="linkTypeA14"]/a'
                            self.browser.item_click(xpath)

                # 条件分岐
                if array.get('条件分岐出力') is None:
                    pass
                else:
                    if array['条件分岐出力'] == 'on':
                        # 1つ前のページと同じページ番号だと改ページONしてくから条件分岐ボタンが存在しないのでスキップ
                        if page_numbers[page_count] == prev_page:
                            pass
                        else:
                            xpath = '//td[starts-with(@class, "setting02")]/a[starts-with(@href, "javascript:openEditConditionConfirmWindow(")]/img/ancestor::tr[1]/td[@class="pageNo"]/a'
                            elements = self.browser.driver.find_elements_by_xpath(xpath)
                            for element in elements:
                                # tmp_pgid = element.get_attribute('id')
                                tmp_pgid = element.text
                                tmp_quid = element.get_attribute('href').split('(')[1][1:5]
                                tmp_pgnum = page_numbers[page_count]
                                tmp_pquid = page_quids[page_count]
                                # 現在取得した設問の右に[条]があれば条件分岐を取得する
                                if ( tmp_pgid == tmp_pgnum and tmp_quid == tmp_pquid ) or ( tmp_pgid == tmp_pgnum and page_numbers[page_count] == tmp_pgid ):
                                    if tmp_pgid == tmp_pgnum and tmp_quid == tmp_pquid:
                                        javascript_code = "javascript:gotoEditQuestion('" + str(tmp_quid) + "');"
                                        # 設問タイプアイコン
                                        xpath = '//a[@href="' + javascript_code + '"]/ancestor::tr[1]/td[@class="type"]/label/img'
                                        # 未設定の設問は設問タイプアイコンがないので対策
                                        unset_question_count = len(self.browser.driver.find_elements_by_xpath(xpath))
                                        if unset_question_count == 0:
                                            question_type = ''
                                        else :
                                            question_type = self.browser.driver.find_element_by_xpath(xpath).get_attribute('alt')
                                        # 条件分岐アイコン
                                        xpath = '//a[@href="' + javascript_code + '"]/ancestor::tr[1]/td[starts-with(@class, "setting02")]'
                                        logic = self.browser.driver.find_element_by_xpath(xpath).get_attribute('class')
                                    else:
                                        javascript_code = "javascript:openEditConditionConfirmWindow('" + str(tmp_pquid) + "');"
                                        # 設問タイプアイコン
                                        question_type = '終了'
                                        # 条件分岐アイコン
                                        xpath = '//a[@href="' + javascript_code + '"]/parent::td'
                                        logic = self.browser.driver.find_element_by_xpath(xpath).get_attribute('class')
                                    # class名が「setting02」は条件分岐なし、「setting02a」はあり
                                    if logic == 'setting02a':
                                        body[page_count]['条件分岐'] = {}
                                        body[page_count]['条件分岐']['結合式'] = ''
                                        # サブウインドウをクリック
                                        self.browser.item_click(xpath + '/a')
                                        # 子ウインドウが表示されるまで待って切り替える
                                        count = 0
                                        retry = 1
                                        while True:
                                            if len(self.browser.driver.window_handles) > 1:
                                                break
                                            if count >= 150 and retry > 0:
                                                # 15秒経過して window_handles が 1つのとき再度クリック
                                                print('[子ウインドウ]-------------------------------')
                                                print('リトライしました' + str(count) + 'ミリ秒')
                                                retry -= 1
                                                count = 0
                                                # サブウインドウを再度クリック
                                                # self.browser.action_sub_window_click(value)
                                                self.browser.item_click(xpath + '/a')
                                            if count >= 300:
                                                print('[子ウインドウ]-------------------------------')
                                                print('タイムアウト:' + str(count) + 'ミリ秒')
                                                break
                                            # self.browser.time.sleep(0.1)
                                            count += 1
                                        all_handles = self.browser.driver.window_handles
                                        self.browser.driver.switch_to_window(all_handles[1])
                                        # サブウインドウの操作
                                        # 条件分岐
                                        # 90番環境は条件分岐がCoDe文キーを削除
                                        if self.browser.mode == 'dev4s' or self.browser.mode == '4s90':
                                            del body[page_count]['条件分岐']['結合式']
                                            body[page_count]['条件分岐']['条件式'] = self.browser.get_item_text('//textarea[@name="syntax"]')
                                        else:
                                            self.browser.convert_edit_question_condition_setting('条件分岐', page_question_number, page_question_type, body[page_count])
                                        # 閉じる
                                        self.browser.item_click('//input[@type="button"][@value="閉じる"]')
                                        # 親ウインドウへ戻る
                                        self.browser.driver.switch_to_window(all_handles[0])
                                        self.browser.time.sleep(0.5)
                if array.get('設問編集出力') is None:
                    pass
                else:
                    if array['設問編集出力'] == 'on':
                        # ファイルに書き出す
                        if len(file_name) == 0:
                            new_file_name = self.browser.get_research_number_of_edit_question() + '.txt'
                        else:
                            new_file_name = file_name + '.txt'
                        self.browser.save_file_at_new_dir(str(dir_path), new_file_name, body)
                prev_page = page_numbers[page_count]
            # ページ設定
            if array.get('ページ設定') is None:
                pass
            else:
                body['ページ設定'] = self.browser.set_setting_information('ページ設定')
                self.browser.convert_edit_question_setting_page('ページ設定', body)
                # ファイルに書き出す
                if len(file_name) == 0:
                    new_file_name = self.browser.get_research_number_of_edit_question() + '.txt'
                else:
                    new_file_name = file_name + '.txt'
                self.browser.save_file_at_new_dir(str(dir_path), new_file_name, body)
            # メッセージ編集
            if array.get('メッセージ編集') is None:
                pass
            else:
                body['メッセージ編集'] = self.browser.set_setting_information('メッセージ編集')
                self.browser.convert_edit_question_system_message('メッセージ編集', body)
                # ファイルに書き出す
                if len(file_name) == 0:
                    new_file_name = self.browser.get_research_number_of_edit_question() + '.txt'
                else:
                    new_file_name = file_name + '.txt'
                self.browser.save_file_at_new_dir(str(dir_path), new_file_name, body)
            print('[処理済み] すべての処理が完了しました')
            print('d:', datetime.datetime.today())

            # ブラウザ処理終了
            self.browser.browser_exit()
        except Exception as exc:
            print(exc)

    # アンケート画面編集に遷移した状態からリサーチを作成
    def edit_new_research(self, open_file_name, reserch_no):
        try:
            print("[作成開始]------------------------------- -> " + open_file_name + " / " + reserch_no)
            print('d:', datetime.datetime.today())
            with codecs.open(open_file_name, encoding='utf-8') as f:
                steps = json.load(f)

            # リサーチが作成されていなければ中断
            if self.browser.get_number_of_displayed_project() == 0:
                print('[エラー] リサーチが存在しません。 -> ' + str(reserch_no))
                print('d:', datetime.datetime.today())
                return False

            # 90番のみ、MYリサーチ一覧がアコーディオンになっている対応
            if self.browser.mode == 'dev4s' or self.browser.mode == '4s90':
                self.browser.research_accordion_open()

            self.browser.my_research_iconMenu_click('アンケート画面編集')

            # アンケート画面編集に切り替わらなければ実行中断（終了）
            if self.browser.check_browser_path('アンケート画面編集') == False:
                print('[エラー] 実行中断しました')
                print('d:', datetime.datetime.today())
                return False

            # 画面上の設問/終了ページをすべて削除
            self.browser.initialize_research_question()

            # 必要な設問を追加するためにQナンバーの最大値を取得し、quidsに格納
            max_quid = 0
            quids = []
            for step in steps:
                quid = steps[step].get('Qナンバー')
                if quid is None:
                    pass
                else:
                    if max_quid < int(quid):
                        max_quid = int(quid)
                    quids.append(quid)
            print('[処理済み] Qナンバー最大値の取得が完了しました')
            print('d:', datetime.datetime.today())

            # 設問一括追加 - 設問をQナンバー最大値分追加して存在しないQナンバーの設問を削除
            if max_quid > 1:
                # 最大追加が1回で99問対策
                while max_quid > 99:
                    # 設問一括追加
                    self.browser.sub_window_operation('設問一括追加', ['', '//select[@name="offset"]/option[@value="after"]', '//input[@name="num"]', 99, '//input[starts-with(@value,"追加する")]'])
                    max_quid -= 99
                    # Ajax読み込み待機
                    self.browser.ajax_loading_wait('//div[@class="loading"]/img')
                    # 存在しないQナンバー選択
                    xpath = '//input[@name="qu_id_check[]"]'
                    if self.browser.dom_loading_wait(xpath):
                        elements = self.browser.driver.find_elements_by_xpath(xpath)
                        for element in elements:
                            quid = element.get_attribute('value')
                            if quid in quids:
                                pass
                            else:
                                element.click()
                    # 最後のQナンバーを消すと設問追加でQナンバーの値が増加しないので最大Qナンバーが選択されてたら解除
                    element_max_quid = str(self.browser.get_my_research_max_q_number())
                    xpath = '//input[@name="qu_id_check[]"][@value="' + str(element_max_quid) + '"]'
                    if self.browser.dom_loading_wait(xpath):
                        if self.browser.driver.find_elements_by_xpath(xpath)[0].is_selected():
                            self.browser.item_click(xpath)
                    # 設問削除
                    self.browser.sub_window_operation('設問削除', ['//input[starts-with(@value,"削除する")]'])
                    # Ajax読み込み待機
                    self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            if max_quid > 1:
                self.browser.sub_window_operation('設問一括追加', ['', '//select[@name="offset"]/option[@value="after"]', '//input[@name="num"]', int(max_quid), '//input[starts-with(@value,"追加する")]'])
            # Ajax読み込み待機
            self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            print('[処理済み] 設問一括追加が完了しました')
            print('d:', datetime.datetime.today())
            # 存在しないQナンバー選択
            xpath = '//input[@name="qu_id_check[]"]'
            chk_count = 0
            if self.browser.dom_loading_wait(xpath):
                elements = self.browser.driver.find_elements_by_xpath(xpath)
                for element in elements:
                    quid = element.get_attribute('value')
                    if quid in quids:
                        pass
                    else:
                        element.click()
                        chk_count = chk_count + 1
            print('[処理済み] 存在しないQナンバーの選択が完了しました')
            print('d:', datetime.datetime.today())
            # 設問削除
            if chk_count > 0:
                self.browser.sub_window_operation('設問削除', ['//input[starts-with(@value,"削除する")]'])
                # Ajax読み込み待機
                self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            print('[処理済み] 不要な設問の削除が完了しました')
            print('d:', datetime.datetime.today())
            # Ajax読み込み待機
            self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            # 設問の順番を並び替える（順番は後ろから）
            quids = []
            for step in steps:
                quid = steps[step].get('Qナンバー')
                if quid is None:
                    pass
                else:
                    quids.append(quid)
            # quids.reverse()
            count = 0
            for quid in quids:
                if count == 0:
                    pass
                else:
                    # Ajax読み込み待機
                    self.browser.ajax_loading_wait('//div[@class="loading"]/img')
                    # 設問をクリック
                    xpath = '//input[@name="qu_id_check[]"][@value="' + str(quid) + '"]'
                    self.browser.item_click(xpath)
                    # 設問移動
                    self.browser.sub_window_operation('設問移動', ['//select[@name="base_qu_id"]/option[starts-with(@value, "' + str(prev_quid) + '")]', '', '//input[starts-with(@value,"移動する")]'])
                prev_quid = quid
                count += 1
            print('[処理済み] 設問の順番の並び替えが完了しました')
            print('d:', datetime.datetime.today())
            # Ajax読み込み待機
            self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            # 設問入力/設定の開始
            prev_page = ''
            # end_pages = []
            page_number = 0
            for step in steps:
                # ページ設定、メッセージ編集など「ページ番号」をもたない設定はスキップ
                if steps[step].get('ページ番号') is None:
                    pass
                else:
                    # ENDページは設問を作成した後に追加したいからスキップ
                    if steps[step]['ページ番号'].find('P') == 0:
                        page_number += 1
                        print('[設問作成][ ' + str(steps[step]['ページ番号']) + ' ]-------------------------------')
                        print('d:', datetime.datetime.today())
                        # 未設定の設問もスキップ対策
                        if steps[step]['設問タイプ'] == '':
                            pass
                        else:
                            self.browser.edit_new_question('P' + str(page_number), steps[step], prev_page=prev_page)
                    elif steps[step]['ページ番号'].find('START') >= 0 or steps[step]['ページ番号'].find('COMP') >= 0:
                        self.browser.edit_new_question(str(steps[step]['ページ番号']), steps[step], prev_page=prev_page)
                    # 作成が終わったページを1つ前のページ番号として保存
                    prev_page = str(steps[step]['ページ番号'])
            # 改ページ準備
            # 作成予定のページ番号を取得：START,COMP,END,GATEは含まない
            plan_pages = []
            for step in steps:
                array_value = steps[step].get('ページ番号')
                if array_value is None:
                    pass
                else:
                    if array_value.find('START') == -1 and array_value.find('COMP') == -1 and array_value.find('END') == -1 and array_value.find('GATE') == -1:
                        plan_pages.append(array_value)
            # 改ページボタンHTMLと紐づけ表を作成
            kaipage_quid = []
            xpath = '//td[@class="setting01"]/a'
            if self.browser.dom_loading_wait(xpath):
                elements = self.browser.driver.find_elements_by_xpath(xpath)
                for element in elements:
                    # 改ページボタンが表示されてるQナンバー
                    kaipage_quid.append(element.get_attribute('href')[22:26])
            page_numbers = []
            page_quids = []
            self.browser.get_my_research_page_number_only(page_quids, page_numbers)
            print('[処理済み] 改ページに必要なページ番号の取得が完了しました')
            print('d:', datetime.datetime.today())
            page_count = 0
            # 改ページの開始
            for plan_page in plan_pages:
                page_count += 1
                if page_count >= len(plan_pages):
                    pass
                else:
                    # ページと次のページが同じページ番号のとき、ページの改ページボタンを押す
                    if plan_page == plan_pages[page_count]:
                        xpath = '//td[@class="setting01"]/a'
                        if self.browser.dom_loading_wait(xpath):
                            elements = self.browser.driver.find_elements_by_xpath(xpath)
                            elements[kaipage_quid.index(page_quids[page_count-1])].click()
                            # Ajax読み込み待機
                            self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            print('[処理済み] 改ページが完了しました')
            print('d:', datetime.datetime.today())
            # ENDページ追加準備
            page_numbers = []
            page_quids = []
            page_pgids = []
            self.browser.get_my_research_page_number_all(page_numbers, page_quids, page_pgids)
            max_end_pgid = 0
            for step in steps:
                quid = steps[step].get('Qナンバー')
                if quid is None:
                    # ENDページの最大値を取得
                    end_pgid = steps[step].get('終了タイプ')
                    if end_pgid is None:
                        pass
                    else:
                        if end_pgid.find('END') >= 0:
                            end_pgid_number = end_pgid[3:len(end_pgid)]
                            if max_end_pgid < int(end_pgid_number):
                                max_end_pgid = int(end_pgid_number)
            # Qナンバーの後ろから2番目（COMPの前の設問）の後ろに一括でENDページ追加
            self.browser.sub_window_operation('途中終了追加', ['//select[@name="pg_id"]/option[@value="' + str(page_pgids[len(page_pgids) - 2]) + '"]', '//input[@name="num"]', max_end_pgid - 1, '//input[starts-with(@value,"追加する")]'])
            print('[処理済み] ENDページの一括追加が完了しました')
            print('d:', datetime.datetime.today())
            # Ajax読み込み待機
            self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            end_pages = []
            for step in steps:
                end_type = steps[step].get('終了タイプ')
                if end_type is None:
                    pass
                else:
                    if end_type.find('END') >= 0:
                        if end_type != 'END1':
                            end_pages.append(end_type)
            delete_end_pages = []
            for count in range(2, max_end_pgid + 1):
                if 'END' + str(count) in end_pages:
                    pass
                else:
                    delete_end_pages.append('END' + str(count))
            # 不要なENDページ一括削除
            if len(delete_end_pages) > 0:
                page_numbers = []
                page_quids = []
                page_pgids = []
                self.browser.get_my_research_page_number_all(page_numbers, page_quids, page_pgids)
                for page_value in delete_end_pages:
                    select_option_value = page_pgids[page_numbers.index(page_value)]
                    xpath = '//input[@name="pg_id_check[]"][@value="' + str(select_option_value) + '"]'
                    self.browser.item_click(xpath)
                # 設問削除 - クリックした設問を削除する
                self.browser.sub_window_operation('設問削除', ['//input[starts-with(@value,"削除する")]'])
                # Ajax読み込み待機
                self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            print('[処理済み] ENDページの削除が完了しました')
            print('d:', datetime.datetime.today())
            page_numbers = []
            page_quids = []
            page_pgids = []
            self.browser.get_my_research_page_number_all(page_numbers, page_quids, page_pgids)
            page_numbers_unique = sorted(set(page_numbers), key=page_numbers.index)
            pages = []
            for step in steps:
                array_value = steps[step].get('ページ番号')
                if array_value is None:
                    pass
                else:
                    if array_value == 'GATE':
                        array_value = steps[step].get('終了タイプ')
                        if array_value is None:
                            pass
                        else:
                            pages.append(array_value)
                    else:
                        pages.append(array_value)
            # ついに！ENDページ移動
            for page in pages:
                if page.find('END') == -1:
                    pass
                # 移動対象ENDページ処理
                else:
                    xpath = '//input[@name="pg_id_check[]"][@value="' + str(page_pgids[page_numbers_unique.index(page)]) + '"]'
                    self.browser.item_click(xpath)
                    # 設問移動
                    self.browser.sub_window_operation('設問移動', ['//select[@name="base_pg_id"]/option[@value="' + str(page_pgids[page_numbers_unique.index(prev_page)]) + '"]', '', '//input[starts-with(@value,"移動する")]'])
                    # Ajax読み込み待機
                    self.browser.ajax_loading_wait('//div[@class="loading"]/img')
                # 1つ前のページ
                prev_page = page
            print('[処理済み] ENDページの移動が完了しました')
            print('d:', datetime.datetime.today())
            # 移動させたらENDを編集
            prev_page = ''
            for step in steps:
                # ページ設定、メッセージ編集など「ページ番号」をもたない設定はスキップ
                if steps[step].get('ページ番号') is None:
                    pass
                else:
                    # ENDページを編集
                    if steps[step]['ページ番号'].find('GATE') == 0 or steps[step]['ページ番号'].find('END') == 0:
                        self.browser.edit_new_question(steps[step]['終了タイプ'], steps[step])
            # 条件分岐
            for step in steps:
                # 条件分岐をもたない設定はスキップ
                if steps[step].get('条件分岐') is None:
                    pass
                else:
                    page_numbers = []
                    page_quids = []
                    page_pgids = []
                    self.browser.get_my_research_page_number_all(page_numbers, page_quids, page_pgids)
                    page_question_number = []
                    page_question_type = []
                    none_end_quids = []
                    self.browser.get_my_research_page_question_number_and_type(page_question_number, page_question_type, none_end_quids)
                    # page_numbersの重複を削除
                    page_numbers_unique = sorted(set(page_numbers), key=page_numbers.index)
                    # GATEは条件分岐が存在しないから page_pgids を取得できない。キーを削除。
                    for page_numbers_gate in page_numbers_unique:
                        if page_numbers_gate == 'GATE':
                             page_numbers_unique.remove('GATE')
                    # 頁Noから条件分岐のボタンのJavaScriptの引数を取得
                    page_index = page_pgids[page_numbers_unique.index(steps[step]['ページ番号'])]
                    javascript_code = "javascript:openEditConditionConfirmWindow('" + str(page_index) + "');"
                    # 条件分岐を編集
                    xpath = '//a[@href="' + javascript_code + '"]'
                    # サブウインドウをクリック
                    self.browser.item_click(xpath)
                    # 子ウインドウが表示されるまで待って切り替える
                    count = 0
                    retry = 1
                    while True:
                        if len(self.browser.driver.window_handles) > 1:
                            break
                        if count >= 150 and retry > 0:
                            # 15秒経過して window_handles が 1つのとき再度クリック
                            print('[子ウインドウ]-------------------------------')
                            print('リトライしました' + str(count) + 'ミリ秒')
                            retry -= 1
                            count = 0
                            # サブウインドウを再度クリック
                            # self.browser.action_sub_window_click(value)
                            self.browser.item_click(xpath + '/a')
                        if count >= 300:
                            print('[子ウインドウ]-------------------------------')
                            print('タイムアウト:' + str(count) + 'ミリ秒')
                            break
                        # self.browser.time.sleep(0.1)
                        count += 1
                    all_handles = self.browser.driver.window_handles
                    self.browser.driver.switch_to_window(all_handles[1])
                    # サブウインドウの操作
                    # 条件分岐
                    # 90番環境は条件分岐がCoDe文キー
                    if self.browser.mode == 'dev4s' or self.browser.mode == '4s90':
                        self.browser.item_send_element_key_by_name('textarea', '条件式', 'syntax', steps[step]['条件分岐'])
                        # 保存する
                        if self.browser.driver.find_elements_by_xpath('//input[@type="button"][@value="保存する"]')[0].is_enabled():
                            self.browser.driver.find_elements_by_xpath('//input[@type="button"][@value="保存する"]')[1].click()
                    else:
                        self.browser.edit_question_condition_setting('条件分岐', page_question_number, page_question_type, none_end_quids, steps[step])
                        # 保存する
                        if self.browser.driver.find_elements_by_xpath('//input[@type="button"][@value="保存する"]')[0].is_enabled():
                            self.browser.driver.find_elements_by_xpath('//input[@type="button"][@value="保存する"]')[0].click()
                    # 親ウインドウへ戻る
                    self.browser.driver.switch_to_window(all_handles[0])
                    self.browser.time.sleep(0.5)
            # メッセージ編集
            if steps.get('メッセージ編集') is None:
                pass
            else:
                self.browser.sub_window_operation('メッセージ編集', steps['メッセージ編集'])
                print('[処理済み] メッセージ編集の処理が完了しました')
                print('d:', datetime.datetime.today())
            # ページ設定
            if steps.get('ページ設定') is None:
                pass
            else:
                self.browser.sub_window_operation('ページ設定', steps['ページ設定'])
                print('[処理済み] ページ設定の処理が完了しました')
                print('d:', datetime.datetime.today())
            print('[処理済み] すべての処理が完了しました')
            print('d:', datetime.datetime.today())

            # ブラウザ処理終了
            self.browser.browser_exit()
        except Exception as exc:
            print(exc)

    # アンケート画面編集に遷移した状態からリサーチを作成
    def edit_new_research_etc(self, open_file_name, reserch_no):
        try:
            # アンケート画面編集に切り替わらなければ実行中断（終了）
            if self.browser.check_browser_path('アンケート画面編集') == False:
                print('[エラー] 実行中断しました')
                print('d:', datetime.datetime.today())
                return False

            print("[作成開始]------------------------------- -> " + open_file_name + " / " + reserch_no)
            print('d:', datetime.datetime.today())
            with codecs.open(open_file_name, encoding='utf-8') as f:
                steps = json.load(f)

            self.browser.convert_new_forsurvey_to_old_forsurvey(steps)
            # マトリクス混合を分解するときページ番号とQナンバーの加工が必要で、先に設定済みQナンバーの最大値を取得しておく
            max_quid = '0000'
            for step in steps:
                if steps[step].get('Qナンバー') is None:
                    pass
                else:
                    quid = steps[step]['Qナンバー']
                    # print(quid)
                    if int(max_quid,10) < int(quid,10):
                        max_quid = quid
            # print('# 設定済み最大Qナンバー -> ' + max_quid)
            new_steps = {}
            new_steps_count = 0
            original_page_number = ''
            original_page_number_back = '' 
            new_page_number = ''
            for step in steps:
                if steps[step].get('Qナンバー') is None:
                    # Qナンバーが存在しないのは設問ではない
                    new_steps[str(new_steps_count)] = steps[step]
                    new_steps_count += 1
                else:
                    original_page_number = steps[step]['ページ番号']
                    # print('# 開始 [' + str(steps[step]['Qナンバー']) + ']--------------------')
                    new_split_steps = self.browser.convert_matrix_mix_split(max_quid, steps[step])
                    # print('# 分割数 -> ' + str(len(new_split_steps)))
                    # 初回のページは「P1」をセットする
                    if new_page_number == '':
                        new_page_number = 'P1'
                        original_page_number_back = ''
                    else:
                        if original_page_number_back == original_page_number:
                            # 同一ページのときページ番号を加算しない
                            pass
                        else:
                            # ページ番号を加算する
                            new_page_number = 'P' + str(int(new_page_number[1:],10) + 1)

                    # セットする前に back に変更前のページ番号をセット
                    original_page_number_back = original_page_number
                    # 新しいページ番号をセット
                    steps[step]['ページ番号'] = new_page_number

                    if new_split_steps == False:
                        # 90番forSurveyにしか存在しないキーを削除
                        self.browser.delete_new_forsurvey_setting_information(steps[step])
                        # 分割しない（MTX以外）設問の処理
                        new_steps[str(new_steps_count)] = steps[step]
                        new_steps_count += 1
                    else:
                        # print('# ページ番号 [' + str(steps[step]['ページ番号']) + ']--------------------')
                        # 分割された設問にページ番号を設定
                        for new_split_step in new_split_steps:
                            new_split_steps[new_split_step]['ページ番号'] = new_page_number
                            # ページ番号を加算する
                            new_page_number = 'P' + str(int(new_page_number[1:],10) + 1)
                            # new_steps[str(new_steps_count)] = new_split_steps

                            # 90番forSurveyにしか存在しないキーを削除
                            self.browser.delete_new_forsurvey_setting_information(new_split_steps[new_split_step])

                            new_steps[str(new_steps_count)] = new_split_steps[new_split_step]
                            new_steps_count += 1
            # print('# [生成結果] ----------------------------')
            # print(new_steps)


            steps = new_steps
            # return False

            # 作成するリサーチNoを検索して表示する
            self.browser.search_by_research_no(reserch_no)

            # リサーチが作成されていなければ中断
            if self.browser.get_number_of_displayed_project() == 0:
                print('[エラー] リサーチが存在しません。 -> ' + str(reserch_no))
                print('d:', datetime.datetime.today())
                return False

            # self.browser.time.sleep(3)
            # return False

            # 90番のみ、MYリサーチ一覧がアコーディオンになっている対応
            if self.browser.mode == 'dev4s' or self.browser.mode == '4s90':
                self.browser.research_accordion_open()

            self.browser.my_research_iconMenu_click('アンケート画面編集')

            # アンケート画面編集に切り替わらなければ実行中断（終了）
            if self.browser.check_browser_path('アンケート画面編集') == False:
                print('[エラー] 実行中断しました')
                print('d:', datetime.datetime.today())
                return False

            # 画面上の設問/終了ページをすべて削除
            self.browser.initialize_research_question()

            # 必要な設問を追加するためにQナンバーの最大値を取得し、quidsに格納
            max_quid = 0
            quids = []
            for step in steps:
                quid = steps[step].get('Qナンバー')
                if quid is None:
                    pass
                else:
                    if max_quid < int(quid):
                        max_quid = int(quid)
                    quids.append(quid)
            print('[処理済み] Qナンバー最大値の取得が完了しました')
            print('d:', datetime.datetime.today())

            # 設問一括追加 - 設問をQナンバー最大値分追加して存在しないQナンバーの設問を削除
            if max_quid > 1:
                # 最大追加が1回で99問対策
                while max_quid > 99:
                    # 設問一括追加
                    self.browser.sub_window_operation('設問一括追加', ['', '//select[@name="offset"]/option[@value="after"]', '//input[@name="num"]', 99, '//input[starts-with(@value,"追加する")]'])
                    max_quid -= 99
                    # Ajax読み込み待機
                    self.browser.ajax_loading_wait('//div[@class="loading"]/img')
                    # 存在しないQナンバー選択
                    xpath = '//input[@name="qu_id_check[]"]'
                    if self.browser.dom_loading_wait(xpath):
                        elements = self.browser.driver.find_elements_by_xpath(xpath)
                        for element in elements:
                            quid = element.get_attribute('value')
                            if quid in quids:
                                pass
                            else:
                                element.click()
                    # 最後のQナンバーを消すと設問追加でQナンバーの値が増加しないので最大Qナンバーが選択されてたら解除
                    element_max_quid = str(self.browser.get_my_research_max_q_number())
                    xpath = '//input[@name="qu_id_check[]"][@value="' + str(element_max_quid) + '"]'
                    if self.browser.dom_loading_wait(xpath):
                        if self.browser.driver.find_elements_by_xpath(xpath)[0].is_selected():
                            self.browser.item_click(xpath)
                    # 設問削除
                    self.browser.sub_window_operation('設問削除', ['//input[starts-with(@value,"削除する")]'])
                    # Ajax読み込み待機
                    self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            if max_quid > 1:
                self.browser.sub_window_operation('設問一括追加', ['', '//select[@name="offset"]/option[@value="after"]', '//input[@name="num"]', int(max_quid), '//input[starts-with(@value,"追加する")]'])
            # Ajax読み込み待機
            self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            print('[処理済み] 設問一括追加が完了しました')
            print('d:', datetime.datetime.today())
            # 存在しないQナンバー選択
            xpath = '//input[@name="qu_id_check[]"]'
            chk_count = 0
            if self.browser.dom_loading_wait(xpath):
                elements = self.browser.driver.find_elements_by_xpath(xpath)
                for element in elements:
                    quid = element.get_attribute('value')
                    if quid in quids:
                        pass
                    else:
                        element.click()
                        chk_count = chk_count + 1
            print('[処理済み] 存在しないQナンバーの選択が完了しました')
            print('d:', datetime.datetime.today())
            # 設問削除
            if chk_count > 0:
                self.browser.sub_window_operation('設問削除', ['//input[starts-with(@value,"削除する")]'])
                # Ajax読み込み待機
                self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            print('[処理済み] 不要な設問の削除が完了しました')
            print('d:', datetime.datetime.today())
            # Ajax読み込み待機
            self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            # 設問の順番を並び替える（順番は後ろから）
            quids = []
            for step in steps:
                quid = steps[step].get('Qナンバー')
                if quid is None:
                    pass
                else:
                    quids.append(quid)
            # quids.reverse()
            count = 0
            for quid in quids:
                if count == 0:
                    pass
                else:
                    # Ajax読み込み待機
                    self.browser.ajax_loading_wait('//div[@class="loading"]/img')
                    # 設問をクリック
                    xpath = '//input[@name="qu_id_check[]"][@value="' + str(quid) + '"]'
                    self.browser.item_click(xpath)
                    # 設問移動
                    self.browser.sub_window_operation('設問移動', ['//select[@name="base_qu_id"]/option[starts-with(@value, "' + str(prev_quid) + '")]', '', '//input[starts-with(@value,"移動する")]'])
                prev_quid = quid
                count += 1
            print('[処理済み] 設問の順番の並び替えが完了しました')
            print('d:', datetime.datetime.today())
            # Ajax読み込み待機
            self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            # 設問入力/設定の開始
            prev_page = ''
            # end_pages = []
            page_number = 0
            for step in steps:
                # ページ設定、メッセージ編集など「ページ番号」をもたない設定はスキップ
                if steps[step].get('ページ番号') is None:
                    pass
                else:
                    # ENDページは設問を作成した後に追加したいからスキップ
                    if steps[step]['ページ番号'].find('P') == 0:
                        page_number += 1
                        print('[設問作成][ ' + str(steps[step]['ページ番号']) + ' ]-------------------------------')
                        print('d:', datetime.datetime.today())
                        # 未設定の設問もスキップ対策
                        if steps[step]['設問タイプ'] == '':
                            pass
                        else:
                            self.browser.edit_new_question('P' + str(page_number), steps[step], prev_page=prev_page)
                    elif steps[step]['ページ番号'].find('START') >= 0 or steps[step]['ページ番号'].find('COMP') >= 0:
                        self.browser.edit_new_question(str(steps[step]['ページ番号']), steps[step], prev_page=prev_page)
                    # 作成が終わったページを1つ前のページ番号として保存
                    prev_page = str(steps[step]['ページ番号'])
            # 改ページ準備
            # 作成予定のページ番号を取得：START,COMP,END,GATEは含まない
            plan_pages = []
            for step in steps:
                array_value = steps[step].get('ページ番号')
                if array_value is None:
                    pass
                else:
                    if array_value.find('START') == -1 and array_value.find('COMP') == -1 and array_value.find('END') == -1 and array_value.find('GATE') == -1:
                        plan_pages.append(array_value)
            # 改ページボタンHTMLと紐づけ表を作成
            kaipage_quid = []
            xpath = '//td[@class="setting01"]/a'
            if self.browser.dom_loading_wait(xpath):
                elements = self.browser.driver.find_elements_by_xpath(xpath)
                for element in elements:
                    # 改ページボタンが表示されてるQナンバー
                    kaipage_quid.append(element.get_attribute('href')[22:26])
            page_numbers = []
            page_quids = []
            self.browser.get_my_research_page_number_only(page_quids, page_numbers)
            print('[処理済み] 改ページに必要なページ番号の取得が完了しました')
            print('d:', datetime.datetime.today())
            page_count = 0
            # 改ページの開始
            for plan_page in plan_pages:
                page_count += 1
                if page_count >= len(plan_pages):
                    pass
                else:
                    # ページと次のページが同じページ番号のとき、ページの改ページボタンを押す
                    if plan_page == plan_pages[page_count]:
                        xpath = '//td[@class="setting01"]/a'
                        if self.browser.dom_loading_wait(xpath):
                            elements = self.browser.driver.find_elements_by_xpath(xpath)
                            elements[kaipage_quid.index(page_quids[page_count-1])].click()
                            # Ajax読み込み待機
                            self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            print('[処理済み] 改ページが完了しました')
            print('d:', datetime.datetime.today())
            # ENDページ追加準備
            page_numbers = []
            page_quids = []
            page_pgids = []
            self.browser.get_my_research_page_number_all(page_numbers, page_quids, page_pgids)
            max_end_pgid = 0
            for step in steps:
                quid = steps[step].get('Qナンバー')
                if quid is None:
                    # ENDページの最大値を取得
                    end_pgid = steps[step].get('終了タイプ')
                    if end_pgid is None:
                        pass
                    else:
                        if end_pgid.find('END') >= 0:
                            end_pgid_number = end_pgid[3:len(end_pgid)]
                            if max_end_pgid < int(end_pgid_number):
                                max_end_pgid = int(end_pgid_number)
            # Qナンバーの後ろから2番目（COMPの前の設問）の後ろに一括でENDページ追加
            self.browser.sub_window_operation('途中終了追加', ['//select[@name="pg_id"]/option[@value="' + str(page_pgids[len(page_pgids) - 2]) + '"]', '//input[@name="num"]', max_end_pgid - 1, '//input[starts-with(@value,"追加する")]'])
            print('[処理済み] ENDページの一括追加が完了しました')
            print('d:', datetime.datetime.today())
            # Ajax読み込み待機
            self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            end_pages = []
            for step in steps:
                end_type = steps[step].get('終了タイプ')
                if end_type is None:
                    pass
                else:
                    if end_type.find('END') >= 0:
                        if end_type != 'END1':
                            end_pages.append(end_type)
            delete_end_pages = []
            for count in range(2, max_end_pgid + 1):
                if 'END' + str(count) in end_pages:
                    pass
                else:
                    delete_end_pages.append('END' + str(count))
            # 不要なENDページ一括削除
            if len(delete_end_pages) > 0:
                page_numbers = []
                page_quids = []
                page_pgids = []
                self.browser.get_my_research_page_number_all(page_numbers, page_quids, page_pgids)
                for page_value in delete_end_pages:
                    select_option_value = page_pgids[page_numbers.index(page_value)]
                    xpath = '//input[@name="pg_id_check[]"][@value="' + str(select_option_value) + '"]'
                    self.browser.item_click(xpath)
                # 設問削除 - クリックした設問を削除する
                self.browser.sub_window_operation('設問削除', ['//input[starts-with(@value,"削除する")]'])
                # Ajax読み込み待機
                self.browser.ajax_loading_wait('//div[@class="loading"]/img')
            print('[処理済み] ENDページの削除が完了しました')
            print('d:', datetime.datetime.today())
            page_numbers = []
            page_quids = []
            page_pgids = []
            self.browser.get_my_research_page_number_all(page_numbers, page_quids, page_pgids)
            page_numbers_unique = sorted(set(page_numbers), key=page_numbers.index)
            pages = []
            for step in steps:
                array_value = steps[step].get('ページ番号')
                if array_value is None:
                    pass
                else:
                    if array_value == 'GATE':
                        array_value = steps[step].get('終了タイプ')
                        if array_value is None:
                            pass
                        else:
                            pages.append(array_value)
                    else:
                        pages.append(array_value)
            # ついに！ENDページ移動
            for page in pages:
                if page.find('END') == -1:
                    pass
                # 移動対象ENDページ処理
                else:
                    xpath = '//input[@name="pg_id_check[]"][@value="' + str(page_pgids[page_numbers_unique.index(page)]) + '"]'
                    self.browser.item_click(xpath)
                    # 設問移動
                    self.browser.sub_window_operation('設問移動', ['//select[@name="base_pg_id"]/option[@value="' + str(page_pgids[page_numbers_unique.index(prev_page)]) + '"]', '', '//input[starts-with(@value,"移動する")]'])
                    # Ajax読み込み待機
                    self.browser.ajax_loading_wait('//div[@class="loading"]/img')
                # 1つ前のページ
                prev_page = page
            print('[処理済み] ENDページの移動が完了しました')
            print('d:', datetime.datetime.today())
            # 移動させたらENDを編集
            prev_page = ''
            for step in steps:
                # ページ設定、メッセージ編集など「ページ番号」をもたない設定はスキップ
                if steps[step].get('ページ番号') is None:
                    pass
                else:
                    # ENDページを編集
                    if steps[step]['ページ番号'].find('GATE') == 0 or steps[step]['ページ番号'].find('END') == 0:
                        self.browser.edit_new_question(steps[step]['終了タイプ'], steps[step])
            # 条件分岐
            for step in steps:
                # 条件分岐をもたない設定はスキップ
                if steps[step].get('条件分岐') is None:
                    pass
                else:
                    page_numbers = []
                    page_quids = []
                    page_pgids = []
                    self.browser.get_my_research_page_number_all(page_numbers, page_quids, page_pgids)
                    page_question_number = []
                    page_question_type = []
                    none_end_quids = []
                    self.browser.get_my_research_page_question_number_and_type(page_question_number, page_question_type, none_end_quids)
                    # page_numbersの重複を削除
                    page_numbers_unique = sorted(set(page_numbers), key=page_numbers.index)
                    # GATEは条件分岐が存在しないから page_pgids を取得できない。キーを削除。
                    # print('Error')
                    # print(page_numbers_unique.index('GATE'))
                    for page_numbers_gate in page_numbers_unique:
                        if page_numbers_gate == 'GATE':
                             page_numbers_unique.remove('GATE')
                    # print(page_numbers)
                    # print(page_quids)
                    # print(page_pgids)
                    # print(page_numbers_unique)
                    # print(page_question_type)
                    # print(page_question_number)
                    # print(none_end_quids)
                    # if page_numbers_unique.index('GATE'):
                    #     pass
                    # else:
                    #     page_numbers_unique.remove('GATE')
                    # print(page_numbers_unique)
                    # print(page_pgids)
                    # print(page_numbers_unique.index(steps[step]['ページ番号']))
                    # 頁Noから条件分岐のボタンのJavaScriptの引数を取得
                    page_index = page_pgids[page_numbers_unique.index(steps[step]['ページ番号'])]
                    # print(page_index)
                    javascript_code = "javascript:openEditConditionConfirmWindow('" + str(page_index) + "');"
                    # 条件分岐を編集
                    xpath = '//a[@href="' + javascript_code + '"]'
                    # サブウインドウをクリック
                    self.browser.item_click(xpath)
                    # 子ウインドウが表示されるまで待って切り替える
                    count = 0
                    retry = 1
                    while True:
                        if len(self.browser.driver.window_handles) > 1:
                            break
                        if count >= 150 and retry > 0:
                            # 15秒経過して window_handles が 1つのとき再度クリック
                            print('[子ウインドウ]-------------------------------')
                            print('リトライしました' + str(count) + 'ミリ秒')
                            retry -= 1
                            count = 0
                            # サブウインドウを再度クリック
                            # self.browser.action_sub_window_click(value)
                            self.browser.item_click(xpath + '/a')
                        if count >= 300:
                            print('[子ウインドウ]-------------------------------')
                            print('タイムアウト:' + str(count) + 'ミリ秒')
                            break
                        # self.browser.time.sleep(0.1)
                        count += 1
                    all_handles = self.browser.driver.window_handles
                    self.browser.driver.switch_to_window(all_handles[1])
                    # サブウインドウの操作
                    # 条件分岐
                    # 90番環境は条件分岐がCoDe文キー
                    if self.browser.mode == 'dev4s' or self.browser.mode == '4s90':
                        # body[page_count]['条件分岐']['条件式'] = self.browser.get_item_text('//textarea[@name="syntax"]')
                        self.browser.item_send_element_key_by_name('textarea', '条件式', 'syntax', steps[step]['条件分岐'])
                        # 保存する
                        if self.browser.driver.find_elements_by_xpath('//input[@type="button"][@value="保存する"]')[0].is_enabled():
                            self.browser.driver.find_elements_by_xpath('//input[@type="button"][@value="保存する"]')[1].click()
                    else:
                        self.browser.edit_question_condition_setting('条件分岐', page_question_number, page_question_type, none_end_quids, steps[step])
                        # 保存する
                        if self.browser.driver.find_elements_by_xpath('//input[@type="button"][@value="保存する"]')[0].is_enabled():
                            self.browser.driver.find_elements_by_xpath('//input[@type="button"][@value="保存する"]')[0].click()
                    # 親ウインドウへ戻る
                    self.browser.driver.switch_to_window(all_handles[0])
                    self.browser.time.sleep(0.5)
            # メッセージ編集
            if steps.get('メッセージ編集') is None:
                pass
            else:
                self.browser.sub_window_operation('メッセージ編集', steps['メッセージ編集'])
                print('[処理済み] メッセージ編集の処理が完了しました')
                print('d:', datetime.datetime.today())
            # ページ設定
            if steps.get('ページ設定') is None:
                pass
            else:
                self.browser.sub_window_operation('ページ設定', steps['ページ設定'])
                print('[処理済み] ページ設定の処理が完了しました')
                print('d:', datetime.datetime.today())
            print('[処理済み] すべての処理が完了しました')
            print('d:', datetime.datetime.today())

            # ブラウザ処理終了
            self.browser.browser_exit()
        except Exception as exc:
            print(exc)
