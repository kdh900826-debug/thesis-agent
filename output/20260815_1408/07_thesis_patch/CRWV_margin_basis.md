# ThesisPatch — CRWV / axes / annotate (margin_trend 기준 기간)

- **Run**: 20260815_1408 · 2026-08-15
- **대상 필드**: `axes` (축 `margin_trend`)
- **operation**: `annotate`
- **승인 필요**: ✅ `requires_human_approval: true`
- **핵심 논거 역전 여부**: ❌ 아님

## 무엇을

```diff
- - {id: margin_trend,      label: "Adj. EBITDA 마진 추세 (59% 하락 추세 ⚠️갱신)"}
+ - {id: margin_trend,      label: "Adj. EBITDA 마진 추세 — ⚠️기준 기간 명시 필요. YoY 기준: Q2 59%(전년 62%)·H1 57%(전년 62%)로 압축 / 시퀀셜 기준: Q1 약 56%→Q2 59%로 개선. 기준에 따라 방향이 반대이므로 축 판정 시 기준을 먼저 고정한다 ⚠️갱신"}
```

## 왜 — 같은 자료로 반대 방향 판정이 나온다

| 기준 | 관측 | 방향 |
|---|---|---|
| **YoY** | Q2 59%(전년 62%) · H1 누적 57%(전년 62%) | 압축 (weaken) |
| **시퀀셜** | Q1 약 56% → Q2 59%, CFO는 조정영업이익률의 순차 확대를 언급 | 개선 |

카드의 현 라벨 `(59% 하락 추세)`는 **어느 기준의 추세인지를 명시하지 않는다.**
따라서 동일한 1차 자료에서 상반된 축 판정이 가능하고, 축 자체가 재현 가능한 판정 단위로 기능하지 못한다.

L2가 축 정의(YoY 기준 vs 시퀀셜 기준)를 카드에 명시할 것을 thesis-refine 검토 후보로 제안했다.

섹터 산출물은 여기에 한 겹을 더한다 — NBIS `margin_transition`(적자→흑자 전환 국면의 마진 **수준** 개선)과
CRWV `margin_trend`(고마진 상태에서의 YoY **압축**)는 표면상 정반대이나 축 정의와 사업 단계가 달라
섹터 마진 방향으로 통합 해석하는 것은 **착시**라고 판정했고, 축 정의 표준화 필요를 `su_20260815_neocloud_05`로 이관했다.

## 근거

- `04_sector/neocloud.json#axis_view[margin_trend]`
- `04_sector/neocloud.json#axis_view[margin_transition]`
- `04_sector/neocloud.json#sector_unconfirmed[su_20260815_neocloud_05]`

## 유의

- 축의 방향을 뒤집지 않는다. 두 기준의 값을 모두 기재해 **기준 선택을 명시적 결정 사항으로 만드는** 주석 패치다.
- 이번 Run의 축 판정(weaken, YoY 기준)은 **변경하지 않는다** — 하위 계층 판정의 소급 수정은 금지된다(P13).
- 기존 수치(59%)는 삭제하지 않고 양 기준의 값을 병기한다(P9).
