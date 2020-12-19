# bot-line
ごちイラWebAPIに依存する簡易的なLineBot

## Features
l-m-api3を使用(簡単にかける)  
gochiira_apiを使用(簡単にかける)  
flexメッセージいっぱい(見た目がよい)  
Docker対応

## Installation
### 1 引っ張ってくる
```Dockerfile
docker pull ghcr.io/gochiira/bot-line:latest
```
### 2 環境変数(.env)を書く
```text
LINE_CHANNEL_TOKEN=HOGE
API_ENDPOINT=https://gochiira.example.com
API_TOKEN=GOCHIIRA_TOKEN
```
### 3 動かす
```Dockerfile
docker run --rm --env-file=<envファイルパス> -p <受付ポート>:1204 -t gochiira/bot-line
```

## Build
```text
docker build -t gochiira/bot-line-pc .
```
```text
docker buildx build --platform linux/arm/v7 --file Dockerfile -t gochiira/bot-line .
```