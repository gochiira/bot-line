# Pythonイメージの取得
FROM python:3.8.6-slim-buster
# ワーキングディレクトリの指定
WORKDIR /app
COPY ./requirements.txt ./
COPY ./line_magic/requirements.txt ./line_magic_requirements.txt
RUN pip install -r requirements.txt
RUN pip install -r line_magic_requirements.txt
# .NudeNet/lite_classifier Checkpointのダウンロード
RUN python3 -c "from nudenet import NudeClassifierLite;x = NudeClassifierLite()"
# モジュールを揃える
COPY . .
# 起動環境設定
EXPOSE 1204
ENTRYPOINT [ "gunicorn", "main:app" ]
CMD [ "-c", "gunicorn_config.py" ]