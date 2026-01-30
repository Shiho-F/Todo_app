FROM python:3.11
# Linux + Python3.11が入った箱を使う
# FROM:元にするイメージを指定する



RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ここから７〜１１行目の解説
# RUN apt-get update && apt-get install -y \
# # RUN...Dockerイメージを作るとき(ビルド時)に実行される命令
# # apt-get update → OSのアプリ一覧を最新にする
# # apt-get install → 必要なソフトをインストール
# # -y → 全部yesでいいから聞かずに入れて
#     default-libmysqlclient-dev \   
#     # MySQLと話すための部品
#     build-essential \
#     # C言語の開発セット
#     # mysqlclient は Cで書かれてる
#     pkg-config \
#     # ライブラリ案内係
#     # libmysqlclientどこにあるか教える
#     # これがないとビルド失敗する
#     && rm -rf /var/lib/apt/lists/*
#     # && どれか一つでも失敗したら、その時点で止まる
#     # apt-getが作ったキャッシュを削除
#     # イメージを軽くしてくれる
    
    # つまり、DjangoをMySQLと接続するために使用する
    # mysqlclient(C拡張ライブラリ)をDocker環境上で
    # 正常にビルド・インストールできるようにするための下準備



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



