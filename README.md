# Wardrobe

ワードローブ管理・コーデ提案アプリ

## セットアップ

```bash
task setup
```

## 起動

```bash
task chroma:up
task dev
```

- Backend: [http://localhost:8000](http://localhost:8000)
- Frontend: [http://localhost:5173](http://localhost:5173)
- ChromaDB: [http://localhost:8001](http://localhost:8001)

`task chroma:up`はフォアグラウンドで起動します。Dockerを使う場合は`task chroma:docker:up`を利用できます。

## Backend Architecture

バックエンドはクリーンアーキテクチャを意識して、Phase0時点では以下の責務に分けています。

- `backend/app/domain`: フレームワークに依存しないドメインモデル
- `backend/app/application`: ユースケース
- `backend/app/presentation`: FastAPIなど外部入出力のアダプタ
- `backend/app/core`: 設定とアプリケーションの配線

## 検証

```bash
task check
```
