from django.contrib import admin
from django.utils import timezone

from .forms import BookAdminForm
from .models import Author, Book, BookStock, Publisher


class BookStockInline(admin.TabularInline):
    # OneToOneField を持っているモデルもインラインOK
    model = BookStock


class BookAdmin(admin.ModelAdmin):
    # class Media:
    #     css = {
    #         'all': (
    #             'admin/css/changelists_book.css',
    #         )
    #     }

    ###############################
    # モデル一覧画面のカスタマイズ
    ###############################
    # 画面表示フィールド
    list_display = ('id', 'title', 'price', 'size', 'publish_date')

    # @admin.display(
    #     description='価格',
    #     ordering='price',
    # )
    # def format_price(self, obj):
    #     """価格フィールドのフォーマットを変更する"""
    #     if obj.price is not None:
    #         return f'{obj.price:,d} 円'

    # 簡易検索
    search_fields = ('title', 'publisher__name', 'authors__name')

    # 絞り込み（フィルタ）
    list_filter = ('size', 'price', 'publish_date')

    # ページネーション
    list_per_page = 10

    # アクション一覧
    actions = ['publish_today']

    @admin.action(
        description='出版日を今日に更新',
        permissions=('change',),
    )
    def publish_today(self, request, queryset):
        """選択されたレコードの出版日を今日に更新する"""
        queryset.update(publish_date=timezone.localdate())

    ###############################
    # モデル追加・変更画面のカスタマイズ
    ###############################
    # フォーム
    form = BookAdminForm

    # インライン表示
    inlines = [BookStockInline]


admin.site.register(Book, BookAdmin)
# admin.site.register(Book)
admin.site.register(Author)
# admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Publisher)
