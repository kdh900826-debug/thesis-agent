# ThesisPatch — MU / axes — axes[ip_litigation_risk] — 관측점 ⑨~⑫ 추가(HBM 2차 ITC 제소, 337-TA-1523 개시일 09-23/09-24 병기, 병행 절차, 9/30 실적 무언급) / amend

- **Run**: 20261001_0900 · as_of 2026-10-01 · 스킬 `thesis-refine`(S7) · L4 cio-portfolio 절차 4
- **patch_id**: `MU_axes_ip_litigation_hbm_second_itc` · priority: high
- **대상 필드**: `axes` — axes[ip_litigation_risk] — 관측점 ⑨~⑫ 추가(HBM 2차 ITC 제소, 337-TA-1523 개시일 09-23/09-24 병기, 병행 절차, 9/30 실적 무언급)
- **승인 필요**: 예 (requires_human_approval: true, F17) / **핵심 논거 역전**: 아니오
- **선행 인간 결정 의존**: 없음
- **적용 순서**: 순서 무관 — MU 5건(key_metrics / earnings_checkpoints / catalysts / risks / axes)은 서로 다른 행을 치환하고 counts는 각자 필드만 검사한다(드라이런 단독·순차 모두 통과). 권장: MU_key_metrics → MU_earnings_checkpoints → MU_catalysts → MU_risks → MU_axes
- **사전 확인(F20)**: `state/thesis_cards/MU.yaml` 전문 80행 열람, before 출현 1회 확인. 현재 계수 axes 7 / key_metrics 7 / catalysts 4 / risks 4 / kill_conditions_ref 5 / version_history 8 / earnings_checkpoints.items 8
- **expected_after**: counts [{"path": "axes", "n": 7}] · contains 5건 · not_contains 1건

## diff

```diff
--- state/thesis_cards/MU.yaml (before)
+++ state/thesis_cards/MU.yaml (after 제안)
-/ 2026-09-30 FY26 Q4 실적 발표·콜의 소송 기술(earnings_checkpoints 참조)"}
+/ 2026-09-30 FY26 Q4 실적 발표·콜의 소송 기술(earnings_checkpoints 참조). 2026-10-01 관측점 갱신(ThesisPatch amend, run 20261001_0900) — ⑨ [fact · grade 1 · confirmed] Netlist가 2026-09-29 Micron을 상대로 신규 2차 ITC 제소를 제기했다 — 주장 특허 US 12,308,087·12,646,537, 대상 제품 Micron HBM3E·HBM4·HBM4E, 배제명령·중지명령 청구. 337-TA-1523(DDR5 RDIMM·MRDIMM)과 별개 사건이며 소송 전선이 처음으로 HBM 자체로 확장됐다(c_20261001_MU_10 — Netlist 보도자료 + 5개 이상 독립매체 삼각검증). Nvidia·Broadcom·Google은 다운스트림 고객으로 거명됐으며 정식 피조사자 구성은 자료 간 불일치로 미확정이다(04_sector esc_20261001_memory_02). institution(조사개시)은 미확정이다(P7). ⑩ [확인 대상 · grade 3 · confirmed=false · 단독 근거 부적격(P4)] 337-TA-1523 조사개시 표결일을 2026-09-23으로 표기하는 자료(매체 1건 + usitc.gov 보도자료 URL 패턴 er0923)가 포착됐다. ⑤의 2026-09-24와 불일치하나 어느 쪽도 정정하지 않고 병기한다(P9, c_20261001_MU_11). usitc.gov 원문은 다시 403. ⑪ [확인 대상 · grade 4 · confirmed=false · 단독 근거 부적격(P4)] CDCA 8:26-cv-02167 배정판사 John W. Holcomb 조회. D.Del 1:26-cv-01014 답변시한(2026-10-01)은 as_of와 겹쳐 답변 제출 여부 미반영. CAFC 2025-1936 신규 진전 보도 없음(c_20261001_MU_13). ⑫ [fact · grade 1 · confirmed] 2026-09-30 실적 보도자료·준비발언·콜 Q&A 전사에서 Netlist·ITC·litigation·patent 언급 0건 — 무언급은 리스크 해소 근거가 아니다(P5, c_20261001_MU_9). ⚠️⑨는 제소 단계다 — 제소 ≠ 조사개시 ≠ 위반 판정 ≠ 배제명령 ≠ 매출 영향(P5·P7). 법률 절차이며 매출·마진·현금흐름·가이던스 수치가 아니므로 등급 상향 근거로 쓸 수 없다(P2). [inference · moderate] L2·arbiter는 소송 대상이 thesis 핵심 제품(HBM)으로 확장됐다는 이유로 이 축을 2회 연속 weaken으로 표기했다. 추적점(재갱신): HBM 2차 제소 institution 표결·공고문상 피조사자 구성 / 337-TA-1523 조사개시일 확정·ALJ 배정·target date / D.Del 1:26-cv-01014 2026-10-01 답변 및 §1659 정지 신청 여부(grade 4 확인 대상) / CDCA 8:26-cv-02167 답변 내용(grade 4 확인 대상) / CAFC 2025-1936 선고 / FY26 10-K 소송·우발부채 각주"}
```

