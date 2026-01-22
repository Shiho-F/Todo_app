# Todo_app
Django × Docker × MySQL で作る個人用Todoアプリ

## 概要
本アプリは、個人開発のTodo管理アプリです
ユーザー新規登録・ログイン機能を備え、タスクの作成・一覧表示・詳細確認ができます。
タスクにはタグを付けることができ、タグによる絞り込みも可能です。

## 使用技術

### バックエンド
- Python
- Django

### フロントエンド
- HTML
- Bootstrap
- JavaScript(簡単な動作処理)

### データベース
- MySQL
  
### インフラ　・開発環境
- Docker / docker-compose
- AWS(EC2)

## 設計

### ER図
![ER図](docs/er_diagram.png)

### インフラ構成図
![インフラ構成図](docs/infra_diagram.png)

### 画面遷移図
![画面遷移図](docs/screen_transition.png)

※ URL設計は実装前にNotionで整理した上で開発しています

## 開発環境(ローカル)

本プロジェクトでは、Pythonの依存関係にPoetryを使用しています。

### 使用バージョン
- Python 3.11
- Django 5.0.6
- Poetry

### セットアップ手順(ローカル)

#### 1. Poetryのインストール(Mac)
```bash
brew install poetry
```
#### 2. 依存関係のインストール
```bash
poetry install
```
#### 3.開発サーバーの起動
```bash
poetry run python manage.py runserver
```

## 開発環境の起動(Docker)

Docker / Docker Compose を使用して開発環境を構築します。

```bash
docker compose up --build
```
上記コマンドを実行すると、以下が自動で行われます。
- Python 3.11 環境の構築
- Poetryのインストール
- pyproject.toml/poetry.lockに基づく依存関係のインストール
- Django開発サーバーの起動

起動後、ブラウザで以下にアクセスしてください。
http://127.0.0.1:8000/todos/

※ 本アプリでは`/todos/`を起点に画面を表示しています。

## 開発環境の停止

```bash
docker compose down
```

## 依存関係管理について
 
本プロジェクトでは、Pythonの依存関係管理にPoetryを使用しています。

- pyproject.toml/poetry.lockにより依存関係を管理
- Dockerfile内で`poetry install --no-root`を実行し、アプリケーション本体はvolume経由で利用しています。
- 開発時のコード変更は即座にコンテナに反映されます。
