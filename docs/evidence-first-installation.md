# Evidence-First 설치 및 연동

[English](evidence-first-installation.en.md) · [다국어 지원](../skills/evidence-first/references/languages.md)

배포 원본은 [`skills/evidence-first/`](../skills/evidence-first/SKILL.md)다. 특정 AI의 확장 필드나 자동 실행 훅 없이 Agent Skills의 `name`·`description` frontmatter와 Markdown을 사용한다. **전체 폴더**를 복사해야 상대 경로의 참고자료·양식·예제가 함께 동작한다. 설치 자체는 데이터 접근·외부 전송·쓰기 권한을 부여하지 않는다.

## 1. 검토할 버전 고정

Git이 있는 환경에서 공개 저장소를 복제한다. 다음은 설치 대상 프로젝트 밖의 임시 작업 폴더에서 실행한다.

```sh
git clone https://github.com/o-min222/enterprise-ontology-architecture.git
cd enterprise-ontology-architecture
git rev-parse HEAD
```

출력된 커밋을 기록하고 파일을 검토한다. 재현 설치는 `git checkout --detach <검토한-커밋-SHA>`로 그 커밋에 고정한다(꺾쇠 부분은 실제 값으로 교체). 이 저장소의 라이선스 부여 여부와 조직의 사용 정책은 별도로 확인한다. 이 패키지는 별도의 사용권을 새로 선언하지 않는다.

## 2. AI별 복사 위치

| 도구 | 프로젝트 설치 | 사용자 전체 설치 | 명시적 호출 |
| --- | --- | --- | --- |
| Codex | `<project>/.agents/skills/evidence-first/` | `~/.agents/skills/evidence-first/` | `$evidence-first` |
| Claude Code 로컬 세션 | `<project>/.claude/skills/evidence-first/` | `~/.claude/skills/evidence-first/` | `/evidence-first` |
| 다른 Agent Skills 지원 AI | 해당 제품이 문서화한 skill 검색 경로 | 제품별 경로 확인 | 제품별 방식 |

