# 플러그인 사용 안내

[English](plugin-guide.md) · [처음으로](../README.md)

Evidence-First 0.1.1은 이 저장소에서 배포하는 스킬 중심의 미리보기 플러그인입니다. OpenAI·Anthropic 공식 디렉터리에 등록된 상태는 아닙니다. 별도 계정·API 키·MCP 서버·백그라운드 서비스 없이 시작하며, 실제 도구와 권한은 사용하는 AI 호스트가 관리합니다.

## 설치와 첫 사용

### Codex CLI / 지원되는 OpenAI 클라이언트

```sh
codex plugin marketplace add o-min222/enterprise-ontology-architecture
codex plugin add evidence-first@evidence-first-plugins
```

새 대화에서 `$evidence-first-setup`으로 초기 설정하거나 `$evidence-first`로 일반 작업을 시작하세요. 클라이언트와 버전에 따라 지원 범위가 다릅니다. 명령을 지원하지 않으면 [핵심 스킬 단독 설치](evidence-first-installation.md)를 사용하세요. 이 저장소를 신뢰한 프로젝트로 열면 지원 클라이언트의 로컬 플러그인 탐색에서도 저장소 카탈로그를 사용할 수 있습니다. 활성화 여부는 클라이언트에서 확인하세요.

### Claude Code

대화창에서 실행합니다.

```text
/plugin marketplace add o-min222/enterprise-ontology-architecture
/plugin install evidence-first@evidence-first-plugins
```

새 세션에서 `/evidence-first:evidence-first-setup` 또는 `/evidence-first:evidence-first`를 호출하세요. 설치 없이 로컬 저장소를 시험하려면 `claude --plugin-dir "저장소의 절대경로"`를 사용할 수 있습니다.

### 다른 코딩 AI

`skills/evidence-first` 폴더 전체를 호스트가 지원하는 위치에 복사하거나 프로젝트 지침에서 SKILL.md를 참조하세요. [AGENTS.md·CLAUDE.md 연동 및 설치 상세](evidence-first-installation.md)를 따릅니다. 초기 설정 스킬도 원하면 두 스킬 폴더를 형제 폴더로 함께 설치하세요. 핵심 스킬은 단독으로 쓸 수 있습니다.

기존 AGENTS.md나 CLAUDE.md는 덮어쓰지 말고 짧은 참조를 병합하세요. 저장소의 루트 지침은 연동 예시이며 다른 프로젝트에 자동 복사되지 않습니다. 설치만으로 모든 AI가 매번 자동 적용한다고 보장할 수 없으므로 필요하면 명시적으로 호출하세요.

## 첫 요청 예시

| 요청 | 기대 동작 |
| --- | --- |
| “이 두 공개 자료를 Evidence-First로 비교해서 스페인어로 설명해줘.” | 스페인어 답변, 원문 출처, 해석 구분, 필요한 수준의 검증. DB 불필요 |
| “이 프로젝트에 한국어 파일 Wiki를 설정해줘. RAG는 아직 필요 없어.” | 대상과 기존 설정 확인, 허용된 Wiki 생성, 실제 상태 확인, 한국어 표시 |
| “기존 SQLite 기록에 RAG를 추가해줘.” | 기준 저장소 확인, 파생 검색 색인 생성, 출처가 있는 검색 문맥 전달 |
| “관계 찾기가 반복돼서 느려. 더 효율적인 방법을 찾아줘.” | 작은 비교와 구체적 제안, 기존 권한 내 실행, 실제 효과 또는 불확실성 보고 |

초기 설정에서는 저장 방식(없음·Wiki·SQLite·그래프·조합), 기준 저장소, 기능(RAG·관계 탐색), 언어, 환경 개선 선호를 구분합니다. 일반 작업에 저장소나 반복 승인을 강요하지 않습니다. [가상 예제](../skills/evidence-first/examples/README.md)로 시작할 수 있습니다.

행동 지침만 쓸 때는 Python이나 추가 패키지가 필요 없습니다. 로컬 도우미는 Python 3.10 이상, RAG는 SQLite FTS5가 필요합니다. 그래프 사용 시에만 `skills/evidence-first/requirements-graph.txt`의 선택 의존성이 필요합니다. 도우미의 `--root`는 대상 프로젝트이고 `--lang`은 표시 언어입니다. 설치된 플러그인 폴더에 프로젝트 기록을 저장하지 마세요.

