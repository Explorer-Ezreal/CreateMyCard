"""模板预选尊重显式主题要求，复用共享颜色偏好解析。"""

import re

from services.post_layout_theme_registry import load_theme_registry


def _has_explicit_color(query: str) -> bool:
    names = load_theme_registry().get("userColorOverrides", {}).get("namedColors", {})
    color_names = "|".join(re.escape(name) for name in names)
    token = r"#[0-9A-Fa-f]{8}|#[0-9A-Fa-f]{6}"
    if color_names:
        token += "|" + color_names
    for target in ("文字|字体|字色|字", "背景|底色"):
        direct = rf"(?:{target})\s*(?:用|是|为|改成|改为|使用|要|：|:)?\s*(?:{token})"
        reverse = rf"(?:{token})\s*(?:的)?(?:{target})"
        if re.search(direct, query) or re.search(reverse, query):
            return True
    return False


def photo_preference_reason(query: str) -> str | None:
    reason: str | None = None
    if re.search(r"纯色|渐变|[融绒]球|不要.*(?:图|背景)|不用.*(?:图|背景)|无(?:背景)?图", query):
        reason = "用户明确其它主题或不要图片"
    elif _has_explicit_color(query):
        reason = "用户明确颜色优先，本轮使用固定底色/渐变"
    return reason
