import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from .lxml_helpers import ChangeListPage
from ..models import Book

User = get_user_model()


class TestAdminBookChangeList(TestCase):
    """管理サイトの Book モデル一覧画面のユニットテスト（システム管理者の場合）"""

    def setUp(self):
        # テストユーザー（システム管理者）を作成
        self.superuser = User.objects.create_superuser('admin', 'admin@example.com', 'pass12345')
        # Bookモデルのテストレコードを作成
        self.book = Book.objects.create(title='Book 1', price=1000, publish_date=datetime.date(2021, 7, 3))

    def test_page_items_for_result_list(self):
        # 管理サイトにログイン
        self.client.login(username=self.superuser.username, password='pass12345')
        # モデル一覧画面に遷移するためのリクエストを実行
        response = self.client.get('/admin/shop/book/')
        self.assertEqual(response.status_code, 200)
        # 画面項目を検証
        page = ChangeListPage(response.rendered_content)
        # 検索結果テーブル
        self.assertEqual(page.result_list_header_texts, ['ID', 'タイトル', '価格', 'サイズ', '出版日'])
        self.assertEqual(len(page.result_list_rows_texts), 1)
        self.assertEqual(page.result_list_rows_texts[0], ['Book 1', '1000', '-', '2021年7月3日'])
