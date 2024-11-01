import os
import smtplib
from email import message

from dotenv import load_dotenv

load_dotenv()

smtp_host = os.getenv("SMTP_HOST")  # 例: example.sakura.ne.jp
smtp_port = int(
    os.getenv("SMTP_PORT")
)  # さくらメールサーバーは通常587番のポート番号を使用する
smtp_user = os.getenv("SMTP_USER")  # 送信元のメールアドレス
smtp_pass = os.getenv("SMTP_PASS")  # メールアドレスのパスワード

from_email = os.getenv("FROM_EMAIL")  # これも送信元のメールアドレス
to_email = "c1221251@st.kanazawa-it.ac.jp"  # 送信先メールアドレス
subject = "テストメール"  # 主題
body = "This is test mail"  # メール本文

msg = message.EmailMessage()
msg.set_content(body)
# 本文を入力
msg["Subject"] = subject  # 件名を入力
msg["From"] = from_email
msg["To"] = to_email
server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
server.login(smtp_user, smtp_pass)
result = server.send_message(msg)
server.quit()
