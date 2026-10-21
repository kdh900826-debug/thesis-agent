# ThesisPatch — CRCL / axes / decompose (regulation 축 P8 분해)

- **Run**: 20260815_2307 · 2026-08-15
- **대상 필드**: `axes` → `regulation`
- **operation**: `decompose` (P8)
- **승인 필요**: ✅ `requires_human_approval: true`
- **핵심 논거 역전 여부**: ❌ 아님 — 라벨에 **방향 전제가 내장되어 있지 않아** 정정 대상이 되는 결론 문장이 없다 (직전 `usdc_circulation` 분해가 에스컬레이션을 거친 이유는 "축소 추세"라는 방향 전제 때문이었다)

## 무엇을

```diff
- - {id: regulation, label: "규제 — SEC Innovation Exemption·CLARITY (2차 독립 게이트)"}
+ - {id: regulation_company_licensing,  label: "회사 개별 인허가 (OCC Circle National Trust 설립 최종 인가·
+                                              NYDFS Circle New York Trust 승인 — grade 1 confirmed,
+                                              scope=company_specific)"}
+ - {id: regulation_sector_legislation, label: "섹터 입법·규제 게이트 (SEC Innovation Exemption·CLARITY —
+                                              2차 독립 게이트. 8/14 SEC 면제 재지연·회의 취소 grade 4,
+                                              CLARITY 9/15 절차 표결 순연 grade 3 — 둘 다 confirmed=false.
+                                              9/15는 최종 표결이 아니다. scope=sector이므로 개별 종목
+                                              등급 근거로 사용 불가(P6·P13))"}
```

(정확한 치환 문자열은 동명 `.json`의 `before`/`after` 참조)

## 왜 (P8 트리거)

| 요소 | 내용 |
|---|---|
| 새 1차 자료 | OCC Circle National Trust 설립 최종 인가 + NYDFS 승인 — **grade 1 confirmed** |
| 기존 축 라벨 | "SEC Innovation Exemption·CLARITY" — **섹터 입법만 지목**. 회사 인허가를 수용하는 정의가 없다 |
| 충돌 | 같은 축에 strengthen 1건(grade 1) + weaken 2건(grade 3·4, confirmed=false)이 매핑돼 diverge/high |
| 섹터 판정 | "종목 간 실질 이견 아님 — intra-ticker 분산 + **축 정의 불일치**". "정의 차이를 걷어내면 두 사안은 서로 다른 층위이므로 애초에 같은 축에서 상쇄될 성질이 아니다" |

- [inference:strong] 분해하지 않으면 **grade 1 confirmed 재료와 grade 3·4 confirmed=false 재료가 등급 구분 없이 같은 축에서 상쇄**돼 P4 위계가 무력화된다.
- [inference:strong] 나아가 섹터 입법 재료는 `scope=sector`라 개별 종목 근거로 쓸 수 없는데(P6·P13), 회사 인허가와 한 축에 묶여 있으면 그 경계가 축 단위에서 보이지 않는다.

## 하위 축 ↔ KC 재연결

| kill_conditions_ref 항목 | 귀속 하위 축 |
|---|---|
| "SEC 면제 불허 확정" | `regulation_sector_legislation` |
| "CLARITY 최종 실패" | `regulation_sector_legislation` |
| (대응 KC 없음) | `regulation_company_licensing` — 신설 여부는 **사용자 판단**(P11) |

## 하지 않는 것

- 두 하위 축의 방향 판정 ❌ (미판정 상태로 둔다)
- `thesis` 문장의 "규제 선점(GENIUS Act·MiCA)" 수정 ❌ (유지)
- `correlation_matrix.yaml` REGULATION 축 변경 제안 ❌ — 해당 축은 이미 섹터 입법 전용으로 정의돼 있고, 회사 개별 인허가는 노출 축이 아니라 종목 고유 사안이다
- 시그널 등급 변경·제안 ❌ (P13)
