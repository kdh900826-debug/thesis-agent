# ThesisPatch — IREN (run 20260919_2209)

- as_of: **2026-09-19** / ticker: **IREN** / priority: **medium**
- card_field: **earnings_checkpoints** / operation: **annotate**
- basis_claims: `c_20260919_IREN_3`, `c_20260919_IREN_4`
- requires_human_approval: **true** (F17 — 카드 자동 반영 금지)
- reverses_core_thesis: **false**
- 생성 패치: **1건** / 제외 후보: **3건**(아래 §4)

> ⚠️ 본 문서는 제안이다. `state/thesis_cards/IREN.yaml`은 수정되지 않았으며, 승인 큐 등재도 수행하지 않았다(오케스트레이터 소관).

---

## 1. F20 — 전문 확인 및 목록형 필드 실계수

`state/thesis_cards/IREN.yaml` **전문 136행**을 행 제한 없이 읽고 PyYAML 파싱으로 계수했다.

| 필드 | 현재 | 패치 후 기대 | 비고 |
|---|---|---|---|
| `earnings_checkpoints.items` | **13** | **14** | 본 패치가 유일하게 건드리는 목록형 필드 |
| `axes` | 6 | 6 | 불변(검증용 고정) |
| `key_metrics` | 8 | 8 | 불변 |
| `catalysts` | 4 | 4 | 불변 |
| `risks` | 8 | 8 | 불변 |
| `kill_conditions_ref` | 3 | 3 | 미기입(패치 무관) |

현재 13개 항목 전수: ①과금 가동률 ②MFU ③매니지드 서비스 믹스 ④Horizon 건설원가 실측 ⑤전력 단위원가 $/MWh ⑥GPU 대체 조항 단가 재협상 ⑦ASC842 리스 매출 최초 인식 금액 ⑧가동 ARR 진척률·가동 MW ⑨Horizon 2-4 인도·인수 ⑩완전희석 주수 range ⑪FY27 capex ⑫SB6 적용 용량 MW ⑬AI Cloud 부문 감가상각 배분.

**⑤가 이미 존재한다** — L4 후보의 두 번째 의도(소비 MWh 관측점 이월 확인)는 결손이 아니라 존치이며, 따라서 해당 건은 패치를 만들지 않았다. 2026-08-16 `ap_20260816_0010`(부분 읽기로 ⑧~⑬ 누락 오인 → 적용 후 즉시 원복)의 재발 방지 절차를 그대로 적용했다.

`expected_after.counts` 포함: **예** — `[{earnings_checkpoints.items, 14}, {axes, 6}, {key_metrics, 8}, {catalysts, 4}, {risks, 8}]`.

---

## 2. diff

```diff
  earnings_checkpoints:
    date: "2026-11 (FY27 Q1 10-Q — 정확일 미공시)"
    items:
      ...
      - "SB6 적용 용량 MW (KC-10 임계 대조 분모)"
      - "AI Cloud 부문 감가상각 배분 (자체 ~14% vs 임차 ~5% 전제 검증용)"
+     # 2026-09-19 ThesisPatch(annotate, run 20260919_2209) — 관측점 1건 신규 추가. 항목 수 13개 → 14개
+     #   (state/thesis_cards/IREN.yaml 전문 136행 기준 계수, F20). 기존 13개 항목은 문구·순서 모두 불변이며 삭제·수정분 없음(P9).
+     # ⚠️P4 한계 명시 — 추가 근거 c_20260919_IREN_3은 evidence_grade 3·confirmed=false(2차 매체 + 규제기관 페이지,
+     #   1차 URL 역추적 실패·수치 확인 실패)이고, c_20260919_IREN_4는 그 등급을 승계한 inference(strength low)다.
+     #   따라서 아래 항목은 '확인된 사실'이 아니라 '확인 대상(관측점)'으로만 등재한다 — 단독으로 축 판정·시그널 등급·
+     #   KC 판정의 근거가 될 수 없다(P4·P13).
+     # ⚠️F20 전문 확인 결과 — 기존 항목 ⑤ "전력 단위원가 $/MWh (부문별 전력비는 확보, 소비 MWh 미공시 — 이월)"는
+     #   카드에 이미 존재하며 소비 MWh 관측점이 이월 상태로 정상 유지되고 있다. 따라서 해당 건은 신규 추가·수정 대상이
+     #   아니며 본 패치는 손대지 않는다(절단 관측에 의한 허위 결손 생성 방지 — 2026-08-16 ap_20260816_0010 전례).
+     - "BC Hydro 2026 Call for Demand 결과 공표 — 선정 결과·선정자 명단 공표 여부, IREN 신청 여부, 기존 BC 계통
+        접속분에 대한 영향 여부. 배분 한도는 AI 300MW + 데이터센터 100MW(2년 단위, 별도 수소 수출 200MW), 접수 15건·
+        약 800MW(한도의 약 2배), 제시된 선정자 통보 시점 2026-09 중순 — 2026-09-19 현재 결과·명단 미공표(unconfirmed, P5).
+        IREN의 BC 노출은 Canal Flats 30 + Prince George 50 + Mackenzie 80 = 160MW(gross, 포트폴리오 5,610MW의 약 2.9%)
+        이며 Mackenzie 공랭 확장은 $2.4bn GPU 파이낸싱의 명시 용도다. ⚠️근거 등급 3·confirmed=false이므로 확인 대상일 뿐
+        확인된 사실이 아니다(P4). TX ERCOT/SB6와 별개 관할·별개 절차라 KC-10 조건문에 현 시점 직접 대응하지 않으며,
+        160MW는 gross 계획 용량이라 기준이 달라 KC-10 '계약 용량 10%+' 임계의 분모로 사용 불가(F3)"
```

`before` 문자열은 카드 내 1회만 출현하며(`grep -c` = 1), `after`는 `before`를 그대로 포함한 뒤 주석 3행 + 항목 1행을 덧붙이는 **append** 형태다 — 기존 서술 삭제 0건(P9), 따라서 `not_contains`는 비어 있다.

---

## 3. 근거와 한계

- **[fact]** `c_20260919_IREN_3` — BC 산업용 전력 배분 프레임워크: 신규 암호화폐 채굴 계통 접속 영구 불허, AI·DC는 2년 단위 경쟁 배분. 2026 Call for Demand는 2026-01-30 공고·02-01 개시, 한도 AI 300MW + DC 100MW, 접수 15건 약 800MW, 선정자 통보 2026-09 중순 제시. 2026-09-19까지 결과 미공표. **grade 3 / confirmed=false / scope=sector / out_of_window=true**, 1차 URL(news.gov.bc.ca)은 인증서 검증 실패, bchydro.com 본문에 수치 부재.
- **[fact]** `c_20260919_IREN_4` — inference(strength **low**, grade 3 승계). IREN BC 노출 160MW(gross) 및 Mackenzie 공랭 확장의 $2.4bn GPU 파이낸싱 용도를 근거로 (a)신청 여부 (b)선정·탈락 (c)기존 접속분 영향이 모두 미특정임을 지적. 축 판정 변경 근거가 아니라 unconfirmed 신규 편입.
- **[fact]** `02_company/IREN.json`의 power_permit Delta = `neutral / stage 없음`, `03_signal/IREN.json`의 `thesis_delta_summary[power_permit]` = 중립, `gate_check.upgrade_gate_result` = `not_met`. 본 패치는 등급·축 판정을 건드리지 않는다(P13).
- **[inference|low]** 이 등급으로 가능한 유일한 반영 형태는 사실 서술 추가가 아니라 **확인 대상 관측점 등재**다. 다음 관측점은 BC Hydro 결과 공표 또는 FY27 Q1 10-Q.

---

## 4. 제외한 후보

| 후보 | 결정 | 사유 |
|---|---|---|
| 전력 단위원가($/MWh)용 소비 MWh 관측점 이월 | 패치 미생성 | 항목 ⑤로 **이미 존재**. 결손 없음 → 중복 패치 금지(F20) |
| `axes.power_permit` 라벨에 BC 관측점 병기 | 패치 미생성 | grade 3·confirmed=false는 축 라벨(판정 기준선) 기입 등급이 아님(P4). Delta neutral(P5) |
| `risks`에 "BC 배분 탈락 → Mackenzie 접속 제약" 추가 | 패치 미생성 | 신청 여부조차 미확인. 공백을 추론으로 메우는 행위(P5, §1 금지사항) |

---

## 5. 하위 영향 및 미변경 항목

- `earnings_checkpoints.date`는 미변경 — BC Hydro 결과 공표는 실적 일정과 독립 사건이므로 항목 본문에 관측 시점을 적었다.
- `axes.power_permit`(2026-09-12 패치로 ERCOT Batch Zero 관측점 병기 완료), `risks`의 TX SB6/ERCOT 항목, `catalysts`의 "PUCT SB6 최종 규칙(2026말)" 모두 **별개 규제 트랙**이므로 미수정.
- KC-10의 조건·임계 수정은 `config/kill_conditions.yaml` 소관이며 사용자 영역(CLAUDE.md §9).

---

## 6. 검증

- `validate_output.py output/20260919_2209/07_thesis_patch/IREN.json --layer thesis_patch` → **PASS**
- 스크래치패드 dry-run(원본 카드 미변경): 치환 1회 적용 → YAML 파싱 성공, `earnings_checkpoints.items` = **14**, axes 6 / key_metrics 8 / catalysts 4 / risks 8 불변, `approvals.verify_after_apply()` 위반 **0건**.
