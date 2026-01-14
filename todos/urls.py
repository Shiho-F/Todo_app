from django.urls import path

from todos.views import (
    TodoListView,
    TodoDetailView,
    TodoCreateView,
    SignUpView,
    MyLoginView,
    MyLogoutView,
    TagCreateView,
    TodoToggleCompleteView,
)

urlpatterns = [
    # サインアップ
    path("signup/", SignUpView.as_view(), name="signup"),
    # ログイン
    path("login/", MyLoginView.as_view(), name="login"),
    # ログアウト
    path("logout/", MyLogoutView.as_view(), name="logout"),
    # タスク一覧
    path("", TodoListView.as_view(), name="todo_list"),
    # ここでの"""は/todos/の続きが何もない状態を表している
    # つまり/todos/ + "" = /todos/
    # タスク作成
    path("create/", TodoCreateView.as_view(), name="todo_create"),
    # タスク詳細
    path("<int:pk>/detail/", TodoDetailView.as_view(), name="todo_detail"),
    # タスク詳細フラグ切り替え用(完了/未完了)
    path(
        "<int:pk>/detail/toggle/",
        TodoToggleCompleteView.as_view(),
        name="todo_toggle_complete",
    ),
    # タグ作成
    path("tags/create/", TagCreateView.as_view(), name="tag_create"),
]
