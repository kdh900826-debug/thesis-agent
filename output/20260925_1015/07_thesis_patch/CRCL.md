# ThesisPatch 인덱스 — CRCL (run 20260925_1015)

- 카드 전문 86행 열람(F20) — axes 8 / key_metrics 7 / catalysts 4 / risks 5 / version_history 12
- 패치 3건 (전부 requires_human_approval: true)

| slug | 후보 | field | op | 요지 |
|---|---|---|---|---|
| reserve_income_binance_renewal | tpc_06 | axes[reserve_income] | amend | Binance 5년 재계약(8-K 9/22)·$1억 사모 — 비용 구조 고정, 요율 비공개로 크기 미단정 |
| diversification_arc_baseline | tpc_08 | axes[diversification] | annotate | Arc 첫 주 기준선(grade 2 CEO 발언), grade 4 온체인은 삼각검증 전용, P7 매출 인식 전 |
| catalysts_clarity_status | tpc_09 | catalysts | amend | CLARITY 9/15 이후 재표결 미확정 — grade 4 확인 대상 표기 |

## dry-run
[fact] scratchpad 사본 순차 적용 3/3 통과(before 1회·YAML 파싱·expected_after). 역순도 통과. 미리보기: `CRCL_dryrun_merged_preview.yaml`.

## 승인 순서
[fact] before 영역 비중첩·계수 불변 → 순서 무관. 권장: tpc_06 → tpc_09 → tpc_08.

## 제외·로그
- tpc_07 (USDC 점유율 제3계열) — [fact] 사람 결정(su_1015_10) 종속, 스킵 + unconfirmed 이월.
- 근거 부족으로 제외된 후보: 없음.
- [fact] 관측만: regulation_sector_legislation 라벨·risks[1]의 '9/15 절차 표결' 서술이 c_20260925_CRCL_7과 시점 불일치 — 후보 범위 밖, 차기 후보로 기록.

> 승인 큐 등재 미수행 — 오케스트레이터가 approvals.py add로 3건 등재할 것.
