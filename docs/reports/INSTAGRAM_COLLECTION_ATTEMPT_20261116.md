# 2026-11-16 Instagram 수집 실행 결과

사용자의 SNS 수집 시작 요청으로 Meta 공식 API 수집기를 실제 실행했다. 결과는 **API 접근 차단으로 미실행**이며 신규 게시물·이미지 저장은 0건이다. 기존 행사 데이터는 보존했다.

- 수집 전 토큰 검증 `/debug_token`: HTTP 400, Meta code 200, subcode 5258005.
- 원인 구분을 위한 기존 Instagram 계정 읽기 `id,username`: 동일 오류.
- 비밀 값과 URL을 가린 Meta 응답 문구: `API access blocked.`
- 토큰 만료 여부·새 scope 누락 여부는 이 응답만으로 확정할 수 없다. API 버전을 바꾸거나 비공식 로그인 수집으로 우회하지 않았다.
- 앱·계정의 접근 제한 상태는 Meta 개발자 대시보드의 알림·앱 상태에서 계정 소유자가 확인해야 한다. 제한이 해소된 후 새로운 보고서 폴더로 재실행한다.

원본 안전 진단: `data/private/instagram/20261116_collection/availability.json`. 해당 파일에는 토큰과 앱 비밀 값이 저장되지 않는다. 번역·분류 전용 작업은 중단하지 않았다.
