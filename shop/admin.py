import csv

from django.contrib import admin
from django.http.response import HttpResponse
from django.utils import timezone

from .forms import BookAdminForm, PublisherAdminForm
from .models import Author, Book, Publisher


class BookInline(admin.TabularInline):
    # ForeignKey を持っている側（多側）のモデルをインラインにする
    model = Book
    fields = ('title', 'price')
    extra = 1


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
    list_display = ('id', 'title', 'format_price', 'size', 'publish_date')

    @admin.display(
        description='価格',
        ordering='price',
    )
    def format_price(self, obj):
        """価格フィールドのフォーマットを変更する"""
        if obj.price is not None:
            return '{:,d} 円'.format(obj.price)

    # 初期表示時のソート
    ordering = ('id',)

    # 簡易検索
    search_fields = ('title', 'price', 'publisher__name', 'authors__name')

    # 絞り込み（フィルタ）
    list_filter = ('size', 'price', 'publish_date', 'publisher', 'authors')

    # ページネーション
    list_per_page = 10
    list_max_show_all = 1000

    # アクション一覧
    # resource_class = BookResource
    actions = ['download_as_csv', 'publish_today']

    def download_as_csv(self, request, queryset):
        """選択されたレコードのCSVダウンロードをおこなう"""
        meta = self.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        field_names = [field.name for field in meta.fields]
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    download_as_csv.short_description = 'CSVダウンロード'

    def publish_today(self, request, queryset):
        """選択されたレコードの出版日を今日に更新する"""
        queryset.update(publish_date=timezone.localdate())

    publish_today.short_description = '出版日を今日に更新'
    publish_today.allowed_permissions = ('change',)

    ###############################
    # モデル追加・変更画面のカスタマイズ
    ###############################
    # 画面表示フィールド
    # fields = (
    #     'id', 'title', 'price', 'size', 'publish_date', 'created_by', 'created_at',
    # )
    # exclude = ('publisher',)
    # readonly_fields = ('id', 'created_by', 'created_at')
    # autocomplete_fields = ('publisher',)
    # radio_fields = {'size': admin.HORIZONTAL}
    # prepopulated_fields = {'description': ('title', 'publish_date', )}
    # formfield_overrides = {
    #     models.CharField: {'widget': TextInput(attrs={'size': '80'})},
    #     models.TextField: {
    #         'widget': Textarea(attrs={'cols': '80', 'rows': '20'}),
    #     }
    # }

    # フォーム
    form = BookAdminForm

    # インライン表示
    # inlines = [
    #     BookStockInline,
    # ]

    ###############################
    # その他のカスタマイズ
    ###############################
    def save_model(self, request, obj, form, change):
        """モデル保存前に処理を追加する"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class PublisherAdmin(admin.ModelAdmin):
    # class Media:
    #     css = {
    #         'all': (
    #             '//code.jquery.com/ui/1.12.0/themes/smoothness/jquery-ui.css',
    #         )
    #     }
    #     js = (
    #         '//code.jquery.com/ui/1.12.1/jquery-ui.min.js',
    #         'admin/js/postal_code.js',
    #     )

    ###############################
    # モデル一覧画面のカスタマイズ
    ###############################
    search_fields = ('name',)

    ###############################
    # モデル追加・変更画面のカスタマイズ
    ###############################
    # fields = ('name', 'phone_number')
    form = PublisherAdminForm
    inlines = [
        BookInline,
    ]


# admin.site.register(Book, BookAdmin)
admin.site.register(Book)
admin.site.register(Author)
# admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Publisher)
