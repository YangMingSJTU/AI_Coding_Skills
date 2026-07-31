#!/usr/bin/env python3
"""Safely store local health profiles in one fixed JSON file."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import tempfile
from copy import deepcopy
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


DATA_DIR_NAME = ".health_plan_data"
DATA_FILE_NAME = "health_profiles.json"
MAX_INPUT_BYTES = 64 * 1024
MAX_STORE_BYTES = 5 * 1024 * 1024
USER_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
DIRECT_IDENTIFIER_PATTERNS = (
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    re.compile(r"(?<![0-9A-Za-z])\d{17}[0-9Xx](?![0-9A-Za-z])"),
    re.compile(r"(?<!\d)0\d{2,3}-?\d{7,8}(?!\d)"),
)
UNSAFE_MARKUP_RE = re.compile(
    r"(?is)<\s*/?\s*[A-Za-z][^>]{0,200}>|```|"
    r"!?\[[^\]\r\n]{0,200}\]\([^\)\r\n]{1,500}\)"
)
DETAIL_LEVELS = {"简约", "详细"}
SAFETY_LEVELS = {"正常规划", "仅一般建议", "停止并转介"}
SEX_VALUES = {"女", "男", "其他", "不愿透露"}
GOAL_VALUES = {"减脂", "减重", "增肌", "维持", "改善体成分", "其他"}


class StoreError(ValueError):
    """Represent a safe, user-facing validation or storage error."""


def configure_standard_streams() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="strict")


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_json_text(raw: str, field_name: str) -> Any:
    def reject_constant(value: str) -> None:
        raise StoreError(f"{field_name} 不能包含非有限数值：{value}")

    try:
        return json.loads(raw, parse_constant=reject_constant)
    except json.JSONDecodeError as exc:
        raise StoreError(f"{field_name} 不是有效的 JSON：{exc.msg}") from exc


def read_payload() -> dict[str, Any]:
    raw_bytes = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    if len(raw_bytes) > MAX_INPUT_BYTES:
        raise StoreError("输入数据超过 64 KiB 限制")
    if not raw_bytes.strip():
        raise StoreError("标准输入中缺少 JSON 对象")
    try:
        raw = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise StoreError("输入必须使用 UTF-8 编码") from exc
    payload = parse_json_text(raw, "输入")
    if not isinstance(payload, dict):
        raise StoreError("输入必须是 JSON 对象")
    return payload


def ensure_object(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise StoreError(f"{field_name} 必须是对象")
    return value


def reject_unknown_fields(
    value: dict[str, Any], allowed: set[str], field_name: str
) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise StoreError(f"{field_name} 包含未支持字段：{', '.join(unknown)}")


def require_fields(value: dict[str, Any], required: set[str], field_name: str) -> None:
    missing = sorted(required - set(value))
    if missing:
        raise StoreError(f"{field_name} 缺少必填字段：{', '.join(missing)}")


def clean_text(value: Any, field_name: str, max_length: int = 500) -> str:
    if not isinstance(value, str):
        raise StoreError(f"{field_name} 必须是文本")
    cleaned = value.strip()
    if not cleaned:
        raise StoreError(f"{field_name} 不能为空")
    if len(cleaned) > max_length:
        raise StoreError(f"{field_name} 超过 {max_length} 字符限制")
    if CONTROL_CHAR_RE.search(cleaned):
        raise StoreError(f"{field_name} 包含不允许的控制字符")
    if any(pattern.search(cleaned) for pattern in DIRECT_IDENTIFIER_PATTERNS):
        raise StoreError(f"{field_name} 可能包含手机号、邮箱或证件号，请先脱敏")
    if UNSAFE_MARKUP_RE.search(cleaned):
        raise StoreError(f"{field_name} 包含不安全的网页或 Markdown 标记，请改用纯文本")
    return cleaned


def optional_text(value: Any, field_name: str, max_length: int = 500) -> str | None:
    if value is None:
        return None
    return clean_text(value, field_name, max_length)


def clean_text_list(
    value: Any, field_name: str, max_items: int = 30, item_length: int = 100
) -> list[str]:
    if not isinstance(value, list):
        raise StoreError(f"{field_name} 必须是数组")
    if len(value) > max_items:
        raise StoreError(f"{field_name} 最多包含 {max_items} 项")
    return [clean_text(item, f"{field_name}[{index}]", item_length) for index, item in enumerate(value)]


def clean_number(
    value: Any,
    field_name: str,
    minimum: float,
    maximum: float,
    *,
    integer: bool = False,
) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise StoreError(f"{field_name} 必须是数值")
    if not math.isfinite(float(value)):
        raise StoreError(f"{field_name} 必须是有限数值")
    if integer and not isinstance(value, int):
        raise StoreError(f"{field_name} 必须是整数")
    if value < minimum or value > maximum:
        raise StoreError(f"{field_name} 必须在 {minimum} 至 {maximum} 之间")
    return value


def optional_number(
    value: Any, field_name: str, minimum: float, maximum: float
) -> int | float | None:
    if value is None:
        return None
    return clean_number(value, field_name, minimum, maximum)


def clean_boolean(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise StoreError(f"{field_name} 必须是布尔值")
    return value


def clean_date(value: Any, field_name: str = "date") -> str:
    text = clean_text(value, field_name, 10)
    try:
        date.fromisoformat(text)
    except ValueError as exc:
        raise StoreError(f"{field_name} 必须使用 YYYY-MM-DD 格式") from exc
    return text


def clean_profile(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "age",
        "sex",
        "height_cm",
        "weight_kg",
        "goals",
        "safety",
        "preferences",
        "optional_metrics",
    }
    required = {"age", "sex", "height_cm", "weight_kg", "goals", "safety", "preferences"}
    reject_unknown_fields(payload, allowed, "profile")
    require_fields(payload, required, "profile")

    sex = clean_text(payload["sex"], "sex", 10)
    if sex not in SEX_VALUES:
        raise StoreError(f"sex 必须是以下值之一：{', '.join(sorted(SEX_VALUES))}")

    goals = ensure_object(payload["goals"], "goals")
    goal_allowed = {
        "primary_goal",
        "target_description",
        "target_weight_kg",
        "target_body_fat_pct",
        "target_muscle_pct",
    }
    reject_unknown_fields(goals, goal_allowed, "goals")
    require_fields(goals, {"primary_goal"}, "goals")
    primary_goal = clean_text(goals["primary_goal"], "goals.primary_goal", 20)
    if primary_goal not in GOAL_VALUES:
        raise StoreError(
            f"goals.primary_goal 必须是以下值之一：{', '.join(sorted(GOAL_VALUES))}"
        )
    normalized_goals = {
        "primary_goal": primary_goal,
        "target_description": optional_text(
            goals.get("target_description"), "goals.target_description", 200
        ),
        "target_weight_kg": optional_number(
            goals.get("target_weight_kg"), "goals.target_weight_kg", 25, 350
        ),
        "target_body_fat_pct": optional_number(
            goals.get("target_body_fat_pct"), "goals.target_body_fat_pct", 1, 75
        ),
        "target_muscle_pct": optional_number(
            goals.get("target_muscle_pct"), "goals.target_muscle_pct", 1, 80
        ),
    }
    if not any(
        normalized_goals[key] is not None
        for key in (
            "target_description",
            "target_weight_kg",
            "target_body_fat_pct",
            "target_muscle_pct",
        )
    ):
        raise StoreError("goals 至少需要目标描述或一个目标指标")

    safety = ensure_object(payload["safety"], "safety")
    safety_required = {
        "has_diagnosed_condition",
        "uses_medication",
        "pregnant_or_breastfeeding",
        "eating_disorder_history",
        "acute_pain_or_injury",
        "food_allergies",
    }
    reject_unknown_fields(safety, safety_required, "safety")
    require_fields(safety, safety_required, "safety")
    normalized_safety = {
        field: clean_boolean(safety[field], f"safety.{field}")
        for field in safety_required - {"food_allergies"}
    }
    normalized_safety["food_allergies"] = clean_text_list(
        safety["food_allergies"], "safety.food_allergies"
    )

    preferences = ensure_object(payload["preferences"], "preferences")
    preference_allowed = {
        "diet_detail_level",
        "exercise_detail_level",
        "dietary_pattern",
        "disliked_foods",
        "available_equipment",
        "activity_level",
        "daily_exercise_minutes",
    }
    reject_unknown_fields(preferences, preference_allowed, "preferences")
    require_fields(
        preferences, {"diet_detail_level", "exercise_detail_level"}, "preferences"
    )
    diet_level = clean_text(
        preferences["diet_detail_level"], "preferences.diet_detail_level", 10
    )
    exercise_level = clean_text(
        preferences["exercise_detail_level"], "preferences.exercise_detail_level", 10
    )
    if diet_level not in DETAIL_LEVELS or exercise_level not in DETAIL_LEVELS:
        raise StoreError("饮食和运动建议级别必须是“简约”或“详细”")
    normalized_preferences = {
        "diet_detail_level": diet_level,
        "exercise_detail_level": exercise_level,
        "dietary_pattern": optional_text(
            preferences.get("dietary_pattern"), "preferences.dietary_pattern", 100
        ),
        "disliked_foods": clean_text_list(
            preferences.get("disliked_foods", []), "preferences.disliked_foods"
        ),
        "available_equipment": clean_text_list(
            preferences.get("available_equipment", []),
            "preferences.available_equipment",
        ),
        "activity_level": optional_text(
            preferences.get("activity_level"), "preferences.activity_level", 100
        ),
        "daily_exercise_minutes": optional_number(
            preferences.get("daily_exercise_minutes"),
            "preferences.daily_exercise_minutes",
            0,
            300,
        ),
    }

    metrics = ensure_object(payload.get("optional_metrics", {}), "optional_metrics")
    metric_allowed = {"body_fat_pct", "muscle_pct"}
    reject_unknown_fields(metrics, metric_allowed, "optional_metrics")
    normalized_metrics = {
        "body_fat_pct": optional_number(
            metrics.get("body_fat_pct"), "optional_metrics.body_fat_pct", 1, 75
        ),
        "muscle_pct": optional_number(
            metrics.get("muscle_pct"), "optional_metrics.muscle_pct", 1, 80
        ),
    }

    return {
        "age": clean_number(payload["age"], "age", 18, 100, integer=True),
        "sex": sex,
        "height_cm": clean_number(payload["height_cm"], "height_cm", 100, 250),
        "weight_kg": clean_number(payload["weight_kg"], "weight_kg", 25, 350),
        "goals": normalized_goals,
        "safety": normalized_safety,
        "preferences": normalized_preferences,
        "optional_metrics": normalized_metrics,
    }


def clean_checkin(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "date",
        "acute_illness_or_fever",
        "new_pain_or_injury",
        "available_exercise_minutes",
        "sleep_hours",
        "energy_1_to_5",
        "current_weight_kg",
        "special_notes",
    }
    required = {
        "date",
        "acute_illness_or_fever",
        "new_pain_or_injury",
        "available_exercise_minutes",
    }
    reject_unknown_fields(payload, allowed, "checkin")
    require_fields(payload, required, "checkin")
    energy = payload.get("energy_1_to_5")
    return {
        "date": clean_date(payload["date"]),
        "acute_illness_or_fever": clean_boolean(
            payload["acute_illness_or_fever"], "acute_illness_or_fever"
        ),
        "new_pain_or_injury": clean_boolean(
            payload["new_pain_or_injury"], "new_pain_or_injury"
        ),
        "available_exercise_minutes": clean_number(
            payload["available_exercise_minutes"],
            "available_exercise_minutes",
            0,
            300,
            integer=True,
        ),
        "sleep_hours": optional_number(payload.get("sleep_hours"), "sleep_hours", 0, 24),
        "energy_1_to_5": (
            None
            if energy is None
            else clean_number(energy, "energy_1_to_5", 1, 5, integer=True)
        ),
        "current_weight_kg": optional_number(
            payload.get("current_weight_kg"), "current_weight_kg", 25, 350
        ),
        "special_notes": optional_text(
            payload.get("special_notes"), "special_notes", 500
        ),
    }


def clean_plan(payload: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "date",
        "diet_mode",
        "exercise_mode",
        "safety_level",
        "diet_summary",
        "exercise_summary",
    }
    reject_unknown_fields(payload, allowed, "plan")
    require_fields(payload, allowed, "plan")
    diet_mode = clean_text(payload["diet_mode"], "diet_mode", 10)
    exercise_mode = clean_text(payload["exercise_mode"], "exercise_mode", 10)
    safety_level = clean_text(payload["safety_level"], "safety_level", 20)
    if diet_mode not in DETAIL_LEVELS or exercise_mode not in DETAIL_LEVELS:
        raise StoreError("diet_mode 和 exercise_mode 必须是“简约”或“详细”")
    if safety_level not in SAFETY_LEVELS:
        raise StoreError("safety_level 必须是正常规划、仅一般建议或停止并转介")
    return {
        "date": clean_date(payload["date"]),
        "diet_mode": diet_mode,
        "exercise_mode": exercise_mode,
        "safety_level": safety_level,
        "diet_summary": clean_text(payload["diet_summary"], "diet_summary", 2000),
        "exercise_summary": clean_text(
            payload["exercise_summary"], "exercise_summary", 2000
        ),
    }


def validate_user_id(user_id: str) -> str:
    if not USER_ID_RE.fullmatch(user_id):
        raise StoreError("user_id 必须由 1 至 64 个英文字母、数字、下划线或连字符组成")
    if (user_id.isdigit() and len(user_id) >= 8) or any(
        pattern.search(user_id) for pattern in DIRECT_IDENTIFIER_PATTERNS
    ):
        raise StoreError("user_id 不能使用手机号、证件号或其他直接身份信息")
    return user_id


def is_redirected_path(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    return bool(callable(is_junction) and is_junction())


def get_store_path() -> Path:
    workspace = Path.cwd().resolve()
    data_dir = workspace / DATA_DIR_NAME
    if data_dir.exists() and is_redirected_path(data_dir):
        raise StoreError("数据目录不能是符号链接或目录联接")
    data_dir.mkdir(mode=0o700, exist_ok=True)
    if data_dir.resolve().parent != workspace:
        raise StoreError("数据目录必须位于当前工作目录内")
    data_file = data_dir / DATA_FILE_NAME
    if data_file.exists() and is_redirected_path(data_file):
        raise StoreError("数据文件不能是符号链接或目录联接")
    return data_file


def load_store(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_version": 1, "users": {}}
    if path.stat().st_size > MAX_STORE_BYTES:
        raise StoreError("数据文件超过 5 MiB 限制")
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise StoreError(f"无法读取数据文件：{exc}") from exc
    store = parse_json_text(raw, "数据文件")
    if not isinstance(store, dict) or store.get("schema_version") != 1:
        raise StoreError("数据文件结构或版本不受支持")
    if not isinstance(store.get("users"), dict):
        raise StoreError("数据文件缺少有效的 users 对象")
    return store


def save_store(path: Path, store: dict[str, Any]) -> None:
    serialized = json.dumps(store, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if len(serialized.encode("utf-8")) > MAX_STORE_BYTES:
        raise StoreError("写入后数据文件将超过 5 MiB 限制")
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=".health_profiles_",
            suffix=".tmp",
            delete=False,
        ) as temp_file:
            temp_name = temp_file.name
            temp_file.write(serialized)
            temp_file.flush()
            os.fsync(temp_file.fileno())
        if os.name != "nt":
            os.chmod(temp_name, 0o600)
        os.replace(temp_name, path)
    except OSError as exc:
        raise StoreError(f"无法安全写入数据文件：{exc}") from exc
    finally:
        if temp_name and os.path.exists(temp_name):
            try:
                os.unlink(temp_name)
            except OSError:
                pass


def ensure_user(store: dict[str, Any], user_id: str) -> dict[str, Any]:
    user = store["users"].get(user_id)
    if user is None:
        raise StoreError("未找到该本地别名的档案，请先建立档案")
    if not isinstance(user, dict):
        raise StoreError("用户档案结构无效")
    return user


def upsert_profile(store: dict[str, Any], user_id: str, profile: dict[str, Any]) -> None:
    timestamp = now_utc()
    existing = store["users"].get(user_id)
    created_at = existing.get("created_at", timestamp) if isinstance(existing, dict) else timestamp
    daily_checkins = existing.get("daily_checkins", {}) if isinstance(existing, dict) else {}
    daily_plans = existing.get("daily_plans", {}) if isinstance(existing, dict) else {}
    profile_history = existing.get("profile_history", []) if isinstance(existing, dict) else []
    if not isinstance(profile_history, list):
        raise StoreError("profile_history 结构无效")
    if isinstance(existing, dict) and isinstance(existing.get("profile"), dict):
        previous_profile = existing["profile"]
        if previous_profile != profile:
            profile_history.append(
                {"profile": deepcopy(previous_profile), "archived_at": timestamp}
            )
    store["users"][user_id] = {
        "profile": profile,
        "profile_history": profile_history,
        "daily_checkins": daily_checkins if isinstance(daily_checkins, dict) else {},
        "daily_plans": daily_plans if isinstance(daily_plans, dict) else {},
        "created_at": created_at,
        "updated_at": timestamp,
    }


def record_checkin(store: dict[str, Any], user_id: str, checkin: dict[str, Any]) -> None:
    user = ensure_user(store, user_id)
    checkins = user.setdefault("daily_checkins", {})
    if not isinstance(checkins, dict):
        raise StoreError("daily_checkins 结构无效")
    entry = deepcopy(checkin)
    entry["recorded_at"] = now_utc()
    entries = checkins.setdefault(checkin["date"], [])
    if isinstance(entries, dict):
        entries = [entries]
        checkins[checkin["date"]] = entries
    if not isinstance(entries, list):
        raise StoreError("当日 daily_checkins 结构无效")
    entries.append(entry)
    user["updated_at"] = now_utc()


def record_plan(store: dict[str, Any], user_id: str, plan: dict[str, Any]) -> None:
    user = ensure_user(store, user_id)
    plans = user.setdefault("daily_plans", {})
    if not isinstance(plans, dict):
        raise StoreError("daily_plans 结构无效")
    entry = deepcopy(plan)
    entry["recorded_at"] = now_utc()
    entries = plans.setdefault(plan["date"], [])
    if isinstance(entries, dict):
        entries = [entries]
        plans[plan["date"]] = entries
    if not isinstance(entries, list):
        raise StoreError("当日 daily_plans 结构无效")
    entries.append(entry)
    user["updated_at"] = now_utc()


def output_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="管理本地健康档案")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("get", "upsert-profile", "record-checkin", "record-plan"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--user-id", required=True)
    return parser


def main() -> int:
    configure_standard_streams()
    args = build_parser().parse_args()
    user_id = validate_user_id(args.user_id)
    path = get_store_path()
    store = load_store(path)

    if args.command == "get":
        user = store["users"].get(user_id)
        output_json(
            {
                "ok": True,
                "found": user is not None,
                "data_file": str(path),
                "user": user,
            }
        )
        return 0

    payload = read_payload()
    if args.command == "upsert-profile":
        upsert_profile(store, user_id, clean_profile(payload))
    elif args.command == "record-checkin":
        record_checkin(store, user_id, clean_checkin(payload))
    elif args.command == "record-plan":
        record_plan(store, user_id, clean_plan(payload))
    else:
        raise StoreError("不支持的操作")

    save_store(path, store)
    output_json({"ok": True, "operation": args.command, "data_file": str(path)})
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except StoreError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2) from exc
