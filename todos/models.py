from django.db import models

# Create your models here.


# タスクテーブル(Todos)の定義
class Todos(models.Model):
    # Todos　→ テーブル名
    # (models.Model) → このクラスはDjangoのモデルですよ。と宣言している
    title = models.CharField(max_length=100, verbose_name="タイトル")
    # title → カラム名
    # models.charField → 文字列用のフィールド
    # models.CharField(max_length=100) → SQLでいうVARCHAR(100)を表している
    # verbose_name="文字列"を入れることで　管理画面・フォーム・エラーメッセージで表示されるラベル名を決めている
    description = models.TextField(blank=True, null=True, verbose_name="詳細")
    # TextField　→　TEXT型
    # (blank=True, null=True) → 詳細未設定(NULL)を許可
    due_date = models.DateField(blank=True, null=True, verbose_name="締切日")
    # DateField → DATE型
    is_completed = models.BooleanField(default=False, verbose_name="完了")
    # BooleanField → TINYINT(1):意味は真偽値
    # 0 = 未完了/1 = 完了
    # (default=False)　→ 値を指定しなかった場合デフォルトで0(未完了)になる
    created_at = models.DateTimeField(auto_now_add=True)
    # DateTimeField　→ TIMESTAMP型で意味は一致している
    # ER図ではDB実装を意識してTIMESTAMPを採用しているがDjango側ではフレームワーク標準のDateTimeFieldに任せている
    # (auto_now_add=True)　→　タスク作成時に現在時刻を自動で1回だけ設定してくれる
    updated_at = models.DateTimeField(auto_now=True)
    # (auto_now=True) → 保存されるたびに、現在時刻で自動更新される

    def __str__(self):
        # __str__ → 文字列としてオブジェクト名を表示させる時に使用するPythonメソッド
        # (管理画面・フォーム・print()など)
        # selfは１件のタスク（Todo）自身
        return self.title
        # self.title　→ そのTodoのタイトル


# ここから学習のためにSQLに変換(理解用)
# ER図ベースSQL

# 🔽タスク(todos)テーブルを作成
# CREATE TABLE todos (id BIGINT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id),
# ER図では論理設計としてINTを使用していたが、Djangoの実装では主キーにBigAutoFieldが使用されるため
# 物理設計としても、ここではBIGINTに合わせている

#     🔽タイトルカラム
#     title VARCHAR(100) NOT NULL,

#     🔽タスクの詳細カラム
#     description TEXT NULL,

#     🔽期限(締切日)カラム作成
#     due_date DATE NULL,

#     🔽完了/未完了フラグ
#     is_completed TINYINT(1) NOT NULL DEFAULT 0,

#     🔽作成日時カラム
#     created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     DEFAULT → 値が渡されなかった時の初期値
#     CURRENT_TIMESTAMP → 今この瞬間の日時
#     この2つを組み合わせるとINSERT文でcreated_atを指定しなかった場合に自動で今の時刻を入れてくれる

#     🔽更新日時カラム
#     updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
# );
#     ON UPDATE CURRENT_TIMESTAMP → DBが自動でupdated_atを今の時刻に変更

#     ※created_atの内部的な動き
#     INSERT INTO todos (title) VALUES ('買い物');
#     created_atを指定していないので、テーブル定義のDEFAULT　CURRENT_TIMESTAMPが適用されDBが自動的に現在時刻をcreated_atに設定する
#     ※ updated_atの内部的な動き
#     UPDATE todos SET title = '買い物と大掃除', updated_at = CURRENT_TIMESTAMP WHERE id = 1;
#     idが1のタスクについてタイトルを変更し、ON UPDATE CURRENT_TIMESTAMPにより
#     DBが自動的に更新日時を現在時刻に設定する

# ・論理設計：どんなデータを、どんな関係で持つかを考える段階
# ・物理設計：それをDBにどう作るかを決める段階