## 왜

[fact] state/thesis_cards/MU.yaml 전문 80행을 읽고 yaml.safe_load로 목록형 필드를 실제 계수했다 — axes 7 / key_metrics 7 / catalysts 4 / risks 4 / kill_conditions_ref 5 / earnings_checkpoints.items 8 / version_history 8(F20). [fact] ip_litigation_risk 라벨의 최신 관측점(⑤~⑧, 2026-09-25)은 소송 대상을 DDR5 RDIMM·MRDIMM(337-TA-1523)로만 기록하고 있으나 2026-09-29 Netlist가 HBM3E·HBM4·HBM4E를 직접 겨냥한 별개 2차 ITC 제소를 제기했다(c_20261001_MU_10, grade1·confirmed) — 축 서술의 소송 범위가 부정확해졌다. [fact] 337-TA-1523 조사개시일 09-23 표기 자료(c_11, grade3·confirmed=false)는 ⑤의 09-24를 정정하지 않고 병기한다(P9). [fact] 본 패치는 기존 라벨 종결부(추적점 마지막 항목 + 닫는 따옴표·중괄호)만을 before로 잡아 그 뒤에 ⑨~⑫를 덧붙인다 — 라벨 앞부분(2026-09-05 원문, ①~⑧)은 문자 그대로 보존된다(P9). 축 수 7개 불변. [fact] 축 추가·분해가 아니라 기존 축의 관측점 갱신이므로 axis_naming_standardization 의존 플래그를 부착하지 않았다.

**역전 판정 주석**: [inference · moderate] HBM 대상 제소는 thesis 핵심 제품을 겨냥하나 현재 제소 단계이고 매출·마진 영향 수치가 없다 — 축 관측점 갱신이며 핵심 논거 역전 패치가 아니다. 다만 institution·배제명령 단계로 진전되면 thesis 본문 재검토가 필요할 수 있다는 점을 사람 확인 사항으로 남긴다.

## 근거 Claim

c_20261001_MU_9, c_20261001_MU_10, c_20261001_MU_11, c_20261001_MU_13

[fact] c_9·c_10 grade1·confirmed — 사실 단정. c_11(grade3)·c_13(grade4) confirmed=false — 확인 대상으로만 기재(P4). 03_signal/MU.json ip_litigation_risk supporting_claims 4건과 동일.

출처: `output/20261001_0900/03_signal/MU.json#claims,thesis_delta_summary · output/20261001_0900/04_sector/memory.json#axis_view,earnings_cycle_context · output/20261001_0900/03_input/arbiter_MU.json(수치·문구 대조)`

**F20 주석**: [fact] 카드 전문 80행 중 28행(ip_litigation_risk)은 단일 행 1만자 이상이다 — 전문을 읽은 뒤 라벨 종결부 문자열('/ 2026-09-30 FY26 Q4 실적 발표·콜의 소송 기술(earnings_checkpoints 참조)"}')이 카드 내 1회 출현함을 스크립트로 확인하고 이를 before로 사용했다(부분 문자열이지만 원문 그대로의 복사). contains 3·4번째는 보존 구간(⑤·②) 존치를 검증하고, not_contains는 원 종결부가 '참조). 2026-10-01 …'로 이어져 사라짐을 검증한다.

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
