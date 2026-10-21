# ThesisPatch — MU / axes / amend

- **Run**: 20260905_0618 · 2026-09-05T06:18 (L4 병행 `thesis-refine`)
- **대상 필드**: `axes` (expected_after.counts: axes=6 — F20)
- **operation**: `amend`
- **승인 필요**: ✅ (requires_human_approval: true, F17) / **핵심 논거 역전**: ❌ 아니오
- **사전 확인**: 대상 카드 전문 열람 후 before 문자열의 카드 원문 일치 확인 ✅ (F20 — 부분 읽기 기반 '부재' 판정 없음)

## diff

```diff
--- state/thesis_cards/MU.yaml (before)
+++ state/thesis_cards/MU.yaml (after 제안)
@@ -1,0 +2,2 @@
+  # 2026-09-05 ThesisPatch(amend, run 20260905_0618) — 신규 축 추가. 축 수 5 → 6(전문 기준 계수). 직전 run(20260820)과 이번 run 2회 연속 계류된 L2 axis_proposal이며 L3(memory)는 본 재료를 MU 단독 귀착으로 판정했다. 관측 단위 신설이며 방향(강화·훼손) 판정은 포함하지 않는다.
+  - {id: ip_litigation_risk, label: "특허소송 리스크 — Netlist가 2026-08-12 ITC에 Micron 포함 4개사를 상대로 특허 4건(US 10,025,731 / 10,217,523 / 12,373,366 / 12,675,407, DDR5 RDIMM·MRDIMM) 침해 제소하며 배제명령·중지명령 청구, 별도로 캘리포니아중부지법(CDCA)에 Micron 단독 제소(특허 2건). 배경: 2026-02-20 CAFC 별건 판결로 $445M 배상 확정 이력. ITC 배제명령은 미국向 수입·매출 인식에 직접 작용하는 경로로 hbm_demand·sca_defense·china_supply 어디에도 매핑되지 않는 독립 리스크다. 2026-09-05 기준 ITC 조사개시(institution) 공지는 확인되지 않았으며 자료 부재는 반증이 아니다(P5). 추적점: ITC institution 투표, CDCA 답변 시한(2026-09-10, grade 4 미확인)"}
```

## 왜

[fact] Netlist는 2026-08-12 ITC 제소(Micron 포함 4개사, 특허 4건, 배제명령·중지명령 청구)와 CDCA 단독 제소(특허 2건)를 동시에 제기했다(c_20260905_MU_03, grade 1 — 원고 측 공식 보도자료). [fact] 카드 axes는 전문 기준 5개(hbm_demand / sca_defense / cycle_position / china_supply / valuation_paradox)이며 특허소송發 수입·매출 인식 리스크가 매핑되는 축이 없다. [fact] 2026-09-05 기준 ITC 조사개시 공지는 확인되지 않았고(c_20260905_MU_05, grade 1 부재 확인), CDCA 답변 시한 2026-09-10은 grade 4·confirmed=false다(c_20260905_MU_04). [inference:strong] 매핑 대상 축이 없으면 후속 Delta가 인접 축(예: china_supply)에 잘못 흡수되거나 유실된다 — 축 신설이 정합적 조치다. 실제로 이번 run의 china_supply Delta는 Apple 소싱 건만 담고 있어 소송 경로가 어디에도 적재되지 않았다. [fact] 축 수 5 → 6. 본 패치는 축의 존재만 신설하고 방향 판정을 부여하지 않으며, 등급 변경 근거로 사용될 수 없다(P2).

**역전 판정 주석**: [fact] thesis 본문('HBM 수요가 AI CapEx에 직접 연동되는 구간에서 SCA·take-or-pay·최소가격 보장 구조를 통해...')은 한 글자도 바꾸지 않는다. 관측 축 1개 신설이며 기존 축의 판정을 뒤집지 않으므로 P8 분해 대상도 아니다.

**후속 주의**: [fact] 승인 시 thesis-delta는 이 축에 Netlist 관련 Delta를 매핑할 수 있게 된다. [fact] ITC institution 여부는 통상 제소 후 30일 내외에 결정되므로 2026-09월 중순 전후 재확인이 필요하다. [fact] 본 축에는 KC 정량 임계가 없다 — 임계 신설은 사용자 영역이며 에이전트는 제안만 한다(P11 · CLAUDE.md §9).

## 근거 Claim

c_20260905_MU_03, c_20260905_MU_04, c_20260905_MU_05

출처: `output/20260905_0618/02_company/MU.json#axis_proposals[ip_litigation_risk] · #claims[c_20260905_MU_03/04/05]`

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 approvals.py가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
