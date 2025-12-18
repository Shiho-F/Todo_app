# ORM to SQL 学習メモ

## 概要
 DjangoのModel定義をSQLに変換し、DBが内部でどのように動いているかを理解するためのメモ

---
# ER図ベースSQL

## 🔽タスク(todos)テーブルを作成
 CREATE TABLE todos (id BIGINT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id),
 ER図では論理設計としてINTを使用していたが、Djangoの実装では主キーにBigAutoFieldが使用されるため
 物理設計としても、ここではBIGINTに合わせている

##  🔽タイトルカラム
 title VARCHAR(100) NOT NULL,

##  🔽タスクの詳細カラム
 description TEXT NULL,

## 🔽期限(締切日)カラム作成
 due_date DATE NULL,

## 🔽完了/未完了フラグ
 is_completed TINYINT(1) NOT NULL DEFAULT 0,

## 🔽作成日時カラム
 created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 ・DEFAULT → 値が渡されなかった時の初期値
 ・CURRENT_TIMESTAMP → 今この瞬間の日時
 ・この2つを組み合わせるとINSERT文でcreated_atを指定しなかった場合に自動で今の時刻を入れてくれる

## 🔽更新日時カラム
 updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
 ・ON UPDATE CURRENT_TIMESTAMP → DBが自動でupdated_atを今の時刻に変更


## 🔽user_id(外部キー)
 CONSTRAINT fk_todos_user
 CONSTRAINT → 制約(ルール)を定義する宣言
 fk_todos_user → 制約の名前（自分で付ける）
 FOREIGN KEY (user_id)
 外部キーです。という宣言
 REFERENCES auth_user(id)
 auth_user:参照先のテーブル
 id:そのテーブルの主キー
 ON DELETE CASCADE
 親(auth_userの1行)が削除されたら子(todosの該当行)も一緒に削除する
 );

## ✅　AUTO_INCREMENT+PRIMARY KEYの裏側
 INSERT INTO todos (title) VALUES('買い物')；
 結果的に内部では id = 1(自動採番)

## ✅　created_atの内部的な動き
 INSERT INTO todos (title) VALUES ('買い物');
 created_atを指定していないので、テーブル定義のDEFAULT　CURRENT_TIMESTAMPが適用されDBが自動的に現在時刻をcreated_atに設定する

## ✅　updated_atの内部的な動き
 UPDATE todos SET title = '買い物と大掃除', updated_at = CURRENT_TIMESTAMP WHERE id = 1;
 idが1のタスクについてタイトルを変更し、ON UPDATE CURRENT_TIMESTAMPによりDBが自動的に更新日時を現在時刻に設定する
 
## ✅外部キー制約の裏側
 ・インサート時
 INSERT INTO todos (title, user_id) VALUES ('買い物', 999);
 1.auth_user.idに999が存在するか検索
 2.無ければエラー(Cannot add or update a child row)
 外部キー = 存在チェック

・デリートされていた時(CASCADE)
 DELETE FROM auth_user WHERE id = 1;
 1. auth_user.id = 1を削除
 2. fk_todos_userを確認
 3. todos.user_id = 1を探す
 4. 見つかった行を自動削除

## ✅クエリ例
 SELECT users.name, todos.title FROM users JOIN todos ON users.id = todos.user_id WHERE todos.is_completed = 0;

 FROM users: 
 どのテーブルを土台にするか決めている
 JOIN ± ON:
 1.usersテーブルの1行目をとる(users.id = 1)
 2.todosテーブルの全部を見る
 3.users.id = todos.user_idが一致する行を探す
 4.一致したら横に合体する(todosテーブルを結合して横に広げている)
 WHERE todos.is_completed = 0:
 JOIN後の結果に対して条件に合わない行を削除
 削除しないと完了・未完了関係なく全部くっついて全タスクを表示してしまう
 ここでは未完了のタスクだけを出している

 ### つまり何をやってるのか
 ユーザ表とタスク表をユーザーIDで結合して、まだ完了していないタスクについてユーザ名とタスクのタイトルを取得している



# ・論理設計：どんなデータを、どんな関係で持つかを考える段階
# ・物理設計：それをDBにどう作るかを決める段階