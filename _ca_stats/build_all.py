#!/usr/bin/env python3
"""アブレーション成績の4ページと、病院サイト用のデータセットをまとめて作り直す。
使い方（リポジトリのどこからでも）:  python3 _ca_stats/build_all.py
材料は同じフォルダの results_v2.json（集計値だけ。個人情報なし）。CAデータの Excel は使わない。"""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for name in ['build_ablation', 'build_wpw', 'build_pvc', 'build_avnrt', 'build_hospital']:
    print(f'--- {name}.py')
    subprocess.run([sys.executable, str(HERE / f'{name}.py')], check=True, cwd=HERE)
print('完了。git diff で確認してから commit / push してください。')
