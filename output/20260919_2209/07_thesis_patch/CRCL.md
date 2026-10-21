# ThesisPatch — CRCL / **패치 0건 (제외 + unconfirmed 이월)**

- **Run**: 20260919_2209 · as_of 2026-09-19 · skill `thesis-refine` (S7)
- **처리 대상**: L4가 올린 후보 **1건**(priority medium / reserve_income 축 금리 노출 강도 표현). 신규 후보 창작 없음.
- **결과**: 패치 **0건** — 승인 큐 등재 대상 없음. `state/thesis_cards/CRCL.yaml`·`state/pending_approvals.json` 미수정(F17), `approvals.py` 미호출.
- **사전 확인(F20)**: `state/thesis_cards/CRCL.yaml` **전문 86행** 열람 완료. `yaml.safe_load` **파싱 정상**. 계수 — axes 8 / risks 5 / key_metrics 7 / earnings_checkpoints.items 6 / version_history 12. 부분 읽기 기반 '부재·누락' 판정 없음.
- **config 경계**: `config/correlation_matrix.yaml`은 **열람·수정하지 않았다**. 노출 벡터 논점은 vcp_05로 분리돼 사용자 편집 영역이다(CLAUDE.md §9).

## diff

```diff
--- state/thesis_cards/CRCL.yaml (before) — 원문 보존, 변경 제안 없음 (P9)
+++ (after 없음 — 패치 미생성)
   - {id: reserve_income,    label: "Reserve Income·마진 (금리 직결)"}
```

## 제외 사유

**[fact]** L4 후보의 원전제(“노출 벡터에 CRCL 금리 노출이 정의돼 있지 않다”)는 **오류**로 확인됐다 — 벡터에 `CRCL.RATES`는 정의돼 있다. 따라서 후보의 최초 근거는 소멸했다.

**[fact]** 남은 실질 논점인 “벡터 강도 **H** vs `c_20260919_CRCL_8`의 `inference_strength: low`”는 **동일 척도의 두 값이 아니다**. 전자는 포트폴리오 층의 구조적 노출 방향·강도 표기이고, 후자는 이번 창 개별 추론의 신뢰 강도다. 이를 ‘비대칭’으로 간주해 카드 문안을 조정하면 **config 값을 카드로 역수입**하는 것이 되어 §9 경계를 침범한다.

**[fact]** 유일한 근거 후보 `c_20260919_CRCL_8`은 `claim_type=inference / scope=macro / confirmed=false / inference_strength=low`다. **P6·P13**상 매크로 스코프 재료는 개별 종목 축 판정의 근거가 될 수 없고, **P2**상 정성 논거는 상향 근거로 부적격이다. 2026-09-16 FOMC 25bp 인상(`c_20260919_CRCL_7`, scope=macro)도 같은 이유로 축 서술의 근거로 사용하지 않았다.

**[fact]** 이번 창에 Circle의 **준비금 실효수익률·듀레이션·재투자 만기구성·유통비용(파트너 분배) 비중**에 관한 회사 1차 자료(공시 또는 경영진 직접 발언)는 **확보되지 않았다**. `02_company/CRCL.json#unconfirmed`에 `no_company_primary_source`로 이미 적재돼 있다. **P5** — 부재는 반증이 아니며 추론으로 메우지 않는다.

**[fact]** `03_signal/CRCL.json`은 reserve_income 축을 **neutral / stage 없음**으로 집계했고 등급 전이 후보는 **maintain(🔴)**이다. 카드 서술을 부정확하게 만든 신규 1차 자료가 없다 — S7의 패치 생성 요건 자체가 성립하지 않는다.

**[fact]** `operation: annotate`(관측 대기 주석) 수준도 **먼저 검토한 뒤 제외**했다. 카드는 이미 세 곳에서 금리 연동을 담고 있다:

| 위치 | 현행 서술 |
|---|---|
| `axes.reserve_income` | "Reserve Income·마진 **(금리 직결)**" |
| `key_metrics` | "**기준금리 (이자수입 직결)**" |
| `risks` | "**금리 인하 시 이자수입 직접 축소** (포트폴리오 내 다른 자산과 역방향 노출 — 자연 헤지)" |

또한 `earnings_checkpoints.items`는 "Reserve Income 절대액·이자율 민감도"와 "유통비용(파트너 분배) 비중"을 **이미 관측 항목으로 지정**하고 있다. 관측 대기 주석은 기존 서술의 중복 기재에 그치고 신규 정보가 없으며, 근거 없는 주석은 S7 규칙상 패치 무효 사유다.

