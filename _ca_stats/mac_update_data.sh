#!/bin/zsh
# 年1回のデータ更新（Mac で実行）：CAデータの Excel を集計し、集計値だけを GitHub へ送る。
# Excel・患者さんの情報・集計スクリプト（analyze_v2.py）は Mac（Google ドライブ）から出さない。
#
# 使い方:  zsh ~/tsuguszk.github.io/_ca_stats/mac_update_data.sh <FileMakerから書き出したCAデータ.xlsx>
#   （Excel はターミナルにドラッグ＆ドロップすると場所が入る）
set -e
[ -f "$1" ] || { echo "使い方: zsh _ca_stats/mac_update_data.sh <CAデータ.xlsx>"; exit 1; }

REPO="$(cd "$(dirname "$0")/.." && pwd)"
ANALYZE_DIR="${ANALYZE_DIR:-$HOME/Library/CloudStorage/GoogleDrive-tsugutoshi@gmail.com/マイドライブ/dropbox_Google/AI_workspace/260626website改編/ca_stats}"
export CA_XLSX="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"

cd "$REPO" && git pull

# 1) 集計（Mac の中だけで動く。結果は集計値だけの results_v2.json）
( cd "$ANALYZE_DIR" && uv run -q --with pandas --with openpyxl python analyze_v2.py )

# 2) リポジトリへ写す。最初と最後の治療日は年月までに丸め、データ更新日（今日）を入れる
python3 - "$ANALYZE_DIR/results_v2.json" "$REPO/_ca_stats/results_v2.json" <<'EOF'
import datetime, json, sys
R = json.load(open(sys.argv[1], encoding='utf-8'))
o = R['overall']
o['first'], o['last'] = o['first'][:7], o['last'][:7]
d = datetime.date.today()
R['updated'] = f'{d.year}年{d.month}月{d.day}日'
json.dump(R, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
EOF

# 3) 4ページと病院サイト用を作り直す（クラウドでも同じコマンドで作れる）
python3 _ca_stats/build_all.py

# 4) 送る
git add _ca_stats/results_v2.json ablation.html wpw_results.html avnrt_results.html pvc_results.html _hospital
git commit -m "アブレーション成績：集計値を更新（$(date +%Y年%-m月%-d日)）"
git push
echo "完了。ページの中の期間の文言（「2026年9月まで」など）は、クラウドの Claude に「集計値を更新した」と伝えて直してもらう。"
