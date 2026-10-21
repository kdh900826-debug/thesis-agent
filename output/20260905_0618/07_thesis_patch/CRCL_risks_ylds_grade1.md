# ThesisPatch — CRCL / risks / amend

- **Run**: 20260905_0618 · 2026-09-05T06:18 (L4 병행 `thesis-refine`)
- **대상 필드**: `risks` (expected_after.counts: risks=5 — F20)
- **operation**: `amend`
- **승인 필요**: ✅ (requires_human_approval: true, F17) / **핵심 논거 역전**: ❌ 아니오
- **사전 확인**: 대상 카드 전문 열람 후 before 문자열의 카드 원문 일치 확인 ✅ (F20 — 부분 읽기 기반 '부재' 판정 없음)

## diff

```diff
--- state/thesis_cards/CRCL.yaml (before)
+++ state/thesis_cards/CRCL.yaml (after 제안)
@@ -1 +1,2 @@
-  - "이자부 스테이블코인 경쟁자 — $YLDS(Figure 발행, SEC 등록, SOFR 연동 이자 지급, Provenance·Solana·Stellar 상장) 유통량 1Q26 약 $598M (grade 4, confirmed=false). USDC 분기말 $73.3B 대비 1% 미만. [inference:medium] 현 규모만으로는 점유율 위협으로 판정되지 않으며, 위협의 실질은 규모가 아니라 이자부 스테이블코인의 법적 취급(CLARITY 이자조항 문언)에 조건부다 — 2026-09-15 절차 표결은 최종 표결이 아니고 조항 문언은 미확정이다. grade 4 단독으로는 방향 판정 근거가 될 수 없으므로(P4) 정량 감시 항목으로만 등재한다"
+  # 2026-09-05 ThesisPatch(amend, run 20260905_0618) — 이전 값의 "1Q26 약 $598M (grade 4, confirmed=false)"는 이번 run에 발행사 FIGR의 1차 공시(8-K EX-99.1 2026-05-12 / 10-Q·8-K 2026-08-13~14)로 grade 1 confirmed 격상됐고 2Q26 신규 수치가 확보됐다. 등급·수치만 정정하며 위협 판정 프레임(CLARITY 이자조항 조건부)은 유지한다(P9 — 이전 서술 주석 보존). 항목 수 5개 불변.
+  - "이자부 스테이블코인 경쟁자 — $YLDS(Figure 발행, SEC 등록, SOFR 연동 이자 지급, Provenance·Solana·Stellar 상장) 유통량: 4Q25말 $328.193M → 1Q26말 $598M → 2Q26말(6/30) $556.033M — 전부 발행사 FIGR 1차 공시(grade 1, confirmed). 2Q26은 QoQ -7.0%로 4Q25→1Q26의 고성장 추세가 정체·반전. USDC 분기말 $73.3B 대비 여전히 1% 미만. [inference:medium] 근접 위협은 완화 신호이나 구조적 리스크는 미해소다 — 위협의 실질은 규모가 아니라 이자부 스테이블코인의 법적 취급(CLARITY 이자조항 문언)에 조건부이며, 2026-09-15 절차 표결은 최종 표결이 아니고 조항 문언은 미확정이다. 정량 감시 항목으로 유지"
```

## 왜

[fact] 카드 항목은 $YLDS 1Q26 유통량을 'grade 4, confirmed=false'로 표기하고 있으나, 이번 run에서 발행사 FIGR의 1차 공시로 동일 수치가 확인됐다 — 1Q26 $598M(8-K EX-99.1, 2026-05-12, c_20260905_CRCL_0618_003), 2Q26 $556.033M·4Q25 $328.193M(10-Q 및 8-K EX-99.1, 2026-08-13~14, c_20260905_CRCL_0618_002). 둘 다 grade 1 confirmed. [fact] 따라서 카드의 등급 표기(grade 4·confirmed=false)는 더 이상 사실이 아니며, 최신 분기 수치도 누락돼 있다. [fact] 두 grade 1 수치의 산술 차이로 2Q26 QoQ -7.0%가 도출된다 — 추세가 고성장에서 정체·반전으로 바뀌었다. [inference:medium] 규모 기준의 근접 위협은 완화됐으나 구조적 리스크는 해소되지 않았다 — 위협의 조건부성(CLARITY 이자조항 문언)은 이번 run에도 변하지 않았으므로 판정 프레임은 그대로 유지한다. [fact] 항목 수는 전문 기준 5개로 불변이며 이전 서술은 주석으로 보존한다(P9·F20).

**역전 판정 주석**: [fact] 리스크 항목의 자료 등급·수치 정정이며 thesis 본문('규제 선점 + USDC 유통량 기반 준비자산 이자 수입...')과 시그널 등급(🔴)에 대한 판정을 포함하지 않는다. 등급 확정은 사람 영역이다.

**후속 주의**: [fact] 본 정정은 competition_ousd 축 분해 제안(CRCL_axes_competition_decompose)과 같은 재료에서 나온다 — 분해가 승인되면 이 risks 항목은 competition_yield_bearing 하위 축과 대응한다. [fact] $YLDS 3Q26 수치는 FIGR 차기 10-Q에서 갱신 가능하다.

## 근거 Claim

c_20260905_CRCL_0618_002, c_20260905_CRCL_0618_003, d_20260905_CRCL_0618_002

출처: `output/20260905_0618/02_company/CRCL.json#claims[c_20260905_CRCL_0618_002/003] · #deltas[d_20260905_CRCL_0618_002]`

> 이 패치는 제안이며 자동 반영되지 않는다(F17). 적용은 사람의 `approve <id>` 이후 approvals.py가 수행한다(백업 → 적용 → expected_after 자동 대조 → 실패 시 원복).
