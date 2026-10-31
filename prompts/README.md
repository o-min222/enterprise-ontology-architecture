# 실무 구축 프롬프트

이 프롬프트는 **자신의 코딩형 AI에 입력하는 출발점**이다. 실제 파일·DB 수정 전 반드시 승인받고, 기업 데이터의 외부 전송 정책을 확인한다.

- [로컬 Markdown Wiki 구축](local-llm-wiki.md)
- [PostgreSQL 공통 모델 구축](postgresql-setup.md)
- [검증 및 복구 점검](validation.md)

공통 분류:
- `information_type`: observation, hypothesis, reviewed_assessment, official_decision, execution_result
- `verification_status`: unverified, in_review, verified, disputed

두 축은 독립적이다. 유형 간 순차 전이를 가정하지 않는다.
