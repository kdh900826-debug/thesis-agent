# ThesisPatch — CRCL / axes[reserve_income] — 유통비용(파트너 분배) 구조 관측 병기

- **Run**: 20260925_1015 · as_of 2026-09-25 · skill `thesis-refine` (S7) · 후보 `tpc_06` (priority high)
- **operation**: `amend` · **requires_human_approval**: true (F17) · 핵심 논거 역전: 아님
- **F20**: 카드 전문 86행 열람, before 출현 1회 확인, counts = [{"path": "axes", "n": 8}, {"path": "key_metrics", "n": 7}, {"path": "catalysts", "n": 4}, {"path": "risks", "n": 5}]

## diff

```diff
-   - {id: reserve_income,    label: "Reserve Income·마진 (금리 직결)"}
+   # 2026-09-25 ThesisPatch(amend, run 20260925_1015) — 이전 라벨: 'Reserve Income·마진 (금리 직결)'(P9 보존). 이전 서술은 금리 한 변수만 명시해 유통비용(파트너 분배) 쪽 비용 구조가 축 밖에 놓여 있었다. 2026-09-22 8-K로 확인된 Binance 5년 재계약을 비용 구조 관측 항목으로 병기한다. 축 수 8개 불변(전문 86행 기준 계수).
+   - {id: reserve_income,    label: "Reserve Income·마진 (금리 직결 + 유통비용 구조). 유통비용 관측 — [fact · grade 1 · confirmed] Circle 자회사와 Binance의 USDC 프로모션 계약 5년 확장·갱신(8-K Item 8.01, 사건일 2026-09-17·제출 2026-09-22). 2024-11·2025-08 기존 계약을 대체하며, Circle은 Binance에 USDC 보유액의 일정 비율인 월간 인센티브 수수료를 지급한다 — 요율·산식·조기해지 트리거는 비공개. 동시에 Binance가 Class A 보통주 1,237,011주를 주당 $80.84(총 $1억)에 사모 인수, 종결 후 2년 락업(c_20260925_CRCL_1). [inference · medium] 파트너 분배 비용이 5년간 잔액 연동 구조로 재고정됐다. 요율 비공개로 마진 영향 크기는 산출 불가이며 과거 Binance向 비용 수치를 대입하지 않는다(c_20260925_CRCL_11). 같은 계약은 usdc_circulation_scale 축에는 유통 채널 고정으로 반대 부호로 들어간다 — 분배계약 본래 구조이며 모순이 아니다. [fact] Coinbase 분배계약은 Item 1.01/1.02 8-K 무공시 약 32일(c_20260925_CRCL_6) — 무공시는 무변경의 증명이 아니다(P5). KC-CRCL-3은 Coinbase 분배계약 정의이며 Binance 산입 여부는 config 결정 영역이다. 관측점: Q3'26 10-Q 계약 주석·유통비용 항목에서 Binance 인센티브 요율·반영 규모 및 Coinbase 분배조건 원문 확인"}
```

## 왜

[fact] state/thesis_cards/CRCL.yaml 전문 86행을 읽었다(F20). 계수 — axes 8 / key_metrics 7 / catalysts 4 / risks 5 / kill_conditions_ref 6 / earnings_checkpoints.items 6 / version_history 12. yaml.safe_load 파싱 정상. before 문자열은 스크립트로 카드 내 출현 횟수 1회를 확인했다. [fact] 2026-09-22 제출 8-K(사건일 09-17, grade 1)로 Binance와의 USDC 프로모션 계약이 5년 갱신됐고, 월간 인센티브 수수료가 USDC 보유액 비율에 연동되며 요율은 비공개다. $1억 사모(1,237,011주 @ $80.84, 2년 락업)가 동시 체결됐다(c_20260925_CRCL_1). [fact] 카드의 reserve_income 라벨은 '금리 직결'만 적어 분배비용 구조가 축 서술 밖에 있었다 — 이번 1차 자료가 이 서술을 불완전하게 만들었다. [inference·medium] 비용 구조는 5년간 고정됐으나 요율 비공개로 크기는 산출 불가하다(c_20260925_CRCL_11) — after는 크기를 단정하지 않는다. [fact] 04_sector/stablecoin.json axis_view[reserve_income]은 intra_ticker(Binance weaken vs Coinbase neutral)로 기록했다. [fact] 등급·방향 판정을 포함하지 않으며 thesis 핵심 논거 역전 패치가 아니다. KC-CRCL-3 분배자 범위 확장은 config 영역으로 이 패치에 포함하지 않는다.

## 근거 Claim

c_20260925_CRCL_1, c_20260925_CRCL_11, c_20260925_CRCL_6 — 출처 `output/20260925_1015/02_company/CRCL.json#claims`

## expected_after (F20 자동 대조)

```json
{
  "contains": [
    "label: \"Reserve Income·마진 (금리 직결 + 유통비용 구조)",
    "c_20260925_CRCL_1",
    "요율·산식·조기해지 트리거는 비공개",
    "Q3'26 10-Q 계약 주석"
  ],
  "not_contains": [
    "label: \"Reserve Income·마진 (금리 직결)\"}"
  ],
  "counts": [
    {
      "path": "axes",
      "n": 8
    },
    {
      "path": "key_metrics",
      "n": 7
    },
    {
      "path": "catalysts",
      "n": 4
    },
    {
      "path": "risks",
      "n": 5
    }
  ]
}
```

## dry-run (scratchpad 사본, 순차 적용)

- 원본 카드 before 출현 1회 · replace 1회 · yaml.safe_load 통과 · expected_after 통과 · 적용 후 계수 {"axes": 8, "key_metrics": 7, "catalysts": 4, "risks": 5} (version_history 13)
- 역순 적용에서도 오류 0건 — 다른 CRCL 패치와 before 영역 비중첩, 승인 순서 무관

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다.
