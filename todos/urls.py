from django.urls import path

from todos.views import TodoListView, TodoDetailView, TodoCreateView

urlpatterns = [
    path("", TodoListView.as_view(), name="todo_list"),
    # ここでの"""は/todos/の続きが何もない状態を表している
    # つまり/todos/ + "" = /todos/
    path("create/", TodoCreateView.as_view(), name="todo_create"),
    path("<int:pk>/detail/", TodoDetailView.as_view(), name="todo_detail"),
]
