# ThesisPatch — CRWV / axes / decompose

- **Run**: 20260815_1408 · 2026-08-15
- **대상 필드**: `axes` (축 `debt_refinancing`)
- **operation**: `decompose` (P8)
- **승인 필요**: ✅ `requires_human_approval: true` — 자동 반영 금지
- **핵심 논거 역전 여부**: ❌ 아님

## 무엇을

한 축에 묶여 있던 **조달 접근성**과 **레버리지·커버리지**를 두 축으로 분해한다.

```diff
- - {id: debt_refinancing,  label: "부채·차환·이자 커버리지 (생존 조건)"}
+ # 2026-08-15 ThesisPatch(decompose, P8) — 이전 축: {id: debt_refinancing, label: "부채·차환·이자 커버리지 (생존 조건)"}
+ - {id: funding_access,     label: "조달 접근성 — 신규 차입 성사 여부·조달 스프레드·covenant 준수·미인출 한도"}
+ - {id: leverage_coverage,  label: "레버리지·커버리지 — 총부채 잔액·이자비용·이자 커버리지·부채상환 대비 영업활동현금흐름"}
```

## 왜

이번 Run에서 `debt_refinancing` 축은 `direction=diverge · dispersion=high`로 집계되었다.
그러나 그 분산은 **종목 간 상충이 아니라 CRWV 한 종목이 같은 축에 반대 방향 Delta 2건을 동시에 제출**한 결과다(intra-ticker).

| 다리 | 관측 |
|---|---|
| **strengthen** | $2.6B DDTL 5.5 오버서브스크라이브 클로징(8/10, SOFR+5.50%, Ba2/BB+, 만기 2031-09) · 가중평균 조달비용 1년간 약 300bp 하락(연 약 $1.1B 이자 절감 효과, CFO 직접 발언) · 전 DDTL covenant 준수(10-Q) · RCF 무차입, 잔여한도 $2.0B |
| **weaken** | 총부채 $21.37B→$35.07B(6개월 +$13.7B) · H1 순이자비용 $1,176M · Q3 이자비용 가이던스 $860~940M(Q2 실제 $640M 대비 QoQ +34~47%) · H1 부채상환 현금흐름 약 $6.2B가 H1 영업활동현금흐름 $3.7B를 초과한다는 10-Q 자체 위험요인 기재 |

두 다리가 상반되는 것은 사실 간 모순이 아니다. **축 정의가 상반 가능한 두 하위 개념을 한 축에 묶고 있어서**,
한 축의 단일 방향으로는 두 사실을 동시에 표현할 수 없는 것이다.

L2가 P8을 근거로 이 분해를 명시적으로 제안했고, 섹터 산출물은 이를 이번 사이클 섹터 분산의 **형식적 원인**으로 지목했다.
같은 형태의 상충이 NBIS `funding_capacity`에서도 독립적으로 관측되었다(→ `NBIS.md`).

## 분해 후 관측 항목

| 하위 축 | 관측 항목 | 이번 Run 방향 |
|---|---|---|
| `funding_access` | 신규 차입 성사 여부, 조달 스프레드(SOFR+bp), covenant 준수, 미인출 한도 | strengthen |
| `leverage_coverage` | 총부채 잔액, 분기 이자비용, 이자 커버리지, 부채상환 대비 영업활동현금흐름 | weaken |

## 근거

- `04_sector/neocloud.json#axis_view[debt_refinancing]`
- `04_sector/neocloud.json#interpretation.dispersion_cause_axes`
- `04_sector/neocloud.json#interpretation.dispersion_detail`
- `04_sector/neocloud.json#sector_unconfirmed[su_20260815_neocloud_05]`

> L4는 P17에 따라 `02_company` 산출물을 로드하지 않으므로 L2 Claim ID 대신 구조화 산출물의 경로 포인터를 근거로 기재한다.
> 위 항목의 원 근거는 CRWV 10-Q 및 실적 콜(grade 1~2)이다.

## 승인 시 영향

- KC-CRWV-3(이자 커버리지·차환) → `leverage_coverage` 축에 연결
- KC-CRWV-1(대형 고객 계약 훼손) → 기존대로 `customer_concentration` 축 유지
- `kill_conditions.yaml` 자체의 수정은 이 패치에 **포함되지 않는다**
- 기존 서술은 삭제하지 않고 주석으로 보존한다(P9)
