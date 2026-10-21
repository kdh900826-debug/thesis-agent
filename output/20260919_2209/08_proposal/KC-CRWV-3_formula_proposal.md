# 제안 — config/kill_conditions.yaml#company.KC-CRWV-3 산식 명문화 (사용자 편집 영역, 에이전트 미수정)

- 근거: 2026-09-20 사용자 결정(ThesisPatch ap_20260920_0804_thesis_patch_crwv_coverage_period_adopted 적용 완료)
- 현재 note "분자·분모 정의(EBITDA 기준) 명시 필수"는 미확정 상태 문언이므로 확정 산식으로 교체 제안
- 임계(1.5x 경고 / 1.0x 발동)·consequence는 변경 없음

## 제안 diff (라인 222 · 223)
```yaml
# before
      - {metric: interest_coverage, operator: "<", threshold: 1.5, unit: "x", severity: warning, note: "경고 단계. 분자·분모 정의(EBITDA 기준) 명시 필수"}
      - {metric: interest_coverage, operator: "<", threshold: 1.0, unit: "x", severity: kill, note: "발동 단계 (v1 승계)"}
# after
      - {metric: interest_coverage, operator: "<", threshold: 1.5, unit: "x", severity: warning, note: "경고 단계. 산식(2026-09-20 사용자 확정) = Adj. EBITDA ÷ Interest expense, net · 분기 연환산(최근 분기 비율). 출처: 8-K Ex 99.2 분기 조정표. TTM은 참고치. 현재 2.36x(Q2'26)"}
      - {metric: interest_coverage, operator: "<", threshold: 1.0, unit: "x", severity: kill, note: "발동 단계 (v1 승계). 산식은 경고 단계와 동일"}
```
- 부수 갱신 권고: 라인 218 주석 "(현 ~2.2x는 재대조 대사 대기 u_001)" → 재대조 완료(Q1'26 2.16x 시점값, 현 Q2'26 2.36x)로 교체
- kc_eval.py는 company KC를 자동 판정하지 않으므로(L2 실측 → arbiter 판정) 스크립트 변경 불필요

---
**2026-09-20 적용 완료(사용자 지시)** — 라인 218·222·223 반영, 백업 config/backup/kill_conditions_20260920_pre_KC-CRWV-3_formula.yaml, YAML 파싱·pytest 29건 통과.
