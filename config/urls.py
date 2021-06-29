from django.contrib import admin
from django.urls import path


# def has_permission(request):
#     return request.user.is_active
#
#
# admin.site.site_header = 'システム管理者用サイト'
# admin.site.site_title = 'マイプロジェクト'
# admin.site.index_title = 'ホーム'
# admin.site.site_url = None
# admin.site.has_permission = has_permission

urlpatterns = [
    path('admin/', admin.site.urls),

]