## 업데이트와 제거

[변경 이력](../CHANGELOG.md)을 검토하고 프로젝트 기록을 백업하세요. 검토한 구성을 재현하려면 Git 커밋을 고정·기록하세요. Codex의 카탈로그 추가는 `--ref COMMIT`을 지원합니다. 수동 설치 시 이전 폴더를 보존하고, 서로 다른 버전의 스크립트를 섞지 마세요.

Codex는 `codex plugin marketplace upgrade --help`에서 현재 버전의 갱신 방법을 확인하고, 갱신 후 `codex plugin list`와 새 대화에서 상태를 확인하세요. 제거는 `codex plugin remove evidence-first@evidence-first-plugins`입니다. Claude Code는 `/plugin marketplace update evidence-first-plugins`, `/plugin update evidence-first@evidence-first-plugins` 순서로 갱신한 뒤 세션을 다시 시작합니다. 제거는 `/plugin uninstall evidence-first@evidence-first-plugins`입니다.

플러그인을 제거해도 프로젝트 기록·설정·색인·백업은 남습니다. 삭제는 소유자의 의사와 보존 정책에 따라 별도로 수행해야 합니다. 업데이트가 자동으로 데이터 이전이나 동기화를 실행하지는 않습니다. 구성 변경은 기존의 미리보기·복사·비교·전환 절차를 따르며 원본을 보존합니다.

## 문제 해결

- 플러그인이 보이지 않으면 호스트 버전, 카탈로그, 활성화 여부와 새 세션을 확인하세요. 미지원 호스트는 단독 스킬 설치를 사용하세요.
- 스킬이 선택되지 않으면 직접 호출하고, 상시 원칙은 프로젝트 지침에 참조를 연결하세요.
- 그래프 의존성이 없으면 선택한 환경에 그래프 패키지만 설치하거나 현재 저장소를 계속 사용하세요.
- RAG 색인이 오래되었다면 기준 원천의 변경을 확인하고 다시 만드세요. 검색 순위는 검증 결과가 아닙니다.
- 미지원 언어 태그의 도구 메시지는 영어 대체를 명시합니다. AI의 요청 언어 답변은 가능합니다. 영·한 상세 지침, 일·중 빠른 시작/메시지, 다른 언어 응답은 서로 다른 지원 수준입니다.

[지원/라이선스 상태](../SUPPORT.md) · [개인정보](../PRIVACY.md) · [보안](../SECURITY.md). [MIT 라이선스](../LICENSE)로 배포합니다. 복사·재배포 시 저작권·허가 고지를 보존하세요. 외부 의존성과 참조 자료의 조건은 별개입니다.

## 배포와 검증

루트 `plugin.json`이 공통 배포 정보를, `.claude-plugin/plugin.json`이 Claude 호환 정보를 제공합니다. 두 버전은 일치해야 합니다. `skills/`에 핵심·설정 스킬이 있고, OpenAI 표시 정보는 루트 확장과 각 스킬의 `agents/openai.yaml`에 있습니다. 두 호스트의 저장소 카탈로그는 같은 패키지를 가리킵니다.

기여자는 [테스트](../tests/README.md), 가능한 경우 Claude의 네이티브 매니페스트 검증을 수행하고 검토한 파일을 스테이징한 뒤 `python scripts/package_plugin.py`를 실행합니다. ZIP에는 Git에 등록된 공개 파일과 원천 트리·파일별 SHA-256을 담은 BUILD-INFO.json이 들어갑니다. 등록되지 않은 로컬 데이터는 수집하지 않으며, 알려진 실행 데이터 경로나 미등록 수정 사항은 거부합니다. 내용의 공개 가능 여부를 자동 보장하는 비밀정보 탐지기는 아니므로 배포 내용을 검토해야 합니다. CI 결과물은 공식 디렉터리 등록이나 GitHub Release와 구분됩니다.

2026-10-31 기준 형식 출처: [OpenAI](https://developers.openai.com/plugins/build/plugins), [Agent Plugins](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json), [Claude 매니페스트](https://code.claude.com/docs/en/plugins-reference), [Claude 카탈로그](https://code.claude.com/docs/en/plugin-marketplaces). 실제 검증 범위는 [검증 기록](../tests/validation-report.md)에 구분해 기록합니다.
