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

## アイテム登録

- フロントエンドで画像を選択して登録すると、バックエンドが画像を `.data/uploads` に保存します。
- 登録メタデータは `.data/items.json` に保存され、`GET /api/items` で一覧取得できます。
- ChromaDB が起動している場合は、embedding と metadata を `wardrobe_items` コレクションへ同期します。
- 現時点の属性抽出と embedding は、Gemini Vision / CLIP の実プロバイダへ差し替える前提のローカル実装です。

主なAPI:

- `POST /api/items`: 画像バイトを登録します。`Content-Type` と `X-Wardrobe-Filename` ヘッダーを使います。
- `GET /api/items`: 登録済みアイテムを一覧します。
- `GET /api/items/{item_id}/image`: 保存済み画像を返します。

## Backend Architecture

バックエンドはクリーンアーキテクチャとDDD（ドメイン駆動設計）を設計ルールとして採用します。

- `backend/app/domain`: フレームワークに依存しないドメインモデル
- `backend/app/application`: ユースケース
- `backend/app/presentation`: FastAPIなど外部入出力のアダプタ
- `backend/app/infrastructure`: DB、ChromaDB、LLM、画像ストレージなど外部技術の実装
- `backend/app/core`: 設定とアプリケーションの配線

依存方向は `presentation -> application -> domain` を基本とし、外部技術の具体実装は `infrastructure` に置きます。

## テスト配置

- Backend: `backend/tests`
- Frontend: `frontend/tests`

## 検証

```bash
task check
```
