---
name: version-publish
description: approve 명령 처리 후 사용. 승인 큐 관리, ThesisPatch 적용(백업+이력), 버전 발행(네이밍·덮어쓰기 차단·docs 격리)을 수행한다.
---

# version-publish — 승인 처리·발행 (S8, D6·D10)

## 실행

```bash
# 승인/반려 (큐 갱신 + 유형별 후속 자동 실행)
python .claude/skills/version-publish/scripts/approvals.py approve <approval_id>
python .claude/skills/version-publish/scripts/approvals.py reject <approval_id> --note "<사유>"
python .claude/skills/version-publish/scripts/approvals.py list

# 발행 (approved 건만)
python .claude/skills/version-publish/scripts/version_publish.py --artifact <path> --doc-type <유형>
```

## approve 후속 처리 (D10)

- `type: thesis_patch` → ① `state/thesis_cards/{T}.yaml`을 `state/thesis_cards/backup/{T}_{ts}.yaml`로 백업 ② 패치의 before→after 적용 ③ 카드 `version_history`에 정정 이력 추가(P9)
- `type: version_publish` → version_publish.py 호출

## 발행 규칙

- 네이밍: `종목_문서유형_vN_YYYYMMDD.md`. **기존 파일 존재 시 발행 중단(덮어쓰기 절대 금지, P9) → 에스컬레이션**
- 발행본을 `docs/`로 복사(F2 대체 가드) + 변경 이력 표 갱신 + 「정정 고지」 블록
- 종료 시 출력: "발행 완료. docs/ 격리됨. 주기적 백업(외부 저장소)을 권장합니다."

## 금지: 승인 없는 발행·카드 쓰기(F17·F19). expired 건 approve 시도 → 거부 + 재실행 안내.
