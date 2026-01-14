from django import forms

# フォームのフィールド、widget・バリデーションを定義するために使用する
from django.contrib.auth.models import User

from todos.models import Todo, Tag

# Django標準ユーザーモデルをインポート
# DjangoはUserモデルを参照する場合はget_user_modelを推奨しているが(将来Userを拡張できるようにするため)
# 今回は標準Userを使用するため、Userを直接参照している
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# UserCreationForm：パスワード付きユーザー作成を安全にやってくれるDjango標準フォーム
# ①パスワード入力欄を用意②パスワード一致チェック③パスワードのバリデーション④パスワードをハッシュ化して保存
# これを自動でやってくれる
# ハッシュ化　= 元のパスワードを元に戻せない形に変換すること
# AuthenticationForm = Django標準のログインフォーム
# フィールドを自動で持っている(username・password)
# エラーメッセージを自動で管理してくれる
# {{ form.non_field_errors }}これがそのまま使える


# サインアップフォーム
class CustomUserCreationForm(UserCreationForm):
    # カスタムユーザーフォーム作成
    # パスワード処理・検証を継承している
    class Meta:
        # ModelForm系で使う内部のMetaの開始(Meta=設計図)
        # ここで「どのモデルに対応させるか」「どのフィールドを使うか」を定義する

        model = User
        # このプロジェクトで使用されているUserモデルを指定している
        # 今回はDjango標準のユーザーモデルを参照

        fields = ("username", "email")
        # フォームでユーザーに入力させるフィールドを定義している
        # フォームの仕様として変更されることを想定していないため、タプルを使用している

        widgets = {
            # widgetsはDjangoフォームフィールドをどんなHTML要素として描写するか決める設定
            "username": forms.TextInput(
                attrs={"class": "form-control", "autofocus": True}
                # "form-control": Bootstrapのフォーム用CSSクラスを指定している
                # 入力欄の見た目を統一し、UIを整えるため
                # "autofocus": True:サインアップページを開いた時にこの入力欄にカーソルが自動で入る
            ),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    # パスワードはモデルのフィールドではなく、UserCreationFormが持つ
    # フォーム専用のフィールドのため、Meta.widgetsでは指定できない
    # そのためフォーム生成後(__init__)にwidgetを上書きして、見た目を調整している
    def __init__(self, *args, **kwargs):
        # __init__はフォームインスタンスが生成された直後に1回呼ばれる初期化処理
        # self=このフォーム自身
        # *argsは主にrequest.POST(フォーム送信データ)が入る
        # **kwargs　は追加情報(requestなど)を受け取るための引数
        # 現時点で使ってはいないが、親クラス(UserCreationForm)との互換性のために受け取っている
        super().__init__(*args, **kwargs)
        # super()=親クラス
        # ここでは親クラスの初期化をしている(UserCreationForm)
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "id": "password1"}
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "id": "password2"}
        )


# ログインフォーム
# AuthenticationFormはModelFormではないため
# widgetsはMetaではなく__init__で上書きする
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget = forms.TextInput(
            attrs={"class": "form-control", "autofocus": True}
        )

        self.fields["password"].widget = forms.PasswordInput(
            attrs={"class": "form-control"}
        )


# タスク作成フォーム
class TodoForm(forms.ModelForm):
    # forms.ModelFormを継承するとTodoモデルのフィールドからフォーム部品を自動で生成できる
    class Meta:
        # ModelFormの設定を書く内側のクラス
        model = Todo
        fields = [
            "title",
            "description",
            "due_date",
            "tags",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "due_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        # TodoCreateViewで渡してるkwargsの中のuserを受け取って
        # kwargs(キーワード引数の辞書)から""user"を取り出して
        # user変数に入れる
        # そしてkwargsから"user"を消す
        # user　がなければ　None
        # popは値を取り出して、元の辞書からは消える
        super().__init__(*args, **kwargs)
        # 親クラス(ModelForm)の初期化処理を実行
        # ここでself.fieldが作られる
        if user is not None:
            # userがきたその時だけ、次の処理をする
            # userを渡さない場面は山ほどあるためNoneを想定する
            self.fields["tags"].queryset = Tag.objects.filter(user=user)
            # self.fields["tags"]：TodoFormに含まれるフィールドの辞書から
            # TodoモデルからManyToManyField(Tag)からtagsを取り出している
            # .queryset:DBから取ってきたQuerySet(候補の集合)をフォームフィールドに
            # 設定(紐付け)してUIの選択肢として表示させる
