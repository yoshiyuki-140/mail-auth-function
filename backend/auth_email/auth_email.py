import os
import smtplib
from email import message

from dotenv import load_dotenv

load_dotenv()


def send_token_via_email(token: int, email: str):
    """Eメール経由で認証トークンを送信する関数

    Args:
        token (int): 6桁の数値
    """
    smtp_host = os.getenv("SMTP_HOST")  # 例: example.sakura.ne.jp
    smtp_port = int(os.getenv("SMTP_PORT"))  # さくらメールサーバーのポート番号
    smtp_user = os.getenv("SMTP_USER")  # 送信元のメールアドレス
    smtp_pass = os.getenv("SMTP_PASS")  # メールアドレスのパスワード

    from_email = os.getenv("FROM_EMAIL")  # これも送信元のメールアドレス
    # to_email = "c1221251@st.kanazawa-it.ac.jp"  # 送信先メールアドレス
    to_email = email  # 送信先メールアドレス

    subject = "認証トークン"  # 主題
    file_path = os.path.join(os.path.dirname(__file__), "email_message.txt")
    with open(file_path) as f:
        body = f"""{f.read()}\n{token}"""  # メール本文

    msg = message.EmailMessage()
    msg.set_content(body)
    # 本文を入力
    msg["Subject"] = subject  # 件名を入力
    msg["From"] = from_email  # 送信元メールアドレス
    msg["To"] = to_email  # 送信先メールアドレス
    server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)  # SMTPサーバーへの接続
    server.login(smtp_user, smtp_pass)  # ログイン
    result = server.send_message(msg)  # メッセージ送信
    server.quit()  # ログアウトしてSMTPサーバーへの接続解除
    if result == {}:
        print("送信成功")
        return True
    else:
        print("送信失敗:", result)
        return False
