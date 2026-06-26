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

バックエンドはクリーンアーキテクチャとDDD（ドメイン駆動設計）を設計ルールとして採用します。

- `backend/app/domain`: フレームワークに依存しないドメインモデル
- `backend/app/application`: ユースケース
- `backend/app/presentation`: FastAPIなど外部入出力のアダプタ
- `backend/app/infrastructure`: DB、ChromaDB、LLM、画像ストレージなど外部技術の実装
- `backend/app/core`: 設定とアプリケーションの配線

依存方向は `presentation -> application -> domain` を基本とし、外部技術の具体実装は `infrastructure` に置きます。

## 検証

```bash
task check
```
