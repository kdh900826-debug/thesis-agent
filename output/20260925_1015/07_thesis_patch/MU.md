# ThesisPatch Set — MU (run 20260925_1015)

- **as_of** 2026-09-25 · 스킬 `thesis-refine`(S7) · 패치 **2건** (L4 tpc_03을 필드별 2건으로 분리), 제외 tpc_04 1건 + 참조 1건
- **카드 전문 확인(F20)**: 75행 전문 열람. axes 7 / key_metrics 7 / catalysts 4 / risks 4 / kill_conditions_ref 5 / earnings_checkpoints.items 7 / version_history 6
- **승인**: 2건 모두 `requires_human_approval: true`(F17). `state/` 미수정, approvals.py 미실행.
- **적용 순서**: 순서 무관(dry-run 양방향 PASS). 권장 A → B.

| 패치 | 필드 | op | 요약 | 기대 counts |
|---|---|---|---|---|
| A `MU_axes_ip_litigation_itc_institution` | axes | amend | ITC 337-TA-1523 조사개시(09-24, grade 1) + CDCA·D.Del(grade 4 확인 대상)·CAFC 관측점 ⑤~⑧ | axes 7 |
| B `MU_earnings_checkpoints_litigation_disclosure` | earnings_checkpoints | amend | 9/30 실적·후속 10-K 소송 기술 체크포인트 추가 | items 8, axes 7 |

## 제외

- **tpc_04 (annotate — SK하이닉스 Netlist 라이선스 상태 정정)** — dropped: [fact] 카드 전문 75행에서 licens·라이선스·라이센스·hynix·하이닉스를 검색한 결과 SK하이닉스 언급은 catalysts의 'SK하이닉스·삼성 실적 (peer 멀티플)' 1건뿐이며 'SK하이닉스 라이선스 보유' 전제 문구는 존재하지 않는다. L4가 지정한 조건('카드에 해당 전제가 있는 경우에 한함')에 따라 패치를 생성하지 않았다. [fact] 섹터 기록(esc_20260925_memory_04)의 '2021-04 5년 계약 2026-04 만료 후 갱신 1차 미확인' 상태는 카드와 충돌하지 않는다.
- **Samsung-Netlist 합의(2026-08-04)·ITC Cooperation Agreement 반영** — dropped: [fact] 04_sector/memory.json의 참조 층위(ref_netlist_samsung_settlement_20260925, Netlist 8-K)이며 02_company Claim이 아니다 — basis_claims 필수 규칙 미충족. [fact] c_20260925_MU_3의 Netlist CEO 인용이 'Samsung agreement'를 언급하나 협력계약 조항 자체를 기술하지 않는다. [inference · moderate] 재검토 조건: L2가 해당 8-K를 MU Claim으로 적재하면 ip_litigation_risk 관측점 후보가 된다.
- **MU 회사 KC 신설(ITC 최종판정·배제명령)** — not_generated — human decision: [fact] kill_conditions.yaml#company에 MU 전용 KC 4회 연속 미정의. 임계+결과 쌍 확정은 사람 영역(P11·CLAUDE.md §9)이며 config는 사용자 직접 편집 영역이다 — add_kc를 만들지 않고 기록만 한다.

## 지시문 불일치

[fact] 지시문은 'CDCA 답변시한 10/1'로 기술했으나 c_20260925_MU_5 기준 10/1은 D.Del 1:26-cv-01014의 Netlist 답변시한이며 CDCA 연장 후 시한은 미특정이다 — 패치는 Claim 기준으로 작성했다.

> 이 패치는 제안이며 자동 반영되지 않는다(F17).
