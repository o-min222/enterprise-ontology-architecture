# 로컬 LLM Wiki 구축 프롬프트

다음 내용을 파일 접근이 가능한 코딩형 AI에 입력하세요.

```text
너는 로컬 파일을 다루는 데이터 아키텍트다.
[작업 경로]에 Markdown 지식베이스를 구축해줘.

파일 작업 전에 기존 파일을 읽기 전용으로 조사하고, 생성·수정할 파일 목록과 백업·롤백 계획을 제시한 뒤 내 승인을 기다려.

폴더:
sources/ 원본의 읽기 전용 캐시 또는 참조
entities/ 공통 객체 ID와 관계
claims/ 누가 무엇을 주장했는지와 출처
analyses/ 가설·추정·검토된 평가
decisions/ 공식 판단·실행 결과
schemas/ 필드·관계·버전

각 기록에 id, entity_ids, source_ids, information_type,
verification_status, created_at, author_or_model, version을
YAML frontmatter로 정의해.

information_type:
observation | hypothesis | reviewed_assessment |
official_decision | execution_result

verification_status:
unverified | in_review | verified | disputed

원본을 임의 수정하지 말고 해석이 공통 사실을 덮어쓰지 못하도록 규칙을 작성해.
모든 예시 데이터는 '가상'으로 표시하고 실제 기업 데이터를 외부에 전송하지 마.
검색은 ID·파일명·본문 검색부터 시작하고 RAG는 필요성이 확인된 뒤 제안해.
생성 후 구조, 검증 방법, 복구 절차를 보고해.
```

## 저장 매핑
| 유형 | Wiki |
|---|---|
| observation | sources/ (발언 기록은 claims/에서 참조) |
| hypothesis, reviewed_assessment | analyses/ |
| official_decision, execution_result | decisions/ |

`claims/`는 정보 유형이 아니라 출처가 있는 주장 기록이다.
