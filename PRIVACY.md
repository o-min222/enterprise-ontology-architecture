# Privacy and data handling

The bundled Python helpers run locally. This package contains no telemetry, hosted backend, model API client, or automatic external translation. Installing a dependency or cloning/updating the repository contacts the selected package host. Your AI host and any additional tools have their own data handling and permissions; a local helper does not make the overall AI session offline.

Project configuration and local write history live under the target project's `.evidence-first/`. Wiki/SQLite/graph records live under `knowledge/` by default; derived retrieval indexes may contain source text and metadata. These paths are ignored at this repository's root, but each target project needs its own ignore/access/backup rules. Git ignore rules are not security controls.

Treat indexes, logs, backups, and translated excerpts as potentially sensitive. Retain source provenance inside the authorized project; do not publish private originals, personal data, credentials, internal URLs, or operational metadata to this public repository. Use synthetic samples when reporting problems. Removing a store is not automatic erasure of copies, backups, or Git history.

The packaging helper reads only staged Git blobs and rejects common runtime/private paths. It does not detect every secret or determine whether content is public. Review staged content and the final archive. Plugin manifests describe capabilities; the AI host enforces actual access and execution permissions.

한국어: 도우미는 로컬에서 작동하며 자체 원격 분석 기능이 없습니다. AI 서비스와 추가 도구의 개인정보 처리는 별개입니다. 기록·검색 색인·백업에는 민감정보가 담길 수 있으므로 공개 저장소에 올리지 마세요. 배포 파일에도 등록된 내용만 들어가지만 공개 가능 여부는 검토해야 합니다.
