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

        # 1. ログイン画面に遷移
        self.selenium.get(self.live_server_url + '/admin/')
        self.wait_page_loaded()

        # 2. システム管理者でログイン
        self.admin_login(self.superuser.username, 'pass12345')
        self.assert_title('サイト管理')
        # ホーム画面でスクリーンショットを撮る（1枚目）
        self.selenium.save_screenshot(f'{self.id()}-1.png')

        # 3. ホーム画面で「本」リンクを押下
        self.selenium.find_element_by_link_text('本').click()
        self.wait_page_loaded()
        self.assert_title('変更する 本 を選択')
        # モデル一覧画面でスクリーンショットを撮る（2枚目）
        self.selenium.save_screenshot(f'{self.id()}-2.png')

        # (以下略)
