# ThesisPatch — CRWV · risks_cross_default_covenant

- as_of 2026-09-25 · run 20260925_1015 · operation **annotate** · requires_human_approval: true
- 카드 필드: `risks[0] ('부채 리스크 #1' 항목) — kill_conditions_ref는 KC ID 문자열 목록(로드 키)이라 주석 삽입 시 KC 참조 파싱을 훼손할 수 있어 대상에서 제외` · basis_claims: c_20260925_CRWV_1, c_20260919_CRWV_6
- 출처 후보: output/20260925_1015/06_portfolio.json#thesis_patch_candidates[tpc_02]

## reason
[fact] 2026-09-22 8-K(Items 1.01/3.02/8.01/9.01)가 $4.2B 2.875% 2033 전환사채 Indenture의 교차부도 트리거('$200M 또는 LTM EBITDA 5% 중 큰 금액', 30일 유예)를 최초 1차 공시했다(c_20260925_CRWV_1, grade 1, confirmed). [fact] L2는 이를 noise_filter#CRWV promote_if 'covenant 관련 공시'로 승격했고, KC-CRWV-3 refinancing_failure_or_covenant_breach 서브 조건의 최초 정량 기준으로 기록했다(02_company/CRWV.json notes). [fact] 카드에 covenant 문턱 서술은 없었다(전문 계수: '교차부도' 0회, 'covenant'는 axes[funding_access] 라벨 1회). [inference:weak] 문턱 추정 약 $220M은 TTM Adj. EBITDA(c_20260919_CRWV_6)의 산술 파생이며 Indenture EBITDA 정의 미확인. [fact] 배치 판단: kill_conditions_ref는 KC ID 로드 목록이라 주석을 넣지 않고, 부채·조달 위험 항목인 risks[0]에 병기했다. KC 정의 문언 변경은 config 영역(§9).

## diff
```diff
-   - "부채 리스크 #1 — CapEx 상향($35-39B)이 매출 상향폭 초과 시 조달 의존 심화"
+   - "부채 리스크 #1 — CapEx 상향($35-39B)이 매출 상향폭 초과 시 조달 의존 심화 [ℹ️ 2026-09-25 교차부도 문턱 주석(run 20260925_1015) — 2026-09-22 8-K(2033 만기 2.875% 전환사채 $4.2B Indenture, c_20260925_CRWV_1, grade 1)가 event of default 중 교차부도(cross-default) 트리거를 처음 1차 공시했다: CoreWeave 또는 significant subsidiaries(합산 포함)의 차입채무 중 원금 '$200M 또는 LTM EBITDA의 5% 중 큰 금액' 이상에 대한 디폴트 발생 시 30일 유예 후 교차부도 사유. 이는 KC-CRWV-3 '차환 실패·covenant 위반' 서브 조건의 최초 정량 관측 기준이다. 참고 산식(inference:weak): TTM Adj. EBITDA $4,403M(c_20260919_CRWV_6) 대입 시 5% ≈ $220M으로 현재 문턱은 약 $220M이나, Indenture상 LTM EBITDA 정의와 회사 Adj. EBITDA의 동일 여부는 미확인. 이번 창 실제 디폴트·트리거 사건 없음. KC 문언(config/kill_conditions.yaml) 반영 여부는 사용자 편집 영역 — 에이전트 미수정. 기존 서술은 삭제하지 않고 병기만 한다(P9)]"
```

## expected_after (F20)
- contains: ['2026-09-25 교차부도 문턱 주석(run 20260925_1015)', "'$200M 또는 LTM EBITDA의 5% 중 큰 금액'"]
- not_contains: []
- counts: [{'path': 'risks', 'n': 5}, {'path': 'kill_conditions_ref', 'n': 4}]

## 적용 순서
4건 모두 서로 다른 목록 항목을 건드리며 before 문자열이 겹치지 않는다 — 순서 무관(24개 순열 dry-run 통과).