**[fact]** 따라서 이번 창의 정상 경로는 패치 생성이 아니라 **제외 + unconfirmed 이월 + 사유 로그**다(P5·P12, CLAUDE.md §7 “게이트 미충족은 실패가 아니라 정상 경로”).

## unconfirmed 이월

1. **Circle 준비금 실효수익률·수익 인식 시차** (`no_company_primary_source`) — 검증 게이트 = Q3'26 실적 공시. 출처: `output/20260919_2209/02_company/CRCL.json#unconfirmed`
2. **벡터 CRCL.RATES 강도(H)와 카드 축 서술의 정합 판단 기준** (`out_of_scope_for_card_patch`) — 두 값이 동일 척도가 아니어서 이번 창 자료로 정합·부정합 어느 쪽도 판정 불가. 벡터 조정 논점은 vcp_05(사용자 판단).

**재개 게이트**: Q3'26 실적·10-Q에서 Reserve Income 절대액·이자율 민감도·유통비용 비중의 회사 1차 수치가 공시되면 reserve_income 축 서술의 강도 정합을 근거 있는 `amend`로 재검토한다.

## 카드 YAML 건전성 점검

**[fact]** `yaml.safe_load` 파싱 **정상**. 과거 `approvals.py` 이스케이프 버그로 인한 파손 이력을 감안해 별도 확인했다. `version_history` 항목의 `change` 문자열에 토큰이 `/`로 분절된 흔적(예: `이전: - / {id: / diversification, ...`)이 남아 있으나 YAML 문법상 유효한 단일 스칼라이며 파싱을 막지 않는다 — **가독성 부채로만 기록**한다(P9 — 이력 삭제 금지).

## 부수 확인 — `.claude/agents/company-crcl.md` (수정하지 않음)

**[fact]** 24행 `**8/18 Q2 실적 임박**` — **stale 확인**. Q2'26 실적은 2026-08-05 발표 완료(카드 catalysts의 ‘⚠️소멸’ 주석)이고, 2026-08-18은 Circle-Coinbase 분배계약 3년 **자동 갱신 예정일**(KC-CRCL-3 관측 항목)로 실적 게이트가 아니다. 카드 `earnings_checkpoints.date`도 2026-08-15 패치로 `null`이며 Q3 공식 IR 공지는 이번 창에도 미확인이다(F1).

**[fact]** 부수 발견 2건(동일 파일, 함께 stale):
- 19행 축 매핑 목록 `usdc_circulation / reserve_income / competition_ousd / regulation / diversification` — 현재 카드 축은 8개이며 `usdc_circulation → usdc_circulation_scale`, `competition_ousd → competition_ousd_consortium + competition_yield_bearing`, `regulation → regulation_company_licensing + regulation_sector_legislation`으로 분해됐고 `usdc_market_share`가 별도 축으로 존재한다.
- 27행 `$YLDS … 리스크 등록부 누락 상태(u_20260815_011) — ThesisPatch 후보` — 해당 누락은 2026-08-15·2026-09-05 risks/amend 패치로 **이미 해소**돼 카드 risks에 grade 1 수치가 등재돼 있다.

**[fact]** 에이전트 정의 파일은 카드 패치 대상이 아니므로 **확인만 수행**했다. 수정 여부는 사용자 판단이다.

## 검증

```
PYTHONIOENCODING=utf-8 python .claude/skills/validate-output/scripts/validate_output.py \
  output/20260919_2209/07_thesis_patch/CRCL.json --layer thesis_patch
→ PASS (exit 0)
```

**[fact]** 스키마 주석 — `check_thesis_patch`는 최상위 dict를 단일 패치로 간주하고 `check_common`은 최상위 `as_of`를 요구하므로, 0건 산출물은 순수 빈 배열로 두 검사를 동시에 만족시킬 수 없다. 최상위를 컨테이너 dict로 두고 패치 배열은 `patches: []`(빈 배열)로 유지했다. 컨테이너의 `requires_human_approval: true`는 F17 불변 조건의 명시이고 `basis_claims`는 ‘검토한 근거 후보’를 가리킨다 — **채택된 패치는 0건**이다.

> 패치 0건은 실패가 아니라 정상 종료다(P5·P12). 카드에 반영될 변경은 없으며 자동 반영도 없다(F17).
