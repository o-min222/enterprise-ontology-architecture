# Support

Use [GitHub Issues](https://github.com/o-min222/enterprise-ontology-architecture/issues) for bugs, feature requests, installation questions, and translation corrections. Use your preferred language. Include the commit/version, AI host version, Python version if helpers are involved, selected storage/features, and a synthetic reproduction. There is no promised response time or commercial support service.

Before reporting, read the [plugin guide](docs/plugin-guide.md), [installation guide](docs/evidence-first-installation.en.md), [examples](skills/evidence-first/examples/README.en.md), and [test scope](tests/README.en.md). For private reports see [SECURITY.md](SECURITY.md).

## Compatibility and limits

| Surface | Package support | Verification |
| --- | --- | --- |
| Portable skill hosts | Core folder with standard SKILL.md | Copy-isolation and link tests |
| Codex / supported OpenAI plugin clients | Root plugin.json, repo marketplace, setup and skill UI metadata | Schema/structure checks; host installation varies by client |
| Claude Code | Native plugin and marketplace manifests; namespaced skills | Native manifest validation; see validation report for observed version |
| Other coding AIs | Read/import the core guidance using the host's supported mechanism | No blanket compatibility claim or host-specific enforcement |
| Local helpers | Python 3.10+; SQLite FTS5 for RAG; optional PyOxigraph for graph | Automated helper tests; CI matrix defines tested platforms |

No remote database connector, vector embeddings, hosted synchronization, background monitoring, or bundled model API is provided. Retrieval prepares cited context; the calling AI generates answers. Behavioral guidance is probabilistic and cannot guarantee future model actions.

## License status

This repository is distributed under the [MIT License](LICENSE). Preserve its copyright and permission notice in copies or substantial portions. Third-party dependencies and referenced external material retain their own terms. Both plugin manifests declare the SPDX identifier `MIT`; each standalone skill includes a copy of the license.

한국어: 설치·오류·번역 문의는 원하는 언어로 이슈에 남길 수 있습니다. 사용 버전과 가상 재현 사례를 포함하고 민감정보는 제외해 주세요. [MIT 라이선스](LICENSE)로 배포하며, 복사·재배포 시 저작권·허가 고지를 보존해야 합니다. 외부 의존성과 참조 자료의 조건은 별개입니다.
