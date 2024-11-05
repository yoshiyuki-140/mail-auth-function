# mail-auth-function
メール認証機能を他のサービスと組み合わせて使うために一度アセットとして作ってみる。

# 環境構築

動かすときは、プロジェクトルートに以下の形式の`.env`ファイルを設置すること。
```bash
# ./.env
# DB用のデータ
POSTGRES_USER="db_username"
POSTGRES_PASSWORD="db_password"
POSTGRES_DB="db_name"
POSTGRES_DEV_DB="db_name" # 開発環境のDBの名前

# コンテナ内におけるPostgreSQLコンテナのIPアドレス(固定化のため。なんでもよいが、compose.ymlの最後の方に記載されているネットワークアドレスに該当するものでないといけない)
POSTGRES_HOST_IP="192.168.100.3"


# email送信用のデータ
SMTP_HOST="example.sakura.ne.jp"  # 例: example.sakura.ne.jp
SMTP_PORT=587  # さくらのメールサーバーは通常587番ポートを使用
SMTP_USER="username@username.sakura.ne.jp"  # 送信元のメールアドレス
FROM_EMAIL="username@username.sakura.ne.jp" # 送信元
SMTP_PASS="password" # メールアドレスのパスワード
```

```bash
make up # docker compose up -d
```
localhost:8000にアクセス

