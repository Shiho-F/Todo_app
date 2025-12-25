from django.urls import path

from todos.views import (
    TodoListView,
    TodoDetailView,
    TodoCreateView,
    SignUpView,
    MyLoginView,
)

urlpatterns = [
    # サインアップ
    path("signup/", SignUpView.as_view(), name="signup"),
    # ログイン
    path("login/", MyLoginView.as_view(), name="login"),
    # タスク一覧
    path("", TodoListView.as_view(), name="todo_list"),
    # ここでの"""は/todos/の続きが何もない状態を表している
    # つまり/todos/ + "" = /todos/
    # タスク作成
    path("create/", TodoCreateView.as_view(), name="todo_create"),
    # タスク詳細
    path("<int:pk>/detail/", TodoDetailView.as_view(), name="todo_detail"),
]
