# -*- coding: utf-8 -*-
"""버전 발행 (S8, P9·F2 대체 가드). approved 건만 발행 가능(F19 — validate_output --layer publish로 선검증).
사용: python version_publish.py --artifact <output/.../판정패키지.md> --name "투자_Thesis_Map_v33_20260827.md"
규칙: docs/에 동일 이름 존재 시 발행 중단(덮어쓰기 절대 금지) → 에스컬레이션.
"""
import argparse, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
NAME_RE = re.compile(r"^[\w가-힣]+_[\w가-힣]+_v\d+(\.\d+)?_\d{8}\.md$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact", required=True)
    ap.add_argument("--name", required=True, help="종목_문서유형_vN_YYYYMMDD.md 형식")
    args = ap.parse_args()

    src = Path(args.artifact)
    if not src.is_absolute():
        src = ROOT / args.artifact
    if not src.exists():
        print(f"⛔ 발행 대상 부재: {src}")
        sys.exit(1)
    if not NAME_RE.match(args.name):
        print(f"⛔ 네이밍 규약 위반: {args.name} (종목_문서유형_vN_YYYYMMDD.md)")
        sys.exit(1)

    dst = ROOT / "docs" / args.name
    if dst.exists():
        print(f"⛔ 파일명 충돌: docs/{args.name} 이미 존재 — 덮어쓰기 절대 금지(P9). 발행 중단, 에스컬레이션")
        sys.exit(1)

    text = src.read_text(encoding="utf-8-sig")
    if "정정 고지" not in text and "변경 이력" not in text:
        print("⚠️ 경고: 「정정 고지」/「변경 이력」 블록이 없음 — P9 확인 필요 (발행은 진행)")

    shutil.copy2(src, dst)
    print(f"✅ 발행 완료: docs/{args.name}")
    print("   docs/에 격리됨. 주기적 백업(외부 저장소)을 권장합니다. (F2 대체 가드)")


if __name__ == "__main__":
    main()
