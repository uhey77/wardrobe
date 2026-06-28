# AGENTS.md

## 重要なルール

- 回答、コミットメッセージ、PRタイトル、PR本文は日本語で書いてください。
- 指摘・フィードバックを受けたら、再発防止に必要な内容を該当する指示ファイルへ反映してください。全エージェントに関係する内容は `AGENTS.md`、`CLAUDE.md`、`GEMINI.md` の整合性を保ってください。
- Skill や手順を増やす場合は横断的に比較し、抽象化できるものは統合し、責務が違うものは分割して保守性を維持してください。
- コミットには現在のタスクに関係する差分のみ含めてください。`task format` や自動整形が無関係ファイルを変更した場合、その差分は含めないでください。
- `pyproject.toml` の `version` は、ユーザーが明示的に指示した場合だけ変更してください。

## 反復タスク・手順化

繰り返し発生する作業、レビュー観点、検証手順、再発防止ルールは、該当するエージェント向けドキュメントに明記してください。
全エージェントに関係する内容は、`AGENTS.md`、`CLAUDE.md`、`GEMINI.md` の内容が矛盾しないように更新してください。

- 反復手順を書く場合は、いつ使うか、実行内容、検証方法、報告すべき未確認事項を簡潔に明記してください。
- 手順が長くなる場合は、各エージェント向けドキュメントに概要を置き、詳細な手順書やSkillへ分離してください。
- Claude向けのSkillを作る場合は `.claude/skills/<名前>/SKILL.md` を候補にしてください。
- Gemini向けの固有手順が必要な場合は `GEMINI.md` から参照できる形にしてください。
- 同じ設計方針を複数ファイルへ書く場合は、内容が古くならないよう同時に更新してください。

## コミュニケーション

- 回答は日本語で行ってください。
- 変更内容、実行した検証、未確認事項を簡潔に報告してください。
- 不明点があっても、リポジトリ内の文脈から安全に判断できる場合は作業を進めてください。
- 判断に迷う前提や未確認のリスクが残る場合は、作業結果とあわせて明示してください。

## プロジェクト概要

- ワードローブ管理・コーデ提案アプリです。
- 設計方針は [wardrobe_app_design.md](wardrobe_app_design.md) を参照してください。
- 初期マイルストーンでは FastAPI backend、Vite React frontend、ChromaDB 起動、固定レスポンスの疎通を扱います。
- Pythonは `uv`、品質チェックは `ruff` と `mypy`、実行補助は `Taskfile.yml` を使います。
- フロントエンドは `frontend` 配下の Vite React アプリで、依存管理は `npm` を使います。

## Backend Architecture

バックエンドはクリーンアーキテクチャとDDD（ドメイン駆動設計）を設計ルールとして採用します。
ドメイン層には服・コーデ・色・季節・利用シーンなど、このアプリの業務概念とルールを表現します。

- `backend/app/domain`: フレームワークに依存しないドメインモデル
- `backend/app/application`: ユースケース、アプリケーションサービス
- `backend/app/presentation`: FastAPIなど外部入出力のアダプタ
- `backend/app/infrastructure`: DB、ChromaDB、LLM、画像ストレージなど外部技術の実装
- `backend/app/core`: 設定、アプリケーションの配線

依存方向は原則として `presentation -> application -> domain` とします。
`infrastructure` は `application` や `domain` が定義した抽象に対する実装を置き、`application` から `infrastructure` へ直接依存させないでください。
`core` は設定と依存注入の配線を担当してよく、`domain` から外側の層へは依存させないでください。

## DDD 設計ルール

DDDは以下を実装時の設計ルールとして守ります。

- ユビキタス言語を揃え、コード上の名前も `ClothingItem`、`Outfit`、`Season`、`StyleTag` などドメイン用語に寄せてください。
- 一意性とライフサイクルを持つものはエンティティ、値だけで意味が決まるものは値オブジェクトとして `domain` に置いてください。
- ドメインルールは `domain` に置き、API都合のバリデーションや表示変換は `presentation` に置いてください。
- ユースケースは `application` に置き、ドメインオブジェクトを使って処理の流れを表現してください。
- リポジトリや外部サービスが必要な場合、抽象は `application` または `domain` に置き、`abc.ABC` と `@abstractmethod` で定義してください。具体実装は `infrastructure` に置いてください。
- 集約は整合性を守る境界として扱い、初期の主要集約は `ClothingItem` と `Outfit` を候補にしてください。

## 開発コマンド

- セットアップ: `task setup`
- バックエンド起動: `task backend:dev`
- フロントエンド起動: `task frontend:dev`
- 両方起動: `task dev`
- ChromaDB起動: `task chroma:up`
- Python lint: `task lint`
- Python型検査: `task typecheck`
- Pythonテスト: `task test`
- フロントエンドビルド: `task frontend:build`
- 全体検証: `task check`
- Python整形: `task format`

