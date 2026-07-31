from __future__ import annotations

import re
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "tech-concept-multisource-learning"


class SubmissionValidationTest(unittest.TestCase):
    def test_frontmatter_and_description_follow_competition_rules(self) -> None:
        content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        _, frontmatter, body = content.split("---", 2)
        metadata_lines = [line for line in frontmatter.strip().splitlines() if line]
        self.assertEqual(len(metadata_lines), 2)
        self.assertTrue(metadata_lines[0].startswith("name: "))
        self.assertTrue(metadata_lines[1].startswith("description: "))

        name = metadata_lines[0].removeprefix("name: ").strip()
        description = metadata_lines[1].removeprefix("description: ").strip()
        self.assertEqual(name, SKILL_ROOT.name)
        self.assertLessEqual(len(name), 64)
        self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertTrue(body.strip())

        segments = description.split("；")
        self.assertEqual(len(segments), 3)
        self.assertIn("输入", segments[0])
        self.assertIn("输出", segments[0])
        self.assertIn("适用于", segments[1])
        self.assertIn("场景", segments[1])
        self.assertTrue(segments[2].startswith("触发词："))
        triggers = segments[2].removeprefix("触发词：").split("、")
        self.assertGreaterEqual(len(triggers), 6)
        self.assertTrue(all(trigger.strip() for trigger in triggers))

    def test_package_has_only_required_runtime_files(self) -> None:
        files = {
            path.relative_to(SKILL_ROOT).as_posix()
            for path in SKILL_ROOT.rglob("*")
            if path.is_file()
        }
        self.assertEqual(
            files,
            {
                "SKILL.md",
                "references/quality-safety-and-visuals.md",
            },
        )
        self.assertFalse(any("__pycache__" in path.parts for path in SKILL_ROOT.rglob("*")))

    def test_zip_has_standard_top_level_directory_and_exact_files(self) -> None:
        zip_path = REPO_ROOT / "dist" / "tech-concept-multisource-learning.zip"
        self.assertTrue(zip_path.is_file())
        with zipfile.ZipFile(zip_path) as archive:
            files = {name for name in archive.namelist() if not name.endswith("/")}
            self.assertEqual(
                files,
                {
                    "tech-concept-multisource-learning/SKILL.md",
                    "tech-concept-multisource-learning/references/quality-safety-and-visuals.md",
                },
            )
            for name in files:
                archive.read(name).decode("utf-8")

    def test_required_workflow_and_visual_guards_are_present(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        reference = (
            SKILL_ROOT / "references" / "quality-safety-and-visuals.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "至少选择三个相互独立的可信来源",
            "建立证据台账",
            "无法消解的分歧并列呈现",
            "一至两张本地矢量图",
            "不覆盖原文件",
        ):
            self.assertIn(phrase, skill)
        for phrase in (
            "十六比九比例",
            "三至七个核心节点",
            "不加载外部字体",
            "可扩展标记语言字符转义",
            "本机名、内网域名",
            "环回、私有、链路本地、保留",
        ):
            self.assertIn(phrase, reference)

    def test_skill_contains_no_static_network_endpoint(self) -> None:
        findings: list[str] = []
        for path in SKILL_ROOT.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            if re.search(r"(?i)https?://", text):
                findings.append(str(path.relative_to(SKILL_ROOT)))
        self.assertEqual(findings, [])

    def test_security_guards_cover_submission_risks(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        reference = (
            SKILL_ROOT / "references" / "quality-safety-and-visuals.md"
        ).read_text(encoding="utf-8")
        self.assertIn("不编写自定义网络请求", skill)
        for phrase in (
            "域名重绑定",
            "全部网络地址",
            "不索取、读取、记录或写入访问密钥",
            "不打开或解压归档文件",
            "不把用户文本解析为图片、链接或自动跳转地址",
            "规范化后的目标必须仍位于当前任务目录内",
            "拒绝符号链接、重解析点",
        ):
            self.assertIn(phrase, reference)


if __name__ == "__main__":
    unittest.main()
