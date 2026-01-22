FROM python:3.11
# Linux + Python3.11が入った箱を使う
# FROM:元にするイメージを指定する

# 作業ディレクトリを作成
WORKDIR /app
# コンテナ内の/appを作業場所にする
# cd　/appした状態になる
# docker-compose.ymlのworking_dir: /appと意味的に揃ってる

# Poetryをインストール
RUN pip install --no-cache-dir poetry
# コンテナ内でPoetryを使いたいからpipはPoetryを入れるためだけに使用している
# RUN：イメージをビルドするときにコマンドを実行する
# pipは通常.whlや.tar.gzなどのファイルをキャッシュディレクトリに保存する
# しかしDockerの作っては壊す性質上、不要なキャッシュファイルをイメージのレイヤーに残さないようにする
# --no-cache-dir：pipが一時的にダウンロードした
# .whlや.tar.gz などのキャッシュファイルを保存せず、インストール後に破棄する

# 依存関係ファイルだけを先にコピー
COPY pyproject.toml poetry.lock* /app/
# COPY コピー元パス+コピー先パス
# ビルド時にローカルのファイル(pyproject.toml)をDockerのイメージの中にコピーしている

# 依存関係をインストール(仮想環境はPoetry管理)
RUN poetry install --no-root
# poetry.lockがあればそれを優先して読み、
# なければpyproject.tomlを元に依存関係を解決する
# これらのファイルに書いてある依存関係を全てインストールする
# その中にDjango5.0.6が含まれている
# ローカルの環境構築時にpoetry add django==5.0.6で依存を追加したため
# root:Poetryでいうrootはプロジェクト自身(Todo_app)
# --no-root:は依存関係(Djangoなど)をインストールして、このプロジェクト自体はインストールしないという意味


