# 정보 모델: 두 개의 독립 축

L1은 원천 기록, L2는 객체·속성·관계·정의·제약의 공통 모델이다. 개인·부서·AI의 해석은 작성자와 목적을 가진 별도 기록이다. L3의 앱·BI·AI는 이 자료를 활용한다. 이 구분은 저장 기술이나 DB 선택을 강제하지 않는다.

## 분류

| information_type | 예 | 검증과 구분할 점 |
| --- | --- | --- |
| observation | 센서가 정지를 기록함 | 센서 기록이 있어도 실제 정지 시간은 분쟁 중일 수 있음 |
| hypothesis | 냉각 이상이 원인일 가능성 | 가정·범위를 정해 검증했어도 보편적 사실로 승격하지 않음 |
| reviewed_assessment | 정비팀이 기준 R2로 위험 평가 | 검토가 수행됐다는 것과 평가의 타당성은 별개 |
| official_decision | 위원회가 점검을 결정 | 채택 권한·일시와 결정 내용의 타당성은 별개 |
| execution_result | 점검 API가 작업을 생성함 | 응답 기록이 있어도 실제 완료 여부는 미확인일 수 있음 |

`verification_status`:

- `unverified`: 이 기록의 명시된 범위를 아직 확인하지 못함.
- `in_review`: 명시된 범위를 확인 중. 진행 중이라는 이유로 결론을 확정하지 않음.
- `verified`: `verification.scope`를 `method`와 `evidence_refs`로 확인함. 유효 기간·대상·조건 밖으로 일반화하지 않음.
- `disputed`: 명시된 범위에 반박 또는 충돌하는 근거가 있음. 거짓으로 최종 확정했다는 뜻은 아님.

5×4 조합 모두 허용한다. `reviewed_assessment/unverified`, `official_decision/disputed`, `execution_result/in_review`도 정상이다. 두 필드는 순차적 파이프라인, 신뢰 점수, 승인 등급이 아니다. 검증 상태 변경만으로 정보 유형을 바꾸지 않는다. 가설을 채택한 결정이나 실제 실행은 원래 기록을 덮어쓰지 않고 새 기록으로 연결한다.

발언이 있었다는 관측과 발언 내용의 진위는 별도 주장으로 나눈다. 예: “위원회가 안전하다고 결정했다”는 존재가 확인된 결정이며, “설비가 안전하다”는 별도 평가다. 두 주장을 한 레코드의 `verified`로 묶지 않는다.

## 선택적 교환 형식

[assertion.schema.json](../assets/assertion.schema.json)은 지속 보존할 **단일 주장**의 JSON Schema다. 스킬 실행이나 짧은 답변에 JSON 저장을 강제하지 않는다. 기존 시스템 필드에는 의미를 보존하는 매핑을 사용한다.

| 필드 | 의미 |
| --- | --- |
| schema_version | 이 교환 형식 버전 (`1.0`) |
| id / entity_ids | 주장 ID / L2 객체 ID. 객체가 불명확하면 빈 배열 |
| statement | 한 범위의 주장 |
| information_type / verification_status | 위의 독립 분류 |
| author_or_model / created_at / version | 작성자 또는 모델·작성 시각·기록 버전 |
| source_refs | 출처 ID, 원본 위치·버전·접근 시각, 접근 가능 여부 |
| semantic_context | L2 모델 ID·버전·사용 정의. 모델이 없으면 `null` |
| verification | 확인 범위·방법·근거 출처 ID. 미확인은 그 한계를 기록 |

검증 근거 ID는 해당 `source_refs`를 참조한다. `verified`는 빈 근거 목록을 허용하지 않는다. 출처가 없는 가설은 `source_refs: []`와 `unverified`로 기록할 수 있다. 원본 미접근 출처는 `availability: unavailable`, `accessed_at: null`로 표시한다. 근거 출처의 일부만 접근 가능하면 무엇을 확인했는지 범위를 좁힌다.

스키마는 필드 형식을 검사할 뿐, 출처의 진위·유효한 접근권·검증의 질·실행 권한을 보장하지 않는다. ID 연결과 접근 여부는 도구·사람이 별도로 확인해야 한다. 기록에 권한 토큰이나 자격증명을 넣지 않는다.
