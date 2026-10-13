#!/usr/bin/env python3
"""从 skill.json + prompt.md 生成各平台产物。

单一真源：
  skill.json   元数据（名称/描述/版本/许可）
  prompt.md    平台无关的提示词正文（自带环境自适应，无需按平台分叉）

产物：
  skills/reading-coach/SKILL.md   Agent Skills 格式。豆包工作任务 / Claude Code /
                                  Cursor / Codex / Gemini CLI 等平台共用这一份。
                                  提交到仓库后，豆包可用「一句话装 GitHub 仓库」直接安装。
  dist/reading-coach.zip          可在任意支持「导入技能包」的平台直接上传

用法：
  python build.py
"""
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8").strip()


def yaml_quote(value: str) -> str:
    """用单引号包裹 YAML 标量：内部双引号是字面量，中文冒号也不会破坏解析。

    YAML 单引号标量里只有单引号需要写成两个，这里统一处理。
    """
    return "'" + value.replace("'", "''") + "'"


def build_frontmatter(meta: dict) -> str:
    lines = [
        "---",
        f"name: {yaml_quote(meta['name'])}",
        f"description: {yaml_quote(meta['description'])}",
        f"version: {yaml_quote(str(meta['version']))}",
        f"license: {yaml_quote(str(meta['license']))}",
        "---",
    ]
    return "\n".join(lines)


def main() -> None:
    meta = json.loads(read_text("skill.json"))
    body = read_text("prompt.md")
    skill_name = meta["name"]

    SKILLS.mkdir(exist_ok=True)
    DIST.mkdir(exist_ok=True)
    skill_dir = SKILLS / skill_name

    # 清掉上一轮产物，避免改名后残留旧目录
    if skill_dir.exists():
        shutil.rmtree(skill_dir)
    skill_dir.mkdir(parents=True)

    # 1) SKILL.md —— 所有有 Skill 机制的平台共用这一份
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(build_frontmatter(meta) + "\n" + body + "\n", encoding="utf-8")
    print(f"[ok] {skill_md.relative_to(ROOT)}")

    # 2) 技能包 zip —— 「上传技能」直接导入（zip 内保留 <name>/ 一层）
    zip_path = DIST / f"{skill_name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(skill_dir.rglob("*")):
            if f.is_file():
                zf.write(f, f.relative_to(SKILLS))
    print(f"[ok] {zip_path.relative_to(ROOT)}")

    print("\n完成。改 prompt.md / skill.json 后重跑本脚本即可。")


if __name__ == "__main__":
    main()
