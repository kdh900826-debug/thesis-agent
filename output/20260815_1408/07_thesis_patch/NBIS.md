# ThesisPatch — NBIS / axes / decompose

- **Run**: 20260815_1408 · 2026-08-15
- **대상 필드**: `axes` (축 `funding_capacity`)
- **operation**: `decompose` (P8)
- **승인 필요**: ✅ `requires_human_approval: true` — 자동 반영 금지
- **핵심 논거 인접 여부**: ⚠️ **인접** — 아래 "자동 제안하지 않은 항목" 절 필독

## 무엇을

```diff
- - {id: funding_capacity,  label: "조달·희석 (현금 $8B, 선불금 $9B+, ATM)"}
+ # 2026-08-15 ThesisPatch(decompose, P8) — 이전 축: {id: funding_capacity, label: "조달·희석 (현금 $8B, 선불금 $9B+, ATM)"}
+ - {id: funding_access,     label: "조달 접근성 — 현금·고객 선불금·자산담보부 차입 성사와 조달 스프레드 (2026-07 최초 $775M, SOFR+2.50%)"}
+ - {id: leverage_burden,    label: "레버리지 부담 — 총부채·비유동부채 잔액과 희석(ATM·전환사채·선지급워런트)에서 이전된 레버리지 리스크"}
```

## 왜

`funding_capacity` 축은 `direction=diverge · dispersion=high`로 집계되었으나,
그 분산은 종목 간 이견이 아니라 **NBIS 한 종목이 같은 축에 양방향 Delta 2건을 제출**한 결과다(intra-ticker).

| Delta | 방향 | 관측 |
|---|---|---|
| `d_20260815_NBIS_03a` | strengthen | 2026-07월 **최초 자산담보부 대출 $775M, SOFR+2.50%** · 담보는 배치 GPU 및 투자적격 고객 계약 현금흐름 · $40B+ 커밋먼트 기반 추가 조달 계획 명시 |
| `d_20260815_NBIS_03b` | weaken | H1 중 전환사채 $4,337.5M + 선지급워런트 $2,000.0M 조달 · 비유동부채 $4,103.2M→**$8,499.0M** · 총부채 $7,836.6M→**$17,621.0M** |

L2는 이를 "조달 리스크의 소멸"이 아니라 **지분희석 리스크에서 레버리지 리스크로의 이전(risk_transfer)**으로 태깅했다.

현 축 라벨 `조달·희석`은 희석 축소를 개선으로 읽히게 한다.
그러나 이번 Run의 사실관계는 **희석이 줄어든 자리를 레버리지가 채운 구조**여서 단일 방향으로 표현할 수 없다.

섹터 산출물은 이 축이 CRWV `debt_refinancing`과 축 명칭만 다를 뿐 동일한 내부 상충 구조를 가지며,
**양사 L2가 서로 독립적으로 하위축 분해를 제안**했다고 기록했다.

## 분해 후 관측 항목

| 하위 축 | 관측 항목 | 이번 Run 방향 |
|---|---|---|
| `funding_access` | 현금 잔액, 고객 선불금 규모·비율, 신규 차입 성사 여부, 조달 스프레드 | strengthen |
| `leverage_burden` | 총부채·비유동부채 잔액, 전환사채·선지급워런트 잔액, ATM 잔여 주수, 이자비용 | weaken |

## ⚠️ 자동 제안하지 않은 항목 (사람 판단 필요)

카드의 thesis 문장은 **"순현금 재무구조 + 고객 선불금 기반 저희석 확장"**이다.
총부채 $7,836.6M→$17,621.0M(약 2.25배)는 **"순현금"이라는 서술의 재확인을 요구하는 관측**이다.

그러나 본 패치는 thesis 문장을 **수정하지 않는다.** 축을 두 개로 분해하기만 한다.
즉 이 패치는 핵심 논거를 뒤집지 않으며, 오히려 **뒤집힘 여부를 판정할 수 있는 관측 단위를 만드는 선행 조치**다.

thesis 문장("순현금 재무구조", "저희석 확장")의 정정 여부는 별도 사람 판단 사항으로 남긴다 — 본 Run에서 자동 제안하지 않았다.

## 근거

- `d_20260815_NBIS_03a` · `d_20260815_NBIS_03b` (04_sector/neocloud.json에 인용된 L2 Delta ID)
- `04_sector/neocloud.json#axis_view[funding_capacity]`
- `04_sector/neocloud.json#interpretation.dispersion_detail`
- `04_sector/neocloud.json#sector_unconfirmed[su_20260815_neocloud_05]`

## 승인 시 영향

- KC-NBIS-3(조달 조건 악화 — cash < $5B 또는 신규 조달 스프레드 +300bp) → `funding_access` 축에 연결
- 현금 $8,042.1M로 하한 상회. **스프레드 조건은 직전 조달 대비 비교 기준이 산출물에 없어 이번 Run에서 판정 불가**
- 기존 서술은 삭제하지 않고 주석으로 보존한다(P9)
