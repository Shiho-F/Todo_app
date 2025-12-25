from django.views.generic import ListView, DetailView, CreateView

# ListView:一覧表示
# DetailView：詳細表示
# CreateView:タスクを作成
from django.contrib.auth.views import LoginView
# loginView:ログイン処理を全部やってくれるDjango標準のView

from django.urls import reverse_lazy

from todos.models import Todo

from .forms import CustomUserCreationForm, LoginForm

from django.contrib.auth.mixins import LoginRequiredMixin
# LoginRequiredMixin：ログインしているユーザーだけにアクセスを許可するView


# サインアップビュー
class SignUpView(CreateView):
    template_name = "todos/signup.html"
    form_class = CustomUserCreationForm
    # forms.pyで定義したCustomCreationFormを参照している
    success_url = reverse_lazy("login")


# ログインビュー
class MyLoginView(LoginView):
    template_name = "todos/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True
    # すでにログインしてる人が/login/に来たらTodo一覧に飛ばす


# タスク一覧画面ビュー
class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = "todos/todo_list.html"
    # template_nameは書かなくても自動推測してくれるが、明示するために書く。
    # 書かないとファイル名を変えた瞬間に壊れる
    context_object_name = "todos"
    # ListViewがテンプレートに渡すtodoの一覧データの変数名を
    # デフォルトのobject_listからtodosに変更している
    # テンプレート側の可読性とViewごとの責務を明確にするために指定している


# タスクの詳細画面ビュー
class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = "todos/todo_detail.html"
    context_object_name = "todo"
    # ここでは1件のタスクを取り扱うので単数形


# タスクの作成ビュー
class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = "todos/todo_form.html"
    # 後で編集機能の追加もできるようにtodo_form.htmlにしている
    fields = ["title", "description", "due_date"]
    # モデルの指定したフィールドから自動でフォームを作る
    # ユーザーが操作可能なフィールドのみを明示的に指定している
    success_url = reverse_lazy("todo_list")
    # success_url：作成成功後　はTodo一覧画面へリダイレクト
