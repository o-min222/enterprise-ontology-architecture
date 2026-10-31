# 검증 실행

스킬을 읽는 데 Python은 필요하지 않다. 다음 의존성은 개발용 검사에만 사용한다. 저장소 루트에서 Python 3.10 이상으로 실행한다.

선택적 로컬 설정/이전 보조 도구도 Python 3.10 이상에서 실행되며 표준 라이브러리만 사용한다. 아래 개발용 패키지를 설치하지 않아도 보조 도구는 동작한다.

```sh
python -m venv .venv
```

가상환경을 활성화한다: Windows PowerShell은 `.venv\Scripts\Activate.ps1`, macOS/Linux는 `source .venv/bin/activate`. 조직 정책상 활성화가 제한되면 가상환경의 Python 실행 파일을 직접 사용한다.

```sh
python -m pip install -r requirements-test.txt
python -m unittest discover -s tests -v
git diff --check
```

검사 범위: 표준 frontmatter, 패키지만 복사한 상태의 로컬 참고 경로, JSON Schema 유효성, 5×4 독립 조합, 잘못된 유형·상태, 검증 근거 누락, 가상 기록의 스키마 및 출처 연결. 단위 테스트의 조합 생성은 형식 검사이며 그 조합의 실제 진실성을 입증하지 않는다.

로컬 구성 검사는 네 초기 선택, DB 직접 추가, 기준 저장소 유지, 부작용 없는 이전 계획, Wiki↔SQLite 전체 기록 대조, 공통 자료·원본 보존, 충돌·전환 실패·잘못된 기록·잠금·기존 저장소 보호, 독립된 SQLite CHECK 제약을 실제 임시 파일과 DB로 확인한다. 설치 폴더만 복사한 상태에서 외부 패키지 없이 보조 도구가 실행되는지도 검사한다.

[scenarios.md](scenarios.md)는 모델의 실제 판단과 도구 사용을 평가한다. 자동 테스트 통과가 모든 AI의 지침 준수·보안·접근 권한을 보장하지 않는다. 실제 제품별 호출과 모델 평가 결과는 제품·모델·버전·시각·실행 로그와 함께 따로 기록한다.

이번 구현에서 실제 실행한 검사와 미검증 범위는 [검증 기록](validation-report.md)에 정리했다.

기존 문서 보존 확인은 변경 전 커밋과 비교한다. 예를 들어 `git diff <기준-커밋> -- docs/ prompts/`에서 기존 파일 변경을 확인하고, 의도한 새 설치 안내 외의 수정이 없는지 검토한다.
