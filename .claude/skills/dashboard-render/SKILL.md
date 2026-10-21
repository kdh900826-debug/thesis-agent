---
name: dashboard-render
description: run dashboard 명령 시에만 사용. KC 이격도(근접순·시계열)·시그널 상향 게이트·노출 매트릭스(부호·강도×실포지션)·축별 Delta 추이·촉매 관측점·승인 대기 건을 정적 로컬 HTML 1장("임계 관제판")으로 생성한다. 자동 생성하지 않는다.
---

# dashboard-render — 요청 시 대시보드 (D11) · v2 "임계 관제판"

## 실행

```bash
python .claude/skills/dashboard-render/scripts/dashboard_render.py --out output/dashboard.html
```

## 내용 (읽기 전용 요약 — 어떤 판정도 새로 생성하지 않는다)

v2(2026-09-05)는 '현재 상태' 나열이 아니라 **'임계까지의 거리·방향·시점'** 을 보여준다.

0. **상단 요약 스트립** — 최근접 KC / 집중도 초과 축 수 / 시그널 한 줄 / 승인 대기 건수
1. **① KC 이격도 보드** (최신 `01_macro_kc.json` + 전 run 시계열) — KC별 실측값 vs 임계
   이격 원문, 근접순 정렬, run 시계열 스파크라인, 파급 종목·포트 파급%(`05_correlation.json`
   `kc_propagation`), provisional·staleness 배지. 없으면 "미실행" 표기
2. **② 시그널 · 상향 게이트** (`state/signals.json` + 최신 `03_signal/*.json`
   `gate_check.upgrade_gate`) — 3요건(정량·회사 고유·매출 인식) 체크와 next_check 원문
3. **③ 노출 매트릭스** (`config/correlation_matrix.yaml` + `config/positions.yaml` +
   `05_correlation.json` 집중도) — 부호·강도(상/중/하) 히트맵에 실포지션 오버레이,
   셀 title에 basis 원문. **수치형 상관계수는 표시하지 않는다(P14)**
4. **④ 축별 Delta 추이** (최근 3개 run의 `02_company/*.json` deltas) — ▲강화/▼훼손/◆혼재/●중립,
   한/영 방향 라벨은 표기만 통일(재해석 아님)
5. **⑤ 촉매·관측점** (`state/thesis_cards/*.yaml`) — 실적 체크포인트 일자 + catalysts 원문
6. **⑥ 승인 대기 큐** (`state/pending_approvals.json` — pending만)
7. 각 항목의 `as_of` + staleness 경고 배지 — **stale 데이터를 신선한 것처럼 보이게 하지 않는다(P16)**

## 파생 계산 고지 (필수 유지)

근접도 막대의 채움율만 본 스크립트의 파생 계산이다(|임계|>0이면 1−|이격|/|임계|, 임계=0이면
run 시계열 범위 대비, AND형은 감시 목적상 최근접 레그). 원 산출물에 없는 지표이므로 하단 각주로
반드시 명기하며, **판정 근거는 항상 원문 이격 문구다.** 그 외 모든 판정·문구는 계층 산출물 원문 인용.

하단 고정 문구: "본 대시보드는 판단 보조용 요약이며 매수·매도 지시가 아닙니다."

v1 스크립트 원본: `scripts/dashboard_render_v1_backup.py` (P9 — 이력 보존)
