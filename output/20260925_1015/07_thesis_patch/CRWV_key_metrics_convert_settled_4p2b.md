# ThesisPatch — CRWV · key_metrics_convert_settled_4p2b

- as_of 2026-09-25 · run 20260925_1015 · operation **annotate** · requires_human_approval: true
- 카드 필드: `key_metrics[6] ('이자 커버리지' 항목) 말미 — 2026-09-20 산식 확정 주석 뒤` · basis_claims: c_20260925_CRWV_1, c_20260925_CRWV_2
- 출처 후보: orchestrator 지시(카드 조달·전환사채 금액 $3.7B→$4.2B 점검) — 06_portfolio tpc 목록 외 신규

## reason
[fact] 카드 내 '$3.7B'는 key_metrics '이자 커버리지' 항목의 2026-09-19 병기 주석 (4)에 1회만 등장하며, 이는 당시(가격결정 단계) 시점 기록이다. [fact] 2026-09-22 8-K로 옵션 $500M 전액 행사·결제 완료, 확정 규모 $4.2B·순수취금 $4,137.0M·capped call 실비 약 $566.2M(c_20260925_CRWV_1, grade 1). [inference:weak] 확정 규모 반영 TTM 정태 커버리지 약 2.21x(c_20260925_CRWV_2). [fact] 기록 시점 주석을 덮어쓰면 P9(오류 이력 삭제 금지·시점 기록 보존) 위반이므로 amend가 아닌 annotate로 말미에 확정치를 병기한다. [fact] 카드의 다른 조달 금액 서술(catalysts '차환·리파이낸싱 성공/실패', axes[funding_access] 라벨)에는 금액이 없어 정정 대상 없음.

## diff
```diff
- 확정 주체: 사람(P11, §9, U4)]"
+ 확정 주체: 사람(P11, §9, U4)] [ℹ️ 2026-09-25 전환사채 결제 확정 주석(run 20260925_1015) — 위 (4)의 '$3.7B/2.875%' 전제는 가격결정 단계 수치이며, 2026-09-22 8-K로 결제가 완료됐다: 추가매입옵션 $500M 전액 행사로 확정 발행규모 $4.2B(2.875%, 2033 만기), 순수취금 $4,137.0M, capped call 실비 약 $566.2M(c_20260925_CRWV_1, grade 1 fact). 확정 규모로 재계산한 연 추가이자 약 $120.75M을 TTM 분모에 정태 가산하면 약 2.21x(종전 $3.7B 가정 2.22x 대비 -0.01x, c_20260925_CRWV_2, inference:weak — 운용 이자수익·DDTL 5.5 이자·EBITDA 증가분 미반영 예시). 공식 산식(분기 연환산) 실측치는 Q3 2026 10-Q 대기. (4)의 원 서술은 당시 시점 기록으로 삭제하지 않고 보존한다(P9)]"
```

## expected_after (F20)
- contains: ['2026-09-25 전환사채 결제 확정 주석(run 20260925_1015)', '확정 발행규모 $4.2B(2.875%, 2033 만기)', '신규 전환사채 $3.7B/2.875%']
- not_contains: []
- counts: [{'path': 'key_metrics', 'n': 10}]

## 적용 순서
4건 모두 서로 다른 목록 항목을 건드리며 before 문자열이 겹치지 않는다 — 순서 무관(24개 순열 dry-run 통과).
