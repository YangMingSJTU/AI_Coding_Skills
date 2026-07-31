from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    REPO_ROOT
    / "skills"
    / "daily-body-composition-planner"
    / "scripts"
    / "profile_store.py"
)
SKILL_ROOT = SCRIPT.parents[1]


PROFILE = {
    "age": 35,
    "sex": "女",
    "height_cm": 165,
    "weight_kg": 68,
    "goals": {
        "primary_goal": "改善体成分",
        "target_description": "先稳步减脂并保持肌肉量",
        "target_weight_kg": 62,
        "target_body_fat_pct": 27,
        "target_muscle_pct": None,
    },
    "safety": {
        "has_diagnosed_condition": False,
        "uses_medication": False,
        "pregnant_or_breastfeeding": False,
        "eating_disorder_history": False,
        "acute_pain_or_injury": False,
        "food_allergies": [],
    },
    "preferences": {
        "diet_detail_level": "详细",
        "exercise_detail_level": "简约",
        "dietary_pattern": "均衡饮食",
        "disliked_foods": ["香菜"],
        "available_equipment": [],
        "activity_level": "久坐",
        "daily_exercise_minutes": 30,
    },
    "optional_metrics": {"body_fat_pct": 32, "muscle_pct": 28},
}

CHECKIN = {
    "date": "2026-07-31",
    "acute_illness_or_fever": False,
    "new_pain_or_injury": False,
    "available_exercise_minutes": 30,
    "sleep_hours": 7,
    "energy_1_to_5": 4,
    "current_weight_kg": 68,
    "special_notes": "今天在家办公",
}

PLAN = {
    "date": "2026-07-31",
    "diet_mode": "详细",
    "exercise_mode": "简约",
    "safety_level": "正常规划",
    "diet_summary": (
        "估算每日能量约1550至1650千卡，蛋白质约100至115克；"
        "三餐加可选加餐，避开香菜并提供等价替换。"
    ),
    "exercise_summary": (
        "30分钟居家低冲击训练：热身5分钟、自重力量与快走20分钟、"
        "放松5分钟，主观用力程度5至6级。"
    ),
}


class ProfileStoreTest(unittest.TestCase):
    def run_cli(
        self,
        cwd: Path,
        command: str,
        user_id: str,
        payload: dict[str, object] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        input_text = None if payload is None else json.dumps(payload, ensure_ascii=False)
        return subprocess.run(
            [
                sys.executable,
                "-B",
                str(SCRIPT),
                command,
                "--user-id",
                user_id,
            ],
            cwd=cwd,
            input=input_text,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )

    def test_full_local_profile_flow(self) -> None:
        with tempfile.TemporaryDirectory(prefix="health-skill-test-") as temp_name:
            workdir = Path(temp_name)

            profile_result = self.run_cli(
                workdir, "upsert-profile", "demo-user-001", PROFILE
            )
            self.assertEqual(profile_result.returncode, 0, profile_result.stderr)

            checkin_result = self.run_cli(
                workdir, "record-checkin", "demo-user-001", CHECKIN
            )
            self.assertEqual(checkin_result.returncode, 0, checkin_result.stderr)

            plan_result = self.run_cli(
                workdir, "record-plan", "demo-user-001", PLAN
            )
            self.assertEqual(plan_result.returncode, 0, plan_result.stderr)
            revised_plan = dict(PLAN)
            revised_plan["exercise_summary"] = PLAN["exercise_summary"] + " 用户确认后更新。"
            revised_plan_result = self.run_cli(
                workdir, "record-plan", "demo-user-001", revised_plan
            )
            self.assertEqual(
                revised_plan_result.returncode, 0, revised_plan_result.stderr
            )

            get_result = self.run_cli(workdir, "get", "demo-user-001")
            self.assertEqual(get_result.returncode, 0, get_result.stderr)
            response = json.loads(get_result.stdout)
            self.assertTrue(response["found"])
            user = response["user"]
            self.assertEqual(
                user["profile"]["preferences"]["diet_detail_level"], "详细"
            )
            self.assertEqual(
                user["profile"]["preferences"]["exercise_detail_level"], "简约"
            )
            self.assertEqual(
                user["daily_checkins"]["2026-07-31"][0]["energy_1_to_5"], 4
            )
            self.assertEqual(
                user["daily_plans"]["2026-07-31"][0]["safety_level"], "正常规划"
            )
            self.assertEqual(len(user["daily_plans"]["2026-07-31"]), 2)

            data_file = workdir / ".health_plan_data" / "health_profiles.json"
            self.assertTrue(data_file.is_file())
            stored = json.loads(data_file.read_text(encoding="utf-8"))
            self.assertEqual(stored["schema_version"], 1)
            self.assertEqual(list(stored["users"]), ["demo-user-001"])

    def test_rejects_unsafe_identifier(self) -> None:
        with tempfile.TemporaryDirectory(prefix="health-skill-test-") as temp_name:
            result = self.run_cli(Path(temp_name), "get", "../escape")
            self.assertEqual(result.returncode, 2)
            self.assertIn("user_id", result.stderr)

    def test_rejects_direct_identifier_as_user_id(self) -> None:
        with tempfile.TemporaryDirectory(prefix="health-skill-test-") as temp_name:
            result = self.run_cli(Path(temp_name), "get", "12345678901")
            self.assertEqual(result.returncode, 2)
            self.assertIn("直接身份信息", result.stderr)

    def test_rejects_direct_identifier_and_markup_in_free_text(self) -> None:
        with tempfile.TemporaryDirectory(prefix="health-skill-test-") as temp_name:
            workdir = Path(temp_name)
            profile_result = self.run_cli(
                workdir, "upsert-profile", "demo-user-002", PROFILE
            )
            self.assertEqual(profile_result.returncode, 0, profile_result.stderr)
            unsafe_checkin = dict(CHECKIN)
            unsafe_checkin["special_notes"] = "请联系 demo@example.invalid"
            checkin_result = self.run_cli(
                workdir, "record-checkin", "demo-user-002", unsafe_checkin
            )
            self.assertEqual(checkin_result.returncode, 2)
            self.assertIn("请先脱敏", checkin_result.stderr)
            markup_checkin = dict(CHECKIN)
            markup_checkin["special_notes"] = "<" + "b>重要内容</" + "b>"
            markup_result = self.run_cli(
                workdir, "record-checkin", "demo-user-002", markup_checkin
            )
            self.assertEqual(markup_result.returncode, 2)
            self.assertIn("不安全", markup_result.stderr)

    def test_rejects_underage_profile(self) -> None:
        with tempfile.TemporaryDirectory(prefix="health-skill-test-") as temp_name:
            underage = dict(PROFILE)
            underage["age"] = 16
            result = self.run_cli(
                Path(temp_name), "upsert-profile", "demo-underage", underage
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("age", result.stderr)


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
        self.assertGreaterEqual(sum("衡刻" in trigger for trigger in triggers), 4)
        self.assertIn("衡刻今日计划", body)

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
                "references/safety-and-output.md",
                "scripts/profile_store.py",
            },
        )
        self.assertFalse(any("__pycache__" in path.parts for path in SKILL_ROOT.rglob("*")))

if __name__ == "__main__":
    unittest.main()
