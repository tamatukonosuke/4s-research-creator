# 4s-research-creator
forSurveyの画面作成を自動でおこないます。

## 環境構築
このプログラムは以下の環境で構築して動作確認しています。

* Windows10 Pro (64-bit)
* Python 3.7.1(32-bit)

## Pythonのライブラリ

* pip (10.0.1)
* pit (0.3)
* Selenium (3.141.0)
* xlrd (1.2.0)
* xlwt (1.3.0)

## サンプルプログラム
```
from forsurvey_operation import forSurveyOperation

# クラス生成
browser = forSurveyOperation('アクセスしたいforSurveyの識別子')

# 通常モード（ブラウザ起動）でログインして設定情報を取得 
browser.get_forsurvey_setting_by_browser_mode('取得したいリサーチのグループ名', '取得したいリサーチNo')

# 通常モード（ブラウザ起動）でログインしてリサーチ作成
browser.edit_forsurvey_by_browser_mode('設定情報ファイル名', '作成先のグループ名', '作成先のリサーチNo')
```

## 説明
#### forSurvey_class.py
自動操作の中心となるプログラム。機能ごとの操作をあつめたプログラム。

#### forSurvey_operation.py
リサーチ設定情報の取得や、新規作成など一連の手順（操作）をまとめたプログラム。
forSurveyの操作を自動化したいとき、このファイルを参考にして作成します。