# ThesisPatch — CRCL / kill_conditions_ref / amend (KC-CRCL-4 참조 추가)

- **Run**: 20260816_0000 · 2026-08-16 (검토 세션)
- **대상 필드**: `kill_conditions_ref`
- **operation**: `amend`
- **승인 필요**: ✅ `requires_human_approval: true`
- **핵심 논거 역전 여부**: ❌ 아님 — KC 신설 결정(2026-08-16 사용자 확정)의 기계적 후속

## 무엇을

```diff
- kill_conditions_ref: ["KC-CRCL-1", "KC-CRCL-2", "KC-CRCL-3", "SEC 면제 불허 확정", "CLARITY 최종 실패"]
+ kill_conditions_ref: ["KC-CRCL-1", "KC-CRCL-2", "KC-CRCL-3", "KC-CRCL-4", "SEC 면제 불허 확정", "CLARITY 최종 실패"]
```

## 왜

- [fact] regulation 축 P8 분해(run 20260815_2307)로 `regulation_company_licensing` 관측 단위가 분리됐으나 대응 KC가 없었다.
- [fact] CRCL은 COIN-3 상당의 규제 조치형 KC가 부재했다 — thesis 첫 전제("규제 선점")를 뒤집는 사건(인가 취소·정지·중대 제한)이 어떤 KC에도 걸리지 않는 공백.
- [fact] 2026-08-16 사용자가 KC-CRCL-4 신설을 확정(2단 구조 + GENIUS 발행자 인가 경로 포함) — kill_conditions.yaml에 active 등재 완료.
- [fact] 본 패치는 카드 참조 목록에 KC-CRCL-4를 추가할 뿐 축 방향·시그널 등급을 변경하지 않는다(P13).
