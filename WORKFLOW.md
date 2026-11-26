# 新しい動画を出すときの手順

1. Metricoolに予約投稿したら、同じ日に `posts.py` へ記事を追加する
   （冒頭に広告表記、結論ボックス、手順、Amazonアフィリエイトリンク tag=kittenpaw-22）。
2. `videos.py` の `PENDING` に「記事スラッグ: Metricool投稿のuuid」を追加。
3. `python3 gen.py && rm -rf docs && cp -r site docs` → commit → push。
4. 動画が公開されたら、Metricool の publicUrl から動画IDを取り、
   `PENDING` から `VIDEOS` に移して再生成・push（毎日の自動チェックが行う）。