설치 위치는 [OpenAI 공식 문서](https://learn.chatgpt.com/docs/build-skills)와 [Claude Code 공식 문서](https://code.claude.com/docs/en/skills)를 기준으로 확인했다(2026-10-31). 도구별 버전·관리 설정·원격 세션의 검색 경로가 다를 수 있다. 위 표는 모든 제품에서 같은 폴더가 자동 인식된다는 보장이 아니다.

PowerShell 예시: **복제한 저장소 루트**에서 실행하며 첫 두 줄은 실제 대상과 원하는 제품에 맞게 수정한다. `codex` 또는 `claude` 중 하나씩 실행한다. 기본 사용자 폴더에는 자동 설치하지 않는다.

```powershell
$projectPath = 'C:\Projects\my-project'
$agentName = 'codex'
if ($agentName -notin @('codex', 'claude')) { throw 'codex 또는 claude를 선택하세요.' }
$skillSource = (Resolve-Path -LiteralPath './skills/evidence-first').Path
$agentFolder = if ($agentName -eq 'codex') { '.agents' } else { '.claude' }
$skillParent = Join-Path $projectPath "$agentFolder/skills"
$skillTarget = Join-Path $skillParent 'evidence-first'
if (Test-Path -LiteralPath $skillTarget) { throw '기존 설치가 있습니다. 차이를 검토하고 백업한 뒤 교체하세요.' }
New-Item -ItemType Directory -Path $skillParent -Force | Out-Null
Copy-Item -LiteralPath $skillSource -Destination $skillTarget -Recurse
Get-Content -LiteralPath (Join-Path $skillTarget 'SKILL.md') -TotalCount 5
```

macOS/Linux 예시: 역시 복제한 저장소 루트에서 시작한다. 대상 경로를 수정하고, Claude는 `.agents` 대신 `.claude`를 사용한다.

```sh
project_path='/path/to/my-project'
skill_parent="$project_path/.agents/skills"
skill_target="$skill_parent/evidence-first"
if [ -e "$skill_target" ]; then
  echo '기존 설치를 검토하고 백업한 뒤 교체하세요.'
else
  mkdir -p "$skill_parent" && cp -R skills/evidence-first "$skill_target"
fi
```

기존 폴더를 덮어쓰거나 현재 설치의 지침 파일을 통째로 교체하지 않는다. 같은 이름의 사용자·프로젝트 스킬이 동시에 있으면 제품별 선택 규칙을 확인한다.

## 3. 기본 행동 원칙으로 연결

스킬 설치는 관련 요청에서의 발견·호출을 지원한다. 매번 적용해야 하는 짧은 원칙은 프로젝트 지침에도 연결한다. 다음 문단을 **기존 AGENTS.md에 병합**하고 실제 설치 경로로 수정한다. Claude 전용 설치라면 `.claude/skills/`를 사용한다.

```markdown
근거에 의존하는 분석·코딩·운영 제안에서는
`.agents/skills/evidence-first/SKILL.md`를 읽고 적용한다.
공유 L1 원천 기록과 L2 정의를 권한 안에서 확인하고, 해석은 분리한다.
정보 유형과 검증 상태는 독립적으로 판단한다. 검증 수준은 영향에 비례한다.
중요한 주장에는 출처를 연결하고, 검증을 실행 권한으로 사용하지 않는다.
AI는 온톨로지를 활용하는 외부 주체다. 일반 표현 수정에 과도한 절차를 추가하지 않는다.
```

Claude Code에서 같은 정책을 사용하려면 프로젝트 루트의 기존 `CLAUDE.md`에 다음 한 줄을 **코드 블록 밖에** 추가한다. `AGENTS.md`와 나란히 둔다.

```markdown
@AGENTS.md
```

[공식 import 안내](https://code.claude.com/docs/en/memory#import-additional-files)에 따른 방식이다. Claude 전용 프로젝트라면 위 기본 원칙을 CLAUDE.md에 직접 병합하고 `.claude/skills/evidence-first/SKILL.md`로 연결할 수도 있다. 이 배포 저장소의 루트 AGENTS.md·CLAUDE.md는 **저장소 유지보수용**이므로 다른 프로젝트에 무조건 복사하지 않는다.

스킬 자동 발견이 없는 AI는 설치된 SKILL.md를 직접 읽도록 요청하고 필요한 참고자료만 제공한다. 프롬프트나 지침을 읽었다고 권한 통제가 생기는 것은 아니다. L1·L2 도구 접근과 서버 측 쓰기 통제를 별도로 구성한다.

## 4. 설치 확인·업데이트·제거

스킬 **설치**와 프로젝트의 저장 **초기 설정**은 별개다. 설치 후 “Evidence-First 초기 설정을 해줘”라고 요청하면 저장 방식(없음·Wiki·관계형 DB·그래프 DB·조합)과 활용 기능(기본 조회·관계 탐색·RAG)을 별도로 선택한다. 사용자가 이미 선택한 경우 다시 묻지 않는다. 일반 작업은 설정 없이 행동 원칙만 적용할 수 있다. 설정·이후 추가·이전 명령과 범위는 [설정 및 전환 절차](../skills/evidence-first/references/workspace-lifecycle.md), 사용 예는 [전환 예제](../skills/evidence-first/examples/setup-and-migration.md)를 참고한다.

로컬 보조 도구에는 Python 3.10 이상이 필요하다. Wiki·SQLite·키워드 RAG는 표준 라이브러리를 사용하고, Oxigraph 그래프 DB를 선택할 때만 선택 의존성을 설치한다. 설치와 실제 RAG 생성 흐름은 [그래프·RAG 안내](../skills/evidence-first/references/graph-and-rag.md)를 따른다. 기존 v1 설정은 그대로 읽고, 실제 구성 변경 시 이전 사본을 보존하며 v2로 갱신한다. 원격 DB·기존 Wiki는 AI가 별도 조사·매핑한다. 현재 보조 도구가 모든 DB나 Wiki의 자동 이전을 제공하는 것은 아니다.

AI는 실제 작업에서 필요를 발견하면 구성 변화를 먼저 제안할 수 있다. 기본은 현재 요청의 권한을 따르는 `task_scoped`다. 영구 정책이 필요할 때만 `.evidence-first/adaptation.json`을 만들고, 소유자가 `propose_only` 또는 허용 작업을 지정한 `scoped_auto`를 선택한다. 이미 특정 변경을 허용했다면 정책 파일이나 재승인을 강제하지 않는다. [환경 개선 절차](../skills/evidence-first/references/adaptive-environment.md), [정책 형식](../skills/evidence-first/assets/adaptation-policy.schema.json), [가상 사례](../skills/evidence-first/examples/adaptive-environment.md)를 참고한다. 예제 정책 복사는 실제 승인으로 취급하지 않는다.

AI는 [효율 비교와 학습](../skills/evidence-first/references/efficient-work.md)에 따라 기존 방법과 작은 대안을 비교하고 품질·출처·권한 조건을 유지하는 효율적인 방법을 찾는다. 반복 활용할 결과는 필요하고 허용될 때만 `.evidence-first/learning/` 같은 로컬 위치에 조건·측정·실패·한계와 함께 기록한다. 별도 설정 파일이나 상시 실험은 필수가 아니며, 이 경험은 모델 가중치 학습이나 새로운 실행 권한이 아니다.

1. 새 로컬 세션을 시작하고 스킬 목록/호출 기능으로 `evidence-first`가 보이는지 확인한다.
2. “Evidence-First로 예제의 최신 Wiki와 원본 충돌을 분석하고, 근거와 미확인 사항을 구분해줘”라고 요청한다. Codex에서는 `$evidence-first`, Claude Code에서는 `/evidence-first`로 명시 호출할 수 있다.
3. [가상 사례](../skills/evidence-first/examples/walkthroughs.md) 및 [행동 평가](../tests/scenarios.md)와 실제 응답·도구 실행을 비교한다. 모델이 파일을 실제 읽었는지와 적용한 버전을 확인한다.
4. 업데이트는 새 커밋을 별도 검토하고 기존 설치와 비교한 뒤, 백업을 보존하여 전체 폴더를 교체한다. 설치 커밋을 다시 기록한다. 심볼릭 링크·자동 업데이트·원격 스크립트 실행은 필요하지 않다.
5. 제거는 설치한 `evidence-first` 폴더와 직접 병합한 해당 지침만 제거하고 새 세션에서 확인한다. 원본 자료·다른 스킬·기존 정책은 삭제하지 않는다.

자동 검사는 [테스트 안내](../tests/README.md)를 따른다. 제품별 실제 설치/호출 여부와 행동 평가는 별도이며 자동 스키마 검사만으로 보장되지 않는다.

## 형식 근거

이식 가능한 파일 구조와 frontmatter는 [Agent Skills 명세](https://agentskills.io/specification)를 따른다. 이 저장소의 L1·L2와 다섯 정보 유형은 프로젝트의 작업 모델이며 Agent Skills 표준이 정의한 분류라고 주장하지 않는다.

## 언어 선택

표준 SKILL.md는 영어 진입점이며 한국어 지침은 SKILL.ko.md에 보존한다. 언어별 스킬을 중복 설치하지 않고 전체 폴더의 동일한 스킬을 사용한다. AI는 요청 언어로 응답한다. 생성 Wiki 안내·RAG 규칙은 명령 앞의 `--lang ko` 등으로 선택하며 `en`·`ko`·`ja`·`zh`를 제공한다. 다른 언어는 도구 메시지의 영어 대체를 표시하고 AI가 요청 언어로 설명한다. CLI 옵션·JSON 키·기술 오류는 영어를 유지한다.

원문·ID·분류·권한은 번역하지 않는다. 로컬 RAG는 자동 번역/의미 검색이 아니며 언어가 다르면 원래 질문을 유지한 채 `--search-query`로 원문 검색어를 별도 전달할 수 있다. CJK 검색용 색인 형식은 버전 2이며 기존 버전 1은 승인 범위에서 다시 만든다. 출력 언어 변경만으로 현재 색인을 다시 만들지 않는다.
