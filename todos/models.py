from django.db import models

from django.conf import settings
# このプロジェクトのsetting.pyの内容を参照している

# Create your models here.


# タスクテーブル(Todos)の定義
class Todo(models.Model):
    # Todos　→ テーブル名
    # (models.Model) → このクラスはDjangoのモデルですよ。と宣言している

    # ユーザーID（FK）
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="todos",
        verbose_name="ユーザー",
    )

    # タイトルカラム
    title = models.CharField(max_length=100, verbose_name="タイトル")
    # title → カラム名
    # models.charField → 文字列用のフィールド
    # models.CharField(max_length=100) → SQLでいうVARCHAR(100)を表している
    # verbose_name="文字列"を入れることで　管理画面・フォーム・エラーメッセージで表示されるラベル名を決めている

    # 詳細カラム
    description = models.TextField(blank=True, null=True, verbose_name="詳細")
    # TextField　→　TEXT型
    # (blank=True, null=True) → 詳細未設定(NULL)を許可

    # 締切日カラム
    due_date = models.DateField(blank=True, null=True, verbose_name="締切日")
    # DateField → DATE型

    # 完了/未完了フラグ
    is_completed = models.BooleanField(default=False, verbose_name="完了")
    # BooleanField → TINYINT(1):意味は真偽値
    # 0 = 未完了/1 = 完了
    # (default=False)　→ 値を指定しなかった場合デフォルトで0(未完了)になる

    # 作成日時カラム
    created_at = models.DateTimeField(auto_now_add=True)
    # DateTimeField　→ TIMESTAMP型で意味は一致している
    # ER図ではDB実装を意識してTIMESTAMPを採用しているがDjango側ではフレームワーク標準のDateTimeFieldに任せている
    # (auto_now_add=True)　→　タスク作成時に現在時刻を自動で1回だけ設定してくれる

    # 更新日時カラム
    updated_at = models.DateTimeField(auto_now=True)
    # (auto_now=True) → 保存されるたびに、現在時刻で自動更新される

    def __str__(self):
        # __str__ → 文字列としてオブジェクト名を表示させる時に使用するPythonメソッド
        # (管理画面・フォーム・print()など)
        # selfは１件のタスク（Todo）自身
        return self.title
        # self.title　→ そのTodoのタイトル


# タグテーブル(Tags)の定義
class Tag(models.Model):
    # ユーザーID(FK)
    user = models.ForeignKey(
        # user = models.ForeignKey(...) → このタグは誰のものか？を決めている
        settings.AUTH_USER_MODEL,
        # settings.pyで指定されているユーザーモデル(現状はDjango標準)をこのプロジェクトで使用
        on_delete=models.CASCADE,
        # on_delete → 削除された時のルール
        # CASCADE → 親(User)が消えたら子(Tag)も消すという意味
        related_name="tags",
        # UserからTagを取得するための名前
        # user.tags.all()でこのユーザーのタグ一覧を取得できる
        verbose_name="ユーザー",
    )
    # タグの名前カラム
    name = models.CharField(max_length=50, verbose_name="タグ名")

    # 作成日時カラム
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新日時カラム
    updated_at = models.DateTimeField(auto_now=True)
