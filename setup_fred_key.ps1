# FRED API 키 설정 도우미 (R1)
# 사용법: 이 파일을 우클릭 → "PowerShell로 실행", 또는 PowerShell에서:
#   powershell -ExecutionPolicy Bypass -File setup_fred_key.ps1
# 발급받은 키를 붙여넣으면 → FRED에 실제 호출로 검증 → 통과 시에만 영구 저장(setx)합니다.

Write-Host "=== FRED API 키 설정 ===" -ForegroundColor Cyan
Write-Host "키가 없다면: https://fredaccount.stlouisfed.org/apikeys 에서 발급 (무료, 이메일만 필요)"
Write-Host ""

$key = Read-Host "발급받은 FRED API 키를 붙여넣고 Enter"
$key = $key.Trim()

# 형식 검사: FRED 키는 32자리 소문자 영숫자
if ($key -notmatch '^[a-z0-9]{32}$') {
    Write-Host "⛔ 키 형식이 아닙니다 (32자리 소문자 영숫자여야 함). 입력값 길이: $($key.Length)" -ForegroundColor Red
    Write-Host "   발급 페이지에서 키를 정확히 복사했는지 확인하세요."
    exit 1
}

# 실제 호출 검증 (DGS30 최신 1건)
Write-Host "FRED에 검증 호출 중..."
try {
    $resp = Invoke-RestMethod -TimeoutSec 30 -Uri ("https://api.stlouisfed.org/fred/series/observations?series_id=DGS30&api_key=$key&file_type=json&sort_order=desc&limit=1")
} catch {
    Write-Host "⛔ 검증 실패: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   키가 잘못됐거나 네트워크 문제입니다. 저장하지 않았습니다."
    exit 1
}
if (-not $resp.observations) {
    Write-Host "⛔ 응답에 데이터가 없습니다. 저장하지 않았습니다." -ForegroundColor Red
    exit 1
}
$obs = $resp.observations[0]
Write-Host "✅ 검증 성공 — 30Y 국채금리 최신값: $($obs.value)% (as_of $($obs.date))" -ForegroundColor Green

# 영구 저장 (사용자 환경변수)
[Environment]::SetEnvironmentVariable("FRED_API_KEY", $key, "User")
Write-Host "✅ FRED_API_KEY 영구 저장 완료 (사용자 환경변수)" -ForegroundColor Green
Write-Host ""
Write-Host "주의: 이미 열려 있는 터미널·Claude Code에는 반영되지 않습니다 — 새로 열어야 적용됩니다."
