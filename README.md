# CNKI Art Thesis Writer

**中国知网（CNKI）艺术类论文检索、下载与论文章节撰写自动化工作流**

---

## 简介

本项目是为中国艺术学专业硕士研究生设计的 AI 辅助研究工具，覆盖从文献检索到论文章节撰写的完整流程。作为 AI 代理（Claude Code / OpenCode）的技能包（skill），它通过与 AI 模型的协作，提供结构化的、可追溯的学术研究支持。

### 核心能力

| 环节 | 能力 | 输出 |
|------|------|------|
| **检索** | 按关键词、期刊、作者、年份等多维度搜索 CNKI | 结构化候选文献列表（JSON） |
| **筛选** | 相关性评分，分层为精读/泛读 | 排序后的文献清单 |
| **下载** | Playwright 自动化下载 PDF/CAJ | 本地文件 |
| **观点提取** | 逐篇阅读，提取论点、概念、案例，记录页码 | 观点-来源矩阵 |
| **撰写** | 按学术规范撰写章节正文 | 章节草稿 |
| **审查** | 质量自动检查：出处完整性、页码可验证性 | 审查报告 |
| **交付** | 生成 .docx 文档 | 完整 Word 文档 |

---

## 项目结构

```
cnki-art-thesis-writer/
├── SKILL.md                  # 技能入口（AI 代理调用入口）
├── agents/
│   └── cnki-researcher.md    # 全流程编排器（7 阶段流水线）
├── skills/
│   ├── cnki-search/          # CNKI 检索子技能
│   │   ├── SKILL.md
│   │   └── scripts/cnki_search.py
│   ├── cnki-download/        # 文献下载子技能
│   │   ├── SKILL.md
│   │   └── scripts/cnki_download.py
│   └── thesis-draft/         # 论文章节撰写子技能
│       └── SKILL.md
├── references/
│   ├── cnki-strategy.md      # 艺术类检索关键词策略
│   ├── gb-t-7714.md          # GB/T 7714 参考文献格式
│   └── output-spec.md        # 文体规范与输出格式
├── cnki-flowchart.html       # 流程示意图（Mermaid）
└── README.md
```

---

## 工作流程

```
[P0] 初始化会话
   ↓
[P1] CNKI 检索（4 层关键词策略，目标 ≥20 篇）
   ↓                       ↗ 文献不足？
[P2] 筛选与评分（精读 5 篇 + 泛读 15 篇）
   ↓
[P3] 下载文献（Playwright 自动化）
   ↓
[P4] 阅读与观点提取（构建观点-来源矩阵）
   ↓
[P5] 撰写章节（证据优先，[n]page 引用格式）
   ↓
[P6] 质量审查 ← ← ← ← ← ← ← ← ←
   ├─ 每段 ≥1 出处？ → 否 → 回 P5
   ├─ 页码可验证？   → 否 → 回 P1 ↗
   └─ 综合评分 ≥70% → 继续
   ↓
[P7] 交付 .docx（正文 + 矩阵 + 参考文献 + 待确认项）
```

### 会话目录结构

每次研究会话自动创建独立目录，支持中断恢复：

```
sessions/{主题}_{YYYYMMDD}/
├── session.json          # 用户参数
├── progress.json         # 阶段进度
├── papers/
│   ├── candidates.json   # 检索候选
│   ├── ranked.json       # 排序结果
│   └── downloaded/       # 下载文件
└── draft/
    ├── matrix.json       # 观点-来源矩阵
    ├── chapter.md        # 章节草稿
    └── references.json   # 参考文献
```

---

## 使用方式

### 作为 AI 代理技能（推荐）

本技能设计用于 AI 编程助手（如 Claude Code、OpenCode）。将项目放置到 AI 工具的 skills 目录后，即可直接与代理对话使用：

**OpenCode + oh-my-openagent**（安装后）：
```
/cnki-researcher 帮我查找"战国楚漆器纹样"的文献
```

**Claude Code**：
```
请读取 cnki-art-thesis-writer/SKILL.md，然后执行全流程
```

### 直接使用 Python 脚本

```bash
# 检索
python skills/cnki-search/scripts/cnki_search.py --keyword "楚漆器 纹样" --source-category CSSCI --save results.json

# 下载
python skills/cnki-download/scripts/cnki_download.py --batch results.json --download-dir ./papers --profile-dir ./session
```

---

## 前置条件

- Python 3.8+（运行 Playwright 脚本）
- Playwright：`pip install playwright && python -m playwright install chromium`
- Chrome/Chromium 浏览器
- 有效的 CNKI 机构登录或校外访问权限
- Node.js >= 18（可选，用于 Chrome DevTools MCP 自动化路径）

---

## 设计原则

1. **可追溯性**：每个核心观点必须关联到具体文献和页码，不生成无法验证的内容
2. **证据优先**：段落以考古事实、数据、文献引文开头，再进行分析阐释
3. **质量控制**：自动审查确保每段有出处、页码真实、引用格式完整
4. **中断恢复**：会话持久化，支持随时暂停和继续
5. **边界意识**：不绕过 paywall 或 DRM，不复制大段原文

---

## 许可

MIT License
