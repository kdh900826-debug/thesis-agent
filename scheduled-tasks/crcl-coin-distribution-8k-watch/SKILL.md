---
name: crcl-coin-distribution-8k-watch
description: Circle-Coinbase 분배계약 8/18 자동 갱신 관련 8-K 제출 여부 관측 (KC-CRCL-3·KC-COIN-4 게이트)
---

작업 디렉토리: C:\Users\user\Desktop\클로드\투자 가설 검증\thesis-agent

이 프로젝트는 투자 Thesis 검증 에이전트 시스템이다. CLAUDE.md(오케스트레이터 지침)를 먼저 읽고 규약을 따르라. Python 실행 시 PYTHONIOENCODING=utf-8 필수.

## 오늘의 임무: Circle-Coinbase 분배계약 갱신 8-K 관측

배경: 2023-08-18 발효된 Circle-Coinbase USDC 분배계약이 **2026-08-18(미국시간)에 3년 자동 갱신 예정**이었다. 양사 CFO/CEO가 "기존 조건대로" 갱신을 사전 확인했으나(grade 2), 갱신 실행·조건을 확인하는 공시(8-K)는 2026-08-16 시점까지 부재였다. 이는 KC-CRCL-3(분배 계약 변경 — 경중 불문 즉시)·KC-COIN-4(COIN 불리 방향)의 관측 항목이며, signals.json의 CRCL next_gate이자, correlation_matrix.yaml의 USDC_DISTRIBUTION_ECONOMICS 축(2026-08-15 신설, CRCL -M/COIN +M) 기준선 확정 재료다.

## 절차

1. state-audit 스크립트(.claude/skills/state-audit/scripts/state_audit.py) 실행으로 시작.
2. EDGAR에서 CRCL(Circle Internet Group)과 COIN(Coinbase Global) 양사의 2026-08-17 이후 신규 8-K를 조회하라 — .claude/skills/source-ingest/scripts/edgar_fulltext.py 사용(--ticker CRCL / COIN, --forms 8-K). Item 1.01(중요 계약 체결)·Item 1.02(계약 종료) 여부를 확인. 웹검색으로 양사 뉴스룸·보도자료도 교차 확인(애그리게이터 추정 라벨 금지 F1, 2차 매체는 삼각검증용 P4).
3. 판정 분기:
   - **8-K 발견 + 기존 조건 유지 갱신** → KC 미발동(변경 아님). 기준선 확정으로 기록. `run ticker CRCL`을 이어서 실행해 신규 1차 자료를 정식 처리(Claim·Delta·arbiter 판정 후보까지).
   - **8-K 발견 + 조건 변경(분배율·구조)** → KC-CRCL-3 발동 후보(경중 불문). COIN에 불리한 방향인지 판별(KC-COIN-4). 자동 실행 금지 — 사람 확인 요청 + 근거 패키지 제출로 종료(🔴🔴 처리 규약).
   - **8-K 부재** → 부재는 반증이 아니다(P5). unconfirmed로 기록하되, 8-K 제출 기한은 발효 후 4영업일(~2026-08-24)임을 사용자에게 알리고, 이 태스크를 사이드바에서 수동 재실행("Run now")해 재관측할 수 있음을 안내하라.
4. 결과를 사용자에게 보고: 발견 여부·Item 유형·조건 변경 유무·KC 판정·후속 조치. 모든 문장 fact/inference 태깅(P1). 매수·매도 지시 금지(P15).