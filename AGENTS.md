# AGENTS.md

このリポジトリで作業するAIエージェント向けの共通指示です。

## コミュニケーション

- 回答は日本語で行ってください。
- 変更内容、実行した検証、未確認事項を簡潔に報告してください。
- 不明点があっても、リポジトリ内の文脈から安全に判断できる場合は作業を進めてください。

## プロジェクト概要

- ワードローブ管理・コーデ提案アプリです。
- 設計方針は [wardrobe_app_design.md](wardrobe_app_design.md) を参照してください。
- Phase0では FastAPI backend、Vite React frontend、ChromaDB 起動、固定レスポンスの疎通を扱います。

## Backend Architecture

バックエンドはクリーンアーキテクチャを意識して分割します。

- `backend/app/domain`: フレームワークに依存しないドメインモデル
- `backend/app/application`: ユースケース、アプリケーションサービス
- `backend/app/presentation`: FastAPIなど外部入出力のアダプタ
- `backend/app/core`: 設定、アプリケーションの配線

依存方向は原則として `presentation -> application -> domain` とし、`domain` から外側の層へ依存させないでください。

## 開発コマンド

- セットアップ: `task setup`
- バックエンド起動: `task backend:dev`
- フロントエンド起動: `task frontend:dev`
- 両方起動: `task dev`
- ChromaDB起動: `task chroma:up`
- 全体検証: `task check`
- Python整形: `task format`

Pythonの依存管理と実行には `uv` を使います。ruffとmypyはTaskfile経由で実行してください。

## 実装ルール

- 既存のディレクトリ構成とレイヤ責務を優先してください。
- ドメインモデルにFastAPI、Pydantic、DBクライアントなど外部技術の詳細を持ち込まないでください。
- API入出力用のPydanticスキーマは `presentation` 配下に置いてください。
- 新しいユースケースは `application` 配下に作り、APIルートから直接ビジネスロジックを書かないでください。
- 生成物、キャッシュ、ローカルデータはコミット対象にしないでください。

## 検証

コードを変更した場合は、原則として以下を実行してください。

```bash
task check
```

ドキュメントのみの変更では必須ではありませんが、影響がある場合は関連する検証を実行してください。
