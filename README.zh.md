> 插件版 0.1.0 preview：[安装与更新 (English)](docs/plugin-guide.md) · [한국어 안내](docs/plugin-guide.ko.md)。尚未在官方目录上架。

# Evidence-First：中文快速入门

[한국어](README.md) · [English](README.en.md) · [日本語](README.ja.md) · 中文

本技能使用共享原始记录（L1）和语义模型（L2），独立保留个人、部门及AI的解读，按风险比例验证，并追踪来源、区分判断与执行权限。AI是外部使用者，不是本体的必要组成部分。

1. 按照[英文安装指南](docs/evidence-first-installation.en.md)复制整个 skills/evidence-first 文件夹。
2. 告诉AI：“使用 Evidence-First，并用中文回答。”标准 [SKILL.md](skills/evidence-first/SKILL.md) 使用英文，但不要求AI只能用英文回答。
3. 分别选择存储方式（无、Wiki、SQLite、图数据库或组合）和功能（基本查询、关系查询、RAG），之后可按需添加或迁移。
4. AI可在已有授权范围内提出、执行并验证必要改进；现有方式足够时保持简单。

```sh
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" --lang zh init --mode wiki
python "PATH_TO_SKILL/scripts/workspace.py" --root "PROJECT" enable rag
python "PATH_TO_SKILL/scripts/rag.py" --root "PROJECT" build
python "PATH_TO_SKILL/scripts/rag.py" --root "PROJECT" --lang zh retrieve --question "冷却原因是否已确认？" --search-query "cooling cause"
```

将 PATH_TO_SKILL 和 PROJECT 替换为实际路径。最后一条命令示范如何为英文资料使用来源语言关键词。RAG只索引已登记的记录，实际使用前需在权限范围内准备资料。

Wiki标签和RAG生成规则提供简体中文目录。CLI选项、JSON键和技术错误信息保留英文，AI可用中文解释。参阅[多语言支持范围](skills/evidence-first/references/languages.md)及[虚构英文样例](skills/evidence-first/examples/README.en.md)。

语言选项不会改变原文、ID、information_type、verification_status或权限。翻译说明不等于原始证据或已验证事实。这里没有宣称所有参考文档均已有审阅过的中文译本；AI可参考维护的英文或韩文指南进行说明。
