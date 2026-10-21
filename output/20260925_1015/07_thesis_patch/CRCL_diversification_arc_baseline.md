# ThesisPatch — CRCL / axes[diversification] — Arc 메인넷 첫 주 기준선 관측 추가

- **Run**: 20260925_1015 · as_of 2026-09-25 · skill `thesis-refine` (S7) · 후보 `tpc_08` (priority low)
- **operation**: `annotate` · **requires_human_approval**: true (F17) · 핵심 논거 역전: 아님
- **F20**: 카드 전문 86행 열람, before 출현 1회 확인, counts = [{"path": "axes", "n": 8}, {"path": "key_metrics", "n": 7}, {"path": "catalysts", "n": 4}, {"path": "risks", "n": 5}]

## diff

```diff
- 관측점: 거래 종결 공시(최대 15개월 내) 및 종결 후 비이자 매출 비중 변화"}
+ 관측점: 거래 종결 공시(최대 15개월 내) 및 종결 후 비이자 매출 비중 변화. (c) Arc 메인넷 기준선(2026-09-25 ThesisPatch annotate, run 20260925_1015 — 기존 (a)(b) 서술 보존, P9): [fact · grade 2 · 경영진 직접 발언] CEO Allaire 2026-09-23 Autonomous Research 심포지엄 발언 — Arc 메인넷(2026-09-16 출시) 첫 주 네트워크상 가치 약 $1B 근접, USDC 기준 거래 수수료 약 $0.5M, FDV 약 $3B, Circle 지분 25%. 본인이 출시 시점 버스트로 규정하고 지속성을 유보했다(c_20260925_CRCL_3). [삼각검증 전용 · grade 4 · confirmed=false · 단독 근거 부적격(P4)] 2차 매체 온체인 집계(DeFi TVL 약 $348M·스테이블코인 잔액 약 $630M 등)는 측정 계열이 달라 위 발언과 합산·대체하지 않는다(c_20260925_CRCL_4). [inference] 네트워크 거래 수수료는 Circle 재무제표 매출과 동일하지 않다 — P7상 이행 개시 단계이며 매출 인식 수치는 미공시. 관측점: 2주 차 이후 지표 지속 여부, Q3'26 재무제표 내 Arc 관련 매출·수수료 인식 여부"}
```

## 왜

[fact] state/thesis_cards/CRCL.yaml 전문 86행을 읽었다(F20). 계수 — axes 8 / key_metrics 7 / catalysts 4 / risks 5 / kill_conditions_ref 6 / earnings_checkpoints.items 6 / version_history 12. yaml.safe_load 파싱 정상. before 문자열은 스크립트로 카드 내 출현 횟수 1회를 확인했다. [fact] CEO Allaire가 2026-09-23 Arc 첫 주 지표(네트워크상 가치 약 $1B 근접, 수수료 약 $0.5M, FDV $3B, Circle 25% 지분)를 직접 언급했고 스스로 지속성을 유보했다 — grade 2(c_20260925_CRCL_3). [fact] 온체인 수치(c_20260925_CRCL_4)는 grade 4·confirmed=false이고 측정 계열이 달라 삼각검증 전용 표기로만 기입했다(P4). [fact] 카드 diversification 축은 Arc 출시 후 지표가 없었다 — 기존 (a)(b) 서술은 그대로 두고 (c)만 덧붙인다. [inference] 네트워크 수수료는 회사 매출이 아니며 P7상 매출 인식 이전이다 — 상향 근거로 쓸 수 없다(P2). 핵심 논거 역전 아님.

## 근거 Claim

c_20260925_CRCL_3, c_20260925_CRCL_4 — 출처 `output/20260925_1015/02_company/CRCL.json#claims`

## expected_after (F20 자동 대조)

```json
{
  "contains": [
    "(c) Arc 메인넷 기준선",
    "c_20260925_CRCL_3",
    "삼각검증 전용 · grade 4 · confirmed=false",
    "Tazapay Pte. Ltd."
  ],
  "not_contains": [
    "비이자 매출 비중 변화\"}"
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

- 원본 카드 before 출현 1회 · replace 1회 · yaml.safe_load 통과 · expected_after 통과 · 적용 후 계수 {"axes": 8, "key_metrics": 7, "catalysts": 4, "risks": 5} (version_history 14)
- 역순 적용에서도 오류 0건 — 다른 CRCL 패치와 before 영역 비중첩, 승인 순서 무관

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 `approvals.py`가 수행한다.
