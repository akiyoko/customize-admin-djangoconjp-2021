# chromedriver_binaryをimportすることでChromeDriverのパスを通してくれる
import chromedriver_binary
from django.contrib.admin.tests import AdminSeleniumTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver

User = get_user_model()


class TestAdminSenario(AdminSeleniumTestCase):
    """管理サイトのシナリオテスト（システム管理者の場合）"""

    available_apps = None
    browser = 'chrome'

    @classmethod
    def create_webdriver(cls):
        """Chrome用のWebDriverインスタンスを作成する"""
        chrome_options = webdriver.ChromeOptions()
        # ヘッドレスモード
        chrome_options.add_argument('--headless')
        return webdriver.Chrome(chrome_options=chrome_options)

    def setUp(self):
        super().setUp()
        # テストユーザー（システム管理者）を作成
        self.superuser = User.objects.create_superuser('admin', 'admin@example.com', 'pass12345')

    def assert_title(self, text):
        """タイトルを検証する"""
        self.assertEqual(self.selenium.title.split(' | ')[0], text)

    def test_book_crud(self):
        """BookモデルのCRUD検証（システム管理者の場合）"""

        # 1. システム管理者でログイン
        self.admin_login(self.superuser.username, 'pass12345')
        self.assert_title('サイト管理')
        # ホーム画面でスクリーンショットを撮る（1枚目）
        self.selenium.save_screenshot(f'{self.id()}-1.png')

        # 2. ホーム画面で「本」リンクを押下
        self.selenium.find_element_by_link_text('本').click()
        self.wait_page_loaded()
        # モデル一覧画面が表示されていることを確認
        self.assert_title('変更する 本 を選択')
        # モデル一覧画面でスクリーンショットを撮る（2枚目）
        self.selenium.save_screenshot(f'{self.id()}-2.png')

        # 3. モデル一覧画面で「本 を追加」ボタンを押下
        self.selenium.find_element_by_link_text('本 を追加').click()
        self.wait_page_loaded()
        # モデル追加画面が表示されていることを確認
        self.assert_title('本 を追加')

        # 4. モデル追加画面で項目を入力して「保存」ボタンを押下
        self.selenium.find_element_by_name('title').send_keys('Book 1')
        self.selenium.find_element_by_name('price').send_keys('1000')
        self.selenium.find_element_by_name('publish_date').send_keys('2021-07-03')
        # モデル追加画面でスクリーンショットを撮る（3枚目）
        self.selenium.save_screenshot(f'{self.id()}-3.png')
        self.selenium.find_element_by_xpath('//input[@value="{}"]'.format('保存')).click()
        self.wait_page_loaded()
        # モデル一覧画面が表示されていることを確認
        self.assert_title('変更する 本 を選択')
        # モデル一覧画面でスクリーンショットを撮る（4枚目）
        self.selenium.save_screenshot(f'{self.id()}-4.png')

        # (以下略)