Pythonの依存管理と実行には `uv` を使います。ruff、mypy、pytestはTaskfile経由で実行してください。

## テスト配置

- Backendのテストは `backend/tests` に置いてください。
- Frontendのテストは `frontend/tests` に置いてください。

## 実装ルール

- 既存のディレクトリ構成とレイヤ責務を優先してください。
- コード、API、UI、テスト名にはロードマップ上の段階名や段階番号を使わず、`service_status` や `item_registration` など機能名・ドメイン名を使ってください。
- ドメインモデルにFastAPI、Pydantic、DBクライアントなど外部技術の詳細を持ち込まないでください。
- API入出力用のPydanticスキーマは `presentation` 配下に置いてください。
- 新しいユースケースは `application` 配下に作り、APIルートから直接ビジネスロジックを書かないでください。
- ChromaDB、LLM、画像ストレージ、CLIPなどの具体実装は `infrastructure` 配下に置いてください。
- 生成物、キャッシュ、ローカルデータはコミット対象にしないでください。
- Pythonは3.12以上を前提とし、型ヒントは `list[str]` や `dict[str, int]` などの built-in generics を使ってください。
- Pythonの `dataclasses.dataclass` / `@dataclass` は使用しないでください。
- API入出力スキーマ、設定、外部I/Oの検証には Pydantic v2 を使用してください。
- Pydantic v2を使う場合は、`Config` class、`validator`、`root_validator`、`parse_obj`、`dict()` などのv1系APIを避け、`ConfigDict`、`field_validator`、`model_validator`、`model_validate`、`model_dump()` などのv2系APIを使ってください。
- `domain` のエンティティ、値オブジェクト、ドメインルールには Pydantic を持ち込まず、通常のclassで実装してください。
- `typing.Protocol` は使用しないでください。リポジトリや外部サービスの抽象は `abc.ABC` と `@abstractmethod` で定義してください。
- `asyncio.get_event_loop()` は使わず、実行中ループが必要な場合は `asyncio.get_running_loop()` を使ってください。

## コーディングスタイル

- 異常系・スキップ条件は先に処理し、正常系のネストを深くしないでください。
- 再利用しない中間変数は作らず、名前が意味を加えない場合はインラインで表現してください。
- 同じ文字列や値を複数回書かず、意味のある定数や変数にまとめてください。
- `next`、`min`、`max`、内包表記、`enumerate(..., start=...)`、`any`、`all` などの組み込み機能を適切に使ってください。
- 型ヒントで入力を制限できている場合、同じ制約を重複して実行時バリデーションしないでください。
- `None` は意味を持つ状態として扱い、不要な `None` 初期化は避けてください。
- `zip()` は長さ不一致を検知したい場面では `strict=True` を付けてください。
- `in` 演算子で繰り返し検索するコレクションは、順序が不要なら `set` を使ってください。
- ファイル拡張子やパスの扱いは、可能なら `pathlib` などの構造化されたAPIを使ってください。
- 処理は意味のある単位でまとめ、過剰な小関数化や private method の乱立は避けてください。
- 関数・メソッドの引数は呼び出し側が制御すべき値に絞り、内部実装の詳細を渡させないでください。
- 関数名は基本的に動詞にしてください。独自クラスやドメイン概念の名前は省略せず、コード全体で同じ用語を使ってください。
- 0-indexed の値は `_index` / `_idx`、1-indexed の値は `_number` など、基準が分かる名前にしてください。
- `except` は広く取りすぎず、想定する例外クラスに絞ってください。
- Error メッセージは英語で書いてください。

## コメント

- コメントはコードから読み取れない意図、制約、回避策、外部仕様の根拠を補足するために書いてください。
- コードを読めば分かる説明や、コミットメッセージ・PR本文に書くべき経緯はコメントにしないでください。
- TODOは未対応事項や将来の拡張ポイントが具体的に分かる形で書いてください。
- 日本語と英語は、周辺コードや既存ファイルの傾向に合わせてください。

## 変更管理

- 作業前後に `git status` と `git diff` を確認し、無関係な変更を混ぜないでください。
- 既存の未コミット変更がある場合、それを勝手に戻さず、今回の作業に必要な範囲だけ編集してください。
- ステージングやコミットを行う場合は、対象差分を精査してから実行してください。
- コミットメッセージとPR文は、変更内容・検証結果・未確認事項が分かる日本語で書いてください。

## 検証

コードを変更した場合は、原則として以下を実行してください。

```bash
task check
```

変更範囲が限定的な場合でも、少なくとも関連する `task lint`、`task typecheck`、`task test`、`task frontend:build` のいずれかを実行してください。
ドキュメントのみの変更では `task check` は必須ではありませんが、リンクやコマンドを変えた場合は整合性を確認してください。
