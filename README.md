# 读书精读教练 · reading-coach

把 AI 从「摘要工具」改造成「精读教练」：不替你读书，先让你开口，再告诉你抓住了什么、漏掉了什么、理解偏了什么。

**一个内核，一套产物，跑在所有平台。**

## 设计思路

平台之间的差别只有一处：**它有没有「技能（Skill）」这个机制。**

| 平台 | 有 Skill 机制？ | 怎么用 |
| --- | --- | --- |
| 任意支持「导入技能包」的 Agent 平台 | ✅ | 上传 `dist/reading-coach.zip` |
| 豆包【工作任务】模式 | ✅ 技能 · 连接器 · 伙伴 | **同一份 zip**，或一句话装本 GitHub 仓库 |
| Claude Code / Cursor / VS Code Copilot / Codex CLI / Gemini CLI | ✅ Agent Skills 标准 | 拷 `skills/reading-coach/` |
| 豆包【智能体】模式 / 任意对话框 | ❌ | 直接粘 `prompt.md` 全文 |

所以只需要**一份内核 + 两种壳**：

```
prompt.md（内核：平台无关的提示词，自带「环境自适应」）
      │
      ├─ + YAML frontmatter ──▶ skills/reading-coach/SKILL.md ──▶ 所有有 Skill 机制的平台
      └─ 打成一个 zip ────────▶ dist/reading-coach.zip ─────────▶ 上传技能
```

> **为什么没有按平台分叉的适配文件？**
> 因为不需要。真正的平台差异只有一条：能不能输出文件、能不能联网。
> 这条已经写在 `prompt.md` 的「环境自适应」一节里，内核在任何环境都自洽——粘到对话框里它自己会降级。
> 每多一个「某平台专用文件」，就多一份会跟内核脱节的副本。

> **为什么不直接只发 SKILL.md？**
> SKILL.md 是 Anthropic 的开放标准（agentskills.io），覆盖 Claude Code、Cursor、Codex、Gemini CLI 等 20+ 产品，豆包【工作任务】也吃同一套。
> 但**只有人设输入框的场景永远存在**（豆包智能体、老版本、别的产品），那里只吃纯文本。所以内核必须独立于 SKILL.md 存在。

## 仓库结构

```
reading-coach-skills-v0.1/
├── skill.json                  # 元数据：名称/描述/版本/许可/兼容平台
├── prompt.md                   # ★ 唯一真源
├── build.py                    # 生成产物
├── skills/reading-coach/SKILL.md   # 产物，提交（各平台取货点）
├── dist/reading-coach.zip          # 产物，提交（上传技能用）
├── README.md
└── LICENSE
```

只有两处需要维护：`prompt.md` 和 `skill.json`。

## 怎么给别人用

先跑一次生成：

```bash
python build.py
```

### 1. 支持「导入技能包」的平台
把 `dist/reading-coach.zip` 发给对方 → 在该平台的技能管理中心选「上传技能 / 导入技能包」→ 选中 zip。

### 2. 豆包用户（工作任务模式）
豆包工作（豆包专业版）有完整的 Skill 体系，装法和其他支持技能包的平台是同一套：

**方式 A · 一句话装 GitHub 仓库**
在豆包工作任务的对话框里发：

```
请打开下面的 GitHub 仓库，找到其中的 reading-coach 技能，阅读相关文件并完成安装：
https://github.com/Sevenhty/reading-coach-skills-v0.1
安装完成后，请告诉我安装结果。
```

**方式 B · 手动上传**
左侧「技能 · 连接器 · 伙伴」→ 右上角「新建」→「上传技能」→ 选 `dist/reading-coach.zip`。
装好后在「我的技能」里管理，对话中打 `/` 调用。

> 豆包里的【**智能体**】是另一回事——那里只有一段"角色描述"输入框，没有技能体系。
> 这种场景不用 zip，直接把 `prompt.md` 全文粘进去就行。

### 3. Claude Code / Cursor / Codex / Gemini CLI 用户
把 `skills/reading-coach/` 整个文件夹放到对应目录：

```bash
~/.claude/skills/reading-coach/     # Claude Code，全局
~/.cursor/skills/reading-coach/     # Cursor，全局
<项目>/.claude/skills/reading-coach/   # 项目级
```

### 4. 什么都装不了的人
把 `prompt.md` 正文直接粘进任意 AI 对话框开头。这是最终兜底。

**如果输入框太短，塞不下全文**，用这段极简版：

> 你是读书精读教练，不替人读书。先问用户"哪句话让你停了一下"，再指出他抓住的核心、漏掉的论证、可能理解偏的地方。禁止凭记忆引用原文，不确定就说不确定。最后输出一张卡片：书名+章节+日期、本章一句话、用户自己说过的一句话、一个应用问题。

## 为什么值得放 GitHub

一个仓库同时喂饱所有平台：支持技能包的平台下载 zip、豆包一句话装仓库、Claude/Cursor 直接拷 skills 目录、不会装的人看 README 抄提示词。**GitHub 是单一真源，各平台从它取货。**

## 怎么改

改 `prompt.md` → 跑 `python build.py` → `skills/` 和 `dist/` 重新生成。版本号在 `skill.json` 里，发新版时递增。

## 许可

MIT，见 [LICENSE](LICENSE)。
