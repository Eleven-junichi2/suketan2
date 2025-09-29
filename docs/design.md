# design

# CLI

## UI

suketan2 コマンドではなくキー入力で項目を選択し操作するモードに入る。
suketan2 schedule <subcommand> [arguments]: スケジュールパターン自体を操作します。
suketan2 task <subcommand> [arguments]: スケジュールパターン内のタスクを操作します。

## `schedule`コマンド

`schedule create`
新しいスケジュールテンプレートを作成します。
構文: suketan2 schedule create "<スケジュール名>"

`schedule list`
登録されているスケジュールテンプレートの一覧を表示します。
構文: suketan2 schedule list

`schedule rename`
スケジュールテンプレートの名前を変更します。
構文: suketan2 schedule rename "<旧名>" "<新名>"

`schedule delete`
スケジュールテンプレートを削除します。
構文: suketan2 schedule delete "<スケジュール名>"

## `task`コマンド
操作対象のテンプレートは -s または --schedule オプションで指定します。

`task add`
テンプレートに新しいタスクを追加します。
構文: suketan2 task add "<タスク内容>" -s "<スケジュール名>" [オプション]
オプション:
- `-f, --from HH:MM`: 開始時刻
- `-t, --to HH:MM`: 終了時刻
- `-d, --duration <時間>`: 所要時間 (例: 1h30m, 45m)
- `-g, --tags <タグ>`: タグ（カンマ区切り）

`task list`
テンプレート内のタスクを一覧表示します。
構文: suketan2 task list "<スケジュール名>"

`task edit`
テンプレート内の既存タスクを編集します。
構文: suketan2 task edit <ID> -s "<スケジュール名>" [オプション]

`task delete`
テンプレート内のタスクを削除します。
構文: suketan2 task delete <ID> -s "<スケジュール名>"
