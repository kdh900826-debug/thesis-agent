# ThesisPatch — CRCL / earnings_checkpoints / amend (게이트 소멸)

- **Run**: 20260815_1408 · 2026-08-15
- **대상 필드**: `earnings_checkpoints.date`
- **operation**: `amend`
- **승인 필요**: ✅ `requires_human_approval: true`
- **핵심 논거 역전 여부**: ❌ 아님 (사실 오류 정정)

## 무엇을

```diff
  earnings_checkpoints:
-   date: "2026-08-18"
+   # 2026-08-15 ThesisPatch(amend) — 이전 값: date: "2026-08-18". Q2 실적은 2026-08-05에 이미 발표되어 해당 게이트는 소멸했다.
+   # 차기 게이트(Q3)는 회사 IR 공식 공지 확인 전까지 null을 유지한다 — 애그리게이터 자동 추정일은 등급과 무관하게 판정 근거로 사용할 수 없다(F1).
+   date: null
```

## 왜

**카드의 차기 실적 게이트가 이미 경과한 날짜를 가리키고 있다.**

- CRCL Q2 실적은 **2026-08-05에 이미 발표**되었다 — 섹터 산출물에 CRCL CFO·CEO의 8/5 실적 콜 발언이 grade 2·confirmed로 복수 인용되어 있다.
- `su_stablecoin_08`이 명시적으로 기록했다: "CRCL은 Q2 실적이 8/5에 이미 발표되어 기존 게이트(8/18)가 소멸했고, 8/18에 별도 회사 이벤트가 있는지는 미확인"
- **2026-08-18은 실적일이 아니다.** 2023-08-18 발효된 Circle-Coinbase 분배계약의 **3년 자동 갱신 예정일**이며,
  이는 KC-CRCL-3(분배 계약 변경)의 관측 항목이지 실적 체크포인트가 아니다(`c_20260815_COIN_004`, grade 2, confirmed).

## 왜 추정일로 채우지 않는가

COIN·HOOD의 Q3 발표일은 애그리게이터 추정치만 존재하고 회사 IR 공식 공지는 확인되지 않았다.
**애그리게이터 자동 추정 라벨은 등급과 무관하게 판정 근거로 사용할 수 없다(F1).**

따라서 차기 게이트를 임의의 추정일로 채우지 않고 `null`로 둔다 — 같은 이유로 NBIS·CRWV 카드의
`earnings_checkpoints.date`도 이미 `null`이다.

## 근거

- `04_sector/stablecoin.json#sector_unconfirmed[su_stablecoin_08]`
- `04_sector/stablecoin.json#sector_unconfirmed[su_stablecoin_04]`
- `c_20260815_CRCL_008` · `c_20260815_CRCL_012` · `c_20260815_COIN_004`

## 관련 문서

| 문서 | 내용 |
|---|---|
| `CRCL_catalyst_gate.md` | 같은 8/18 게이트가 `catalysts`에도 중복 기재되어 있어 별도 패치로 분리 (자동 적용은 패치당 문자열 1건 치환) |
| **`CRCL_escalation_usdc_circulation.md`** | ⚠️ CRCL 카드의 **핵심 전제**(USDC 유통량 축소 추세)와 1차 공시의 상충 — **자동 제안 대상이 아니어서 승인 큐에 등재하지 않았다** |
