from django.views.generic import ListView, DetailView, CreateView

# ListView:一覧表示
# DetailView：詳細表示
# CreateView:タスクを作成
from django.contrib.auth.views import LoginView, LogoutView

# loginView:ログイン処理を全部やってくれるDjango標準のView
from django.views import View
# ViewはDjangoが用意している一番基本のViewクラス
# 自分でGET/POSTを自分で書くときの土台(自分で処理を書く用)

from django.urls import reverse_lazy

from todos.models import Todo, Tag

from .forms import CustomUserCreationForm, LoginForm, TodoForm

from django.contrib.auth.mixins import LoginRequiredMixin
# LoginRequiredMixin：ログインしているユーザーだけにアクセスを許可するView

from django.shortcuts import get_object_or_404, redirect


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


# ログアウトビュー
class MyLogoutView(LogoutView):
    next_page = "login"
    # ログアウトが終わった後に、どこに移動するかを指定している


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

    def get_queryset(self):
        # ListViewが表示するデータ一覧(QuerySet)を決めるメソッド

        # タグ一覧表示
        queryset = Todo.objects.filter(user=self.request.user)
        # Todo.objects:Todoテーブルから
        # .filter(...):条件に合うものだけを取り出す
        # user=self.request.user:ログイン中のユーザーのTodoだけ

        # ここからTodoに紐づいているタグの絞り込み(中身を絞る)
        tag_ids = self.request.GET.getlist("tag")
        # URLのクエリパラメータから選ばれたタグIDを全部取り出す
        if tag_ids:
            # タグが一つでも選ばれていたら実行
            # tag_idsが空リスト[]ならfalse → タグ未選択なら全件表示される
            # ["1", "3"]みたいに入っていたらtrue → 選択されたタグのタスクのみ表示
            queryset = queryset.filter(tags__id__in=tag_ids).distinct()
            # queryset.filter(...):ログインしてるユーザーのTodo一覧の中から
            # tags:Todoの紐づくタグ(ManyToMany)
            # Djangoの__(ダブルアンダースコア)は「〜の中の」という意味
            # tags__idでこのTodoに紐づくTagのidを見ている
            # __inはDjangoの検索ルールで、このリストの中に含まれているか？という意味
            # つまりtags__id__in=tag_idsはTodoに紐づくタグの中に、IDがtag_idsのどれかに一致するタグを持つTodo
            # .distinct():重複を消す
        return queryset
        # 最後にListViewにこれ表示してねって返している
        # 返したquerysetがテンプレの{% for todo in todos %}のもとになる

    # ここから画面にタグ一覧と選択状態を渡す(UIを成立させている)
    def get_context_data(self, **kwargs):
        # get_context_data:ListViewがテンプレートに渡すcontextを拡張するためのメソッド
        # **kwargs：名前付きで渡された引数を、全部まとめて受け取る
        # Djangoが渡してくる追加データだけを受け取りたいから、ここでは*args(位置引数)は使用されない
        context = super().get_context_data(**kwargs)
        # 親クラス(ListView)が用意したcontextをそのまま受け取る
        # contextはテンプレに渡すためにViewが用意した全部入りセット
        # クエリ由来やDB由来のものがある
        context["all_tags"] = Tag.objects.filter(user=self.request.user)
        # ここではDBからall_tagsを取ってきている(View内部の処理)
        # context["all_tags"]で今ログインしているユーザーのタグ一覧を取得
        context["selected_tag_ids"] = self.request.GET.getlist("tag")
        # ここではURLのクエリパラメーター(GET)からタグのIDの一覧(tag_ids)取ってきている
        # context["selected_tag_ids"]でユーザーが選択したタグのID一覧を取得している
        # タグで絞り込みを行った時ににUIで再描写した時に選んだタグをチェック状態で残す
        # これがないと再描写した時にチェックが外れてしまう
        return context


# タスクの詳細画面ビュー
class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = "todos/todo_detail.html"
    context_object_name = "todo"
    # ここでは1件のタスクを取り扱うので単数形

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    # LoginRequiredMixin=ログインしているかを判断している
    # get_queryset/filter(user=...)=ログインユーザーののデータかを判断している
    # この二つが揃って初めてセキュリティが安全になる


# タスクの詳細画面フラグ切り替え用ビュー(完了/未完了)
class TodoToggleCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # POSTリクエストが来た時だけ動くメソッド
        # request:今来たリクエスト情報(ログインユーザー、GET/POSTデータが入っている)
        # pk：URLから渡されるTodoのID
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
        # Todo1件取りに行く
        # pk=pk:このIDのTodoを探す
        # user=request.user：ログイン中のユーザーのTodoだけに限定
        # 見つからなければ４０４(存在しない扱い)を返す
        todo.is_completed = not todo.is_completed
        # is_completed(完了フラグ)を反転させる
        # クリックするたびに完了/未完了が切り替わる(トグル)
        todo.save()
        # DBに保存
        return redirect("todo_detail", pk=pk)
        # redirect("todo_detail", pk=pk):
        # urls.pyのname="todo_detail"を探して
        # そのURLにpkを埋めて移動するという意味


# タスクの作成ビュー
class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = "todos/todo_form.html"
    # 後で編集機能の追加もできるようにtodo_form.htmlにしている
    form_class = TodoForm
    success_url = reverse_lazy("todo_list")
    # success_url：作成成功後　はTodo一覧画面へリダイレクト

    # ここからTodoFormにログインユーザーを渡している
    def get_form_kwargs(self):
        # get_form_kwargs：CreateViewがフォームを作る時に渡す引数をカスタマイズするメソッド
        kwargs = super().get_form_kwargs()
        # 親クラス(CreateView)が用意した標準のフォーム引数一式を取得している
        # kwargsはキーワド引数の辞書
        kwargs["user"] = self.request.user
        # ここで "user"というキーでself.request.user(ログインユーザー)を入れる
        return kwargs
        # このkwargsをTodoFormに返している

    # 146行目と意味同じ
    # Modelのデータ確定・保存処理
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# タグ作成ビュー
class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    template_name = "todos/tag_form.html"
    fields = ["name"]
    success_url = reverse_lazy("todo_list")

    def form_valid(self, form):
        # フォームの入力が正しかった時に呼ばれるメソッドを定義している
        # CreateViewにはもともとform_valid()というメソッドがある
        # form_valid()は保存と画面遷移をまとめてやってくれるメソッド
        # formは送信されたフォームのデータを持っている箱
        form.instance.user = self.request.user
        # form.instance:まだDBに保存されていないTagオブジェクト
        # 例：Tag(name="仕事") userはまだNone
        # .user = self.request.user:userフィールドにログインユーザーを代入している
        # 例：Tag(name="仕事", user=<User:shiho>)
        # ここまではまだ保存前の下書き(DB未保存)
        return super().form_valid(form)
        # super()=CreateView(親クラス)のメソッドを呼び出している
        # form_valid(form)：ここでDBに保存処理と
        # success_urlにリダイレクトしている(ここではタグ一覧画面)
