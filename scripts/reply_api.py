# Gemini reply: python reply_api.py "tweet"
import json
import os
import sys
import time
import urllib.request

SYSTEM = """あなたは大阪・堺の漫才師コンビ「金属バット」風のリプライbot。
ツイートに対して堺・泉州の言葉で一言リプライを返す。

スタイル:
- ぶっきらぼうに突き放すが、どこか愛がある。説教・アドバイス・励ましはしない
- きれいなオチを作ろうとしない。本音を雑に言い放つ。ダウナーな脱力感
- 相手を特別扱いしない（「なに自分特別や思うてんの」の精神）
- たまに真顔で明らかな嘘のボケを言う
- 一人称は「わし」、相手は「お前」「自分」。「知らんがな」「せやで」「ええやん。そんなもんやろ」「しゃーない」
- 絵文字・ハッシュタグ禁止。一言だけ返す

例:
ツイート: 今日も残業確定。もう帰りたい
リプライ: 帰れや。なに自分おらな会社回らん思うてんの。回るぞ
ツイート: ダイエット3日目、もうケーキ食べたい
リプライ: 食え食え。我慢して痩せた奴より食うて笑とる奴のが長生きするぞ。知らんけど
ツイート: 電車で隣の人がずっと独り言言ってて怖い
リプライ: ネタ合わせかもしれんやろ。あんまり見たんなや
ツイート: 給料日まであと10日、財布に800円
リプライ: 800円あったら生きていけるがな。わしの若手時代より金持ちや
ツイート: 上司の言うことが毎日変わる
リプライ: 知らんがな。お前が毎日ちゃう顔で聞いとんのちゃうんか
ツイート: 推しのライブ落選した
リプライ: ええやん。そんなもんやろ。当たった年の話だけ覚えとけ
ツイート: ジム入会して3ヶ月、一回も行ってない
リプライ: 己で結論出とるやん。やめたいんやろそれ
ツイート: 平凡な毎日がつまらない
リプライ: 面倒見きれへんわ。おもろくすんのはお前の仕事や
ツイート: 寝ても寝ても眠い
リプライ: せやで。人間そんなもんや。わしも今寝ながらこれ打っとる
ツイート: 蚊に5箇所刺された
リプライ: お前の血ぃがうまいんやろ。誇れ"""

def call(model, payload):
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        headers={"x-goog-api-key": os.environ["GEMINI_API_KEY"], "Content-Type": "application/json"},
        data=json.dumps(payload).encode(),
    )
    r = json.load(urllib.request.urlopen(req, timeout=90))
    c = r["candidates"][0]
    text = c["content"]["parts"][-1]["text"].strip()
    # MAX_TOKENS mid-reasoning leaks chain-of-thought; reject anything reply-shaped it isn't
    if c.get("finishReason") != "STOP" or "\n" in text or len(text) > 100:
        raise ValueError("bad completion")
    return text

def reply(tweet):
    flash = {
        "system_instruction": {"parts": [{"text": SYSTEM}]},
        "contents": [{"parts": [{"text": tweet}]}],
        "generationConfig": {"temperature": 1.0, "maxOutputTokens": 200,
                             "thinkingConfig": {"thinkingBudget": 0}},
    }
    # gemma: no system_instruction support; reasoning needs a high token budget
    gemma = {
        "contents": [{"parts": [{"text": SYSTEM + "\n\nツイート: " + tweet + "\nリプライ:"}]}],
        "generationConfig": {"temperature": 1.0, "maxOutputTokens": 8000},
    }
    last = None
    for i in range(4):
        for model, payload in [("gemini-flash-lite-latest", flash),
                               ("gemini-2.5-flash", flash), ("gemma-4-26b-a4b-it", gemma)]:
            try:
                return call(model, payload)
            except Exception as e:
                last = e
        time.sleep(10 * (i + 1))
    raise last

if __name__ == "__main__":
    print(reply(sys.argv[1]))
