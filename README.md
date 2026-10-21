# thesis-agent — 투자 Thesis 검증·포트폴리오 구성 에이전트 시스템

설계 문서: [docs/에이전트시스템_설계계획서_v2_20260815.md](docs/에이전트시스템_설계계획서_v2_20260815.md) (v2.1)

> 투자 판단 보조 시스템. 매수·매도 지시를 생성하지 않는다.

## 시작 전 체크리스트 (설계서 §11 R1~R3, U4)

| # | 항목 | 방법 |
|---|---|---|
| R1 | FRED API 키 | https://fred.stlouisfed.org/docs/api/api_key.html 무료 발급 → 환경변수 `FRED_API_KEY` 설정. 부재 시 30Y·ON RRP·브렌트가 웹검색 fallback으로 강등 |
| R2 | 종목 KC 임계 확정 | `config/kill_conditions.yaml`의 `status: draft` KC들 — ⚠️초안 수치를 검토·수정 후 `status: active`로 변경. 확정 전에는 로드되지 않음(P11) |
| R3 | 포지션 기입 | `config/positions.yaml`의 `weight_range`(비중 구간)를 기입. 미기입 시 축 집중도는 종목 수 기준 상대 판정만 가능 |
| U4 | 상관 노출 벡터 확정 | `config/correlation_matrix.yaml` — v1 §5-8에서 도출한 ⚠️초안 상태. 검토 후 `status: active`로 변경 |
| — | Python 의존성 | `pip install pyyaml requests` (선택: `yfinance` — VIX·브렌트 수집용) |

## 사용법

Claude Code를 이 폴더에서 열고 자연어로 명령한다. 명령 목록은 `CLAUDE.md` §3.

```bash
claude
```

예: `run macro` / `run ticker IREN` / `run earnings CRCL` / `approve ap_20260815_1430_patch_iren` / `run dashboard`

## 구조

```
CLAUDE.md            L0 오케스트레이터 지침 (원칙 P1~P17, 명령, 격리 화이트리스트)
config/              ★ 사용자 직접 편집 영역 (7종 yaml)
state/               영속 상태 — thesis 카드 7장, 시그널, 승인 큐, 미확인 큐
.claude/agents/      서브에이전트 12개 정의
.claude/skills/      스킬 13개 (SKILL.md + CODE 스크립트)
.claude/scripts/     오케스트레이터 전용 스크립트 (격리 필터본 생성 등)
output/{run_id}/     Run별 산출물 (로컬 영속)
tests/validators/    검증기 단위 테스트 (pytest, D12)
docs/                발행 안정 버전 격리 + 설계 문서
scheduled-tasks/     예약 작업 프롬프트 사본 (원본: ~/.claude/scheduled-tasks/)
```

## 다른 PC에서 이어 쓰기

1. `git clone https://github.com/kdh900826-debug/thesis-agent.git` 후 이 폴더에서 Claude Code를 연다.
2. 주간 이벤트 페이지(weekly_events): 데이터 `state/weekly_events.json`·`state/weekly_prices.json`, 렌더러 `.claude/skills/weekly-events/`, 결과 `output/weekly_events.html`이 저장소에 들어 있다.
3. 예약 작업은 PC별로 등록된다 — `scheduled-tasks/{작업명}/SKILL.md`를 새 PC의 `~/.claude/scheduled-tasks/`로 복사하거나, Claude에게 해당 SKILL.md 내용으로 예약 작업을 다시 만들어 달라고 한다. SKILL.md 안의 절대 경로가 새 PC와 다르면 고친다.
4. FRED 키는 저장소에 없다 — `setup_fred_key.ps1`로 새 PC에서 다시 설정한다.

## 설계서와의 구현 편차 (기록)

- 설계서 §8-1의 `/agents/{name}/AGENT.md`는 Claude Code 실제 규약인 `.claude/agents/{name}.md`(단일 파일 + frontmatter)로 구현했다.
- 오케스트레이터 전용 스크립트(D7 필터본 생성)는 `.claude/scripts/`에 둔다 — 설계서 트리에 없던 폴더이나, 특정 스킬 소속이 아니기 때문.
- `state/signals.json` 초기 등급은 `투자_Thesis_Map_v32_20260814.md`에서 승계했고, 신규 커버리지 NBIS·CRWV는 🟡 관망으로 초기화했다.
