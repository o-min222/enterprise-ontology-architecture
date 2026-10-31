# PostgreSQL 공통 모델 구축 프롬프트

```text
너는 PostgreSQL 데이터 모델러다. 다음 업무에 필요한 최소 객체 3~5개로
공통 의미 모델을 설계해줘: [업무 설명].

먼저 기존 DB의 스키마를 읽기 전용으로 점검해. 실제 변경은 하지 마.
다음 산출물을 작성해:
1) 핵심 객체, PK/FK, 관계, 공통 ID와 원천 ID 매핑
2) source_record, entity, entity_link, assertion,
   interpretation, decision_event, execution_event,
   ontology_schema_version의 역할
3) information_type 5종과 verification_status 4종의 독립 필드
4) 원본 출처, 수정 이력, 접근 권한, 감사 로그
5) DDL, 테스트용 가상 데이터, 무결성 테스트, 롤백 SQL
6) RDBMS만으로 충분한지와 추가 인프라의 필요성 및 비용

운영 DB에 접속하거나 마이그레이션을 실행하기 전 변경 계획과
백업·복구 방법을 보여주고 명시적인 승인을 기다려.
실제 개인정보와 비밀정보를 외부에 전송하지 마.
```
