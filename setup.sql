-- セットアップ用のSQL

CREATE EXTENSION pgcrypto;  -- パスワード暗号化のための拡張をインストール

-- ユーザー情報を格納するテーブル作成クエリ
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
);