---
name: weekly-events-neocloud
description: thesis-agent 산출물로 IREN·NBIS·CRWV 주간 이벤트 공개용 HTML을 쉬운 말로 갱신(개인정보 없음)
---

작업 폴더: C:\Users\user\Desktop\클로드\투자 가설 검증\thesis-agent
목표: IREN·NBIS·CRWV 주간 이벤트 페이지(output/weekly_events.html)를 최신 점검 산출물과 주가·재무부 현금(TGA) 기준으로 갱신한다. 이 페이지는 제3자에게 공개될 수 있다.

먼저 .claude/skills/weekly-events/SKILL.md 전문을 읽고 그 규칙(1~27번, 18a~18f·22a~22d 포함)을 따른다. 요약:

0. 주가·TGA 갱신 (Bash, UTF-8 모드):
   cd "C:/Users/user/Desktop/클로드/투자 가설 검증/thesis-agent" && PYTHONUTF8=1 python .claude/skills/weekly-events/scripts/weekly_events_render.py --update-prices --update-tga
   - yfinance 수집 실패 시 캐시(state/weekly_prices.json)로, TGA 수집 실패 시 캐시(state/weekly_tga.json)로 진행하고 보고에 적는다.
1. 정리 대기 목록 생성: PYTHONUTF8=1 python .claude/skills/weekly-events/scripts/weekly_events_render.py --pending
2. output/weekly_events_pending.json을 읽는다. 0건이면 3단계의 Claim 정리는 건너뛴다.
3. state/weekly_events.json 전문을 읽고(수정 전 state/weekly_events_backup_<오늘 YYYYMMDD>.json으로 복사), 대기 항목을 쉬운 말 이벤트로 events에 추가한다. 새 항목마다:
   - id(e<MMDD>-<IREN|NBIS|CRWV|ALL>-<n>), text(무슨 일), why(왜 중요한가 1~2문장)
   - detail: 3~6문장 — 누가·언제·어떤 서류·핵심 숫자·공개 안 된 것·자료 등급
   - exposure: 노출 매트릭스 영향 [{tk, axis, dir(up/down/watch), note}] — 2차 보도·계획 단계·숫자 없음은 watch 기본. 매트릭스에 없는 축은 자유 라벨.
   - basis: 해당 run 점검 판정(02_company deltas·03_signal)이 있으면 한 줄, 없으면 생략
   - links: 관련 과거 이벤트 [{id, why}], threads: 소속 추적 이야기 id
   - 추적 이야기(threads[])의 events에 새 id를 추가하고 status·next를 이번 주 기준으로 고쳐 쓴다. 새 흐름이면 이야기 추가.
   - 숫자는 원문 그대로(반올림만). 새 판정·전망·매수/매도 표현 금지. evidence_grade 3·4 또는 confirmed:false → "rumor": true. 노이즈·같은 사실 재확인은 제외('신규 공시 없음'은 한 줄).
   - 주가 규칙(SKILL.md 21번): 지난주 주간 등락 ±8% 이상 또는 하루 ±5% 이상 움직임이 있고 원장에 설명 항목이 없으면, WebSearch로 원인을 찾아 항목을 추가한다(rumor: true, basis: "시스템 점검 반영 전 — 다음 점검에서 1차 자료로 대조 필요"). 업종 동반 움직임은 이야기 t-ai-demand에 묶는다. 인과를 단정하지 않는다.
   - 필요하면 week_titles(월요일 ISO 키), headline(지난주 주간 등락 한 문장 포함), status_notes, upcoming 갱신.
   - curated_through_run = 처리한 최신 run_id(있으면), updated_at = 오늘 날짜.
   - 시스템 점검·등급 확정 항목과 주가·TGA 수치는 스크립트가 자동 생성하므로 원장에 숫자 표를 따로 만들지 않는다(추적 표 sw-stages·dilution은 예외 — 4b).
3b. 업계 AI 계약 비교 갱신(SKILL.md 23~27번): state/peer_contracts.json 전문을 읽고 asof 이후 IREN·Hut 8·Cipher Digital·TeraWulf·Core Scientific·Galaxy·Applied Digital·Riot·CleanSpark·Bitdeer(필요시 MARA·Keel 등 신규 계약사)의 새 AI 임대·클라우드 계약·연장·자금 조달 발표를 WebSearch로 찾는다(회사 보도자료·8-K 우선, 2차 보도만 있으면 rumor: true). 새 건이 있으면 수정 전 state/peer_contracts_backup_<오늘 YYYYMMDD>.json으로 복사하고 contracts[]/financing[]에 추가, asof를 오늘로 바꾼다. 단가는 쓰지 않는다(렌더러 계산). 순서는 신경 쓰지 않는다(렌더러가 최근 순 정렬). IREN 관련 새 계약이면 원장 events에도 항목을 추가할지 판단한다.
3c. TGA 계획 가정 확인(SKILL.md 22c): 지난주에 재무부 분기 차입 추정 발표(home.treasury.gov 'Treasury Announces Marketable Borrowing Estimates') 또는 분기 발행 계획 발표('Quarterly Refunding Statement')가 나왔는지 WebSearch로 확인한다(2·5·8·11월 초). 나왔으면 수정 전 state/weekly_tga_backup_<오늘 YYYYMMDD>.json으로 복사하고, 원문의 분기 말 잔고 가정·기간 중 최고치 예상을 plan[]에 새 항목으로 추가한다(원문 숫자만, src·url 필수, 지난 항목은 지우지 않음). 범위를 해석했으면 plan_note에 "(해석)"으로 적는다. 가설·인과 문장은 쓰지 않는다.
4. 렌더(1차): PYTHONUTF8=1 python .claude/skills/weekly-events/scripts/weekly_events_render.py
   - '안내(해설)'에 나온 추적 이야기마다 explainer를 새로 쓰거나 갱신한다(SKILL.md 15~17번): asof=오늘, summary(한 줄 답), context(규모 표·전체 대비 %·숫자 성격), gates(관문별 상태·근거), scenarios(나빠지는 경로별 — 관측·판단 분리 + conclusion), impact(단기/장기), watch(언제 알 수 있나), caveats. 조건부↔확정, 계획↔확보↔가동, 발표↔이행↔매출을 구분하고 회사 자체 평가와 규제·감사 결과를 구분한다. 근거는 산출물 Claim·과거 원장 항목·thesis 카드(읽기만)와, 주가 원인에 한해 WebSearch 결과(2차 자료로 표시)에서만 가져온다.
4b. 추적 표 재확인(SKILL.md 18a~18f): '안내(해설)'에 `<이야기>/<표 id>: 추적 표를 이번 주에 확인하지 않음` 또는 `<종목>/dilution: 종목 추적 표가 아직 없음`이 나오면, 새 소식이 없어도 그 표의 칸마다 근거를 다시 대조한다(없으면 만든다). 단계가 바뀐 칸만 고치고(확인 수준을 칸에 표시: 2차 보도 "(2차 보도)", 정황은 "정황상", 계산은 "(계산)"), 바뀌지 않아도 표 asof를 오늘로 바꾼다. 칸이 바뀌면 같은 이야기의 gates·status·summary도 맞추고, 원장에 없는 새 사실은 이벤트로 추가한다. 현재 대상:
   - t-iren-tx/sw-stages(Sweetwater 1·2 단계표) — 이번 주 IREN 산출물 Claim·원장 이벤트를 먼저 보고, WebSearch로 IREN 보도자료·8-K/10-Q와 ERCOT Batch Zero 소식(분류 유지·강등, 12/10 검증 보고서, 연결 보류 해제, 용량 약정·담보 마감, Sweetwater 1 가용 MW, Sweetwater 2 개통)을 확인한다.
   - <종목>/dilution 희석 점검표(IREN t-iren-dilution, NBIS t-nbis-funding, CRWV t-crwv-debt) — SKILL.md 18e의 ⓐ 주식 판매 남은 한도(+최근 종가로 다 쓰면 늘어날 주식 수) ⓑ 발행 주식 수→완전희석 주식 수(+전환사채 전환 시 증가분) 행을 둔다. ⓒ 행은 렌더러가 per_share로 자동 생성하므로 손으로 쓰지 않는다. WebSearch·EDGAR로 새 10-Q/10-K/6-K 표지 주식 수, ATM 보충서·판매 실적, 전환사채 발행·전환·되사기, 주총 희석 안건, 연환산 매출 발표를 확인하고, ⓐ 환산 주식 수는 최근 종가로 매주 다시 계산한다. '지난 확인 대비' 열에 바뀐 칸만 "이전 → 지금 (근거)"를 적는다.
   - 주당 매출·ARR(SKILL.md 18f) — 분기 보고서·실적 발표·ARR 갱신·발행 주식 수가 실린 공시가 새로 나왔거나 '안내(해설)'에 `<종목>/per_share: …입력이 아직 없음`이 나오면, state/weekly_events.json의 per_share.<종목>에 원본 숫자(금액 $M·주식 백만 주: asof·label·rev_q·rev_q_period·arr_live·arr_live_asof·arr_contract·sh_basic·sh_basic_asof·sh_fd·sh_fd_asof·src)로 새 입력을 덧붙인다. 직전 입력을 복사해 바뀐 값만 고치고, 지난 입력은 고치지 않는다. 공개 안 된 값은 null, 2차 보도 숫자는 넣지 않는다.
5. 렌더(최종): 같은 명령을 다시 실행. 종료 코드 2(개인정보 의심 문구)면 원장 문구를 바꿔 쓰고 재실행. '경고(연결)'는 끊긴 id를 고친다. '안내(해설)'가 남지 않아야 한다.
6. 확인: PYTHONUTF8=1 python -m pytest tests/validators/test_weekly_events_privacy.py tests/validators/test_weekly_events_tga.py -q

개인정보 절대 금지: config/positions.yaml을 읽지 않는다. 보유 비중·보유/미보유·평단·주수·개인 가격선($30·$28 등)·계좌 집중도·'내 ~' 표현을 쓰지 않는다. 회사 지표에도 '보유'·'비중' 단어 대신 다른 말(예: '매출에서 차지하는 몫', 회사 주식은 '발행 주식 수')을 쓴다. 주가·TGA(공개 시장·정부 데이터)는 써도 된다.
하지 말 것: run full 등 점검 파이프라인 실행, config/*.yaml·state/signals.json·thesis 카드 수정, 아티팩트 발행·외부 전송.

끝나면 한국어로 8줄 이내 보고: 지난주 세 종목 주간 등락(나스닥100 대비), 재무부 현금(TGA) 최신 잔고·전주 대비와 재무부 계획 가정 대비 차이(새 계획 발표를 반영했으면 그 내용), 추가한 이벤트 수, 업데이트된 추적 이야기와 해설을 쓴/갱신한 이야기, 추적 표(sw-stages)에서 바뀐 칸(없으면 '변동 없음'), 희석 점검표(dilution) 종목별 바뀐 칸·새로 만든 표와 주당 매출·ARR 새 입력(종목별 주당 가동 ARR 범위와 직전 대비 %, 없으면 '변동 없음'), 업계 계약 표에 추가한 계약·자금 조달 건수, 마지막 시스템 점검일(10일 넘게 지났으면 '새 점검 필요'라고 명시), 생성 파일 경로.