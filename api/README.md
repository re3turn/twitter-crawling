# FastAPI web-api server

## ローカルでの実行

### 要件

- pipenv

### インストール

```
pipenv install
```

### 環境変数

|環境変数|説明|
|--------|----|
|DATABASE_URL| データベースURL|
|MONGO_DATABASE| データベース名|

`.env` または環境変数に以下を設定する

```
DATABASE_URL=mongodb://user:password@localhost:27019
MONGO_DATABASE=twitterdb
```

### 実行

DB起動後以下を実行

```
pipenv run python run.py
```
オートリロードする場合は以下

```
pipenv run python run_reload.py
 ```
