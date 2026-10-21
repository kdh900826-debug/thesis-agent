# ThesisPatch — CRCL / catalysts[CLARITY Act 상원 경로] — 9/15 이후 상태(미확정) 병기

- **Run**: 20260925_1015 · as_of 2026-09-25 · skill `thesis-refine` (S7) · 후보 `tpc_09` (priority medium)
- **operation**: `amend` · **requires_human_approval**: true (F17) · 핵심 논거 역전: 아님
- **F20**: 카드 전문 86행 열람, before 출현 1회 확인, counts = [{"path": "catalysts", "n": 4}, {"path": "axes", "n": 8}, {"path": "key_metrics", "n": 7}, {"path": "risks", "n": 5}]

## diff

```diff
-   - "CLARITY Act 상원 경로"
+   # 2026-09-25 ThesisPatch(amend, run 20260925_1015) — 이전 항목: 'CLARITY Act 상원 경로'(P9 보존). 이전 서술은 경로만 적어 9/15 이후 상태가 촉매 목록에 반영되지 않았다. 근거가 grade 4·scope=sector이므로 일정 서술에만 쓰고 방향 판정 근거로 쓰지 않는다(P4·P6·P13). 항목 수 4개 불변(전문 86행 기준 계수).
+   - "CLARITY Act 상원 경로 — [확인 대상 · grade 4 · confirmed=false · scope=sector] 2차 매체 관측: 2026-09-15 클로처 부결 후 재의동의가 제출됐으나 2026-09-25 현재 재표결 일정 미확정, 11월 중간선거 이후 레임덕 세션 지연 가능성 지목. 미해결 쟁점에 이자부 스테이블코인 금지 조항 포함(c_20260925_CRCL_7). 1차 자료(senate.gov) 미확인 — 사실 확정이 아니다. [inference] 재의 경로가 남아 있어 kill_conditions_ref의 'CLARITY 최종 실패' 확정으로 읽지 않는다. 관측점: 재표결 일정 1차 확인, 이자부 스테이블코인 조항 문언"
```

## 왜

[fact] state/thesis_cards/CRCL.yaml 전문 86행을 읽었다(F20). 계수 — axes 8 / key_metrics 7 / catalysts 4 / risks 5 / kill_conditions_ref 6 / earnings_checkpoints.items 6 / version_history 12. yaml.safe_load 파싱 정상. before 문자열은 스크립트로 카드 내 출현 횟수 1회를 확인했다. [fact] 2차 매체(grade 4·confirmed=false·scope=sector)에 따르면 9/15 클로처 부결 후 재의동의에도 9/25 현재 재표결 일정이 없고 레임덕 세션 지연 가능성이 지목됐으며 이자부 스테이블코인 금지 조항이 미해결이다(c_20260925_CRCL_7). senate.gov 1차 확인은 불가했다. [fact] 카드 catalysts 항목은 '상원 경로'만 적어 현재 상태를 담지 않았다. after는 전 내용을 '확인 대상'으로 표기하고 사실로 확정하지 않는다(P4). [fact] scope=sector이므로 개별 종목 등급·방향 근거로 쓰지 않는다(P6·P13). [inference] 재의 경로가 남아 있어 'CLARITY 최종 실패' KC 충족으로 읽지 않는다. 핵심 논거 역전 아님.

## 근거 Claim

c_20260925_CRCL_7 — 출처 `output/20260925_1015/02_company/CRCL.json#claims`

## expected_after (F20 자동 대조)

```json
{
  "contains": [
    "CLARITY Act 상원 경로 — [확인 대상 · grade 4 · confirmed=false · scope=sector]",
    "c_20260925_CRCL_7"
  ],
  "not_contains": [
    "\"CLARITY Act 상원 경로\""
  ],
  "counts": [
    {
      "path": "catalysts",
      "n": 4
    },
    {
      "path": "axes",
      "n": 8
    },
    {
      "path": "key_metrics",
      "n": 7
    },
    {
      "path": "risks",
      "n": 5
    }
  ]
}
```

## dry-run (scratchpad 사본, 순차 적용)

- 원본 카드 before 출현 1회 · replace 1회 · yaml.safe_load 통과 · expected_after 통과 · 적용 후 계수 {"axes": 8, "key_metrics": 7, "catalysts": 4, "risks": 5} (version_history 15)
- 역순 적용에서도 오류 0건 — 다른 CRCL 패치와 before 영역 비중첩, 승인 순서 무관

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다.
