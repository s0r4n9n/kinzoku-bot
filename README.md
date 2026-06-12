# kinzoku-bot

金属バット風の一言リプライを返すbot。Gemini API（few-shotプロンプト）使用。

## 準備

`.env` に API キーを置く（https://aistudio.google.com/apikey で無料取得）:

```
GEMINI_API_KEY=...
```

## 使い方

```sh
./reply.sh "今日も残業確定。もう帰りたい"
```

ツイート→リプライのTSVを一括生成・補完:

```sh
sh scripts/fill_empty.sh output/pairs_api.tsv   # 2列目が空の行を生成
```

モデルは gemini-2.5-flash → gemma-4-26b-a4b-it の順にフォールバック（無料枠対策）。
ペルソナとfew-shot例は `scripts/reply_api.py` の `SYSTEM` を編集。
