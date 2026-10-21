# ThesisPatch — CRWV / key_metrics / annotate (이자 커버리지 계산기준)

- **Run**: 20260815_1408 · 2026-08-15
- **대상 필드**: `key_metrics` (이자 커버리지 항목)
- **operation**: `annotate`
- **승인 필요**: ✅ `requires_human_approval: true`
- **핵심 논거 역전 여부**: ❌ 아님

## 무엇을

```diff
- - "이자 커버리지 (EBITDA/이자 — 1.5x 이하 = 위험, 현 ~2.2x ⚠️갱신)"
+ - "이자 커버리지 — ⚠️계산기준 미확정. 분자(Adj. EBITDA / GAAP 영업이익 중 택1)·분모(순이자비용 / 총이자비용 중 택1)·기간(분기 연환산 / TTM 중 택1)을 확정해야 KC-CRWV-3 판정이 가능하다. 임계는 1.5x 이하 경고·1.0x 이하 발동(KC-CRWV-3). 카드상 '현 ~2.2x'는 직전 세션 확인분으로 1차 자료 재대조 미완 ⚠️갱신"
```

## 왜 — 이번 Run에서 실제로 판정 불가가 발생했다

`kill_conditions.yaml`의 KC-CRWV-3은 1.5x(경고)·1.0x(발동) 임계를 정의하면서 note에
**"분자·분모 정의(EBITDA 기준) 명시 필수"**를 요구한다.
그런데 카드의 `key_metrics`는 `EBITDA/이자`로만 적혀 있어 다음이 확정되지 않는다.

| 미확정 요소 | 선택지 |
|---|---|
| 분자 | Adj. EBITDA / GAAP 영업이익 |
| 분모 | 순이자비용 / 총이자비용 |
| 기간 | 분기 연환산 / TTM |

이번 Run에는 H1 순이자비용 $1,176M, Q3 이자비용 가이던스 $860~940M, Q2 Adj. EBITDA 마진 59%가 제출되었으나,
**계산 기준이 확정되지 않아 임계 대비 판정을 낼 수 없었다.**
`06_portfolio.json`의 `company_kc_watch[KC-CRWV-3]`에 커버리지 조건을 "판정 불가"로 기록한 것이 그 결과다.

기준이 다르면 같은 분기 자료로도 커버리지 값이 달라진다. 기준 미확정 상태에서 임계 대비 판정을 산출하면
**근거 없는 수치가 생성된다.**

또한 카드의 `현 ~2.2x`는 카드 머리말이 이미 "Q2 2026 수치는 직전 세션 확인분 — 1차 자료 재대조가 Task 0"로 표기한 항목이며,
이번 Run에서도 재대조되지 않았다.

## 근거

- `config/kill_conditions.yaml#company.KC-CRWV-3` (note: 분자·분모 정의 명시 필수)
- `04_sector/neocloud.json#axis_view[debt_refinancing]`
- `04_sector/neocloud.json#axis_view[margin_trend]`
- `output/20260815_1408/06_portfolio.json#company_kc_watch[KC-CRWV-3]`

## 유의

- 지표의 **값이나 방향을 바꾸지 않는다.** 계산 기준이 미확정이라는 사실을 명시하는 주석 패치다.
- conclusion의 "진입 검토 조건 = FCF 흑자 전환 + 이자 커버리지 3x 이상 + 금리 경로 확정"은 그대로 유지된다.
  다만 **그 3x 판정 역시 동일한 기준 확정에 의존한다.**
- 기존 임계·값은 삭제하지 않고 보존한다(P9).
