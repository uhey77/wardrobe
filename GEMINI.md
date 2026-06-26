# GEMINI.md

Geminiでこのリポジトリを扱う際の指示です。基本方針は [AGENTS.md](AGENTS.md) と同じです。

## コミュニケーション

- 回答は日本語で行ってください。
- 変更内容、実行した検証、未確認事項を簡潔に報告してください。

## プロジェクト

- ワードローブ管理・コーデ提案アプリです。
- 設計は [wardrobe_app_design.md](wardrobe_app_design.md) を参照してください。
- Pythonは `uv`、品質チェックは `ruff` と `mypy`、実行補助は `Taskfile.yml` を使います。

## Backend Architecture

バックエンドはクリーンアーキテクチャを意識します。

- `backend/app/domain`: フレームワーク非依存のドメインモデル
- `backend/app/application`: ユースケース、アプリケーションサービス
- `backend/app/presentation`: FastAPIなど外部入出力のアダプタ
- `backend/app/core`: 設定、アプリケーションの配線

依存方向は `presentation -> application -> domain` を基本とし、`domain` は外部技術へ依存させないでください。

## よく使うコマンド

- `task setup`: 依存関係をセットアップ
- `task dev`: backend/frontendを同時起動
- `task chroma:up`: ChromaDBを起動
- `task format`: Pythonコードを整形
- `task check`: ruff、mypy、pytest、frontend buildを実行

## 実装時の注意

- APIルートにビジネスロジックを直接書かず、`application` のユースケースへ委譲してください。
- API入出力スキーマは `presentation` 配下へ置いてください。
- キャッシュ、ビルド成果物、ローカルDBなどはコミット対象にしないでください。
