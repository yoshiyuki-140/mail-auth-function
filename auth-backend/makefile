.PHONY: run ac dac up f test

# サーバー立ち上げ
run:
	# uvicorn main:app --reload
	uvicorn main:app --reload --host localhost --port 8000

# 仮想環境有効化
ac:
	. ./venv/bin/activate

# 仮想環境無効化
dac:
	deactivate

# docker コンテナ ビルド
dockerbuild:
	docker build -t auth-backend .

# dockerコンテナ立ち上げテスト(単体)
up:
	docker run --publish 8000:8000 --name auth-backend --rm auth-backend

f:
	autoflake --remove-all-unused-imports -r --in-place .
	isort .	
	black .

test:
	pytest --timeout=10