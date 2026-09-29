"""验证版本化布局契约与正式 Few-shot 保持一致。"""

import re
from pathlib import Path

import pytest

from services.card_validation import CompactDslValidationError, validate_compact_dsl
from services.compact_dsl_a2ui_converter import ComponentRow, parse_compact_dsl_rows
from services.compact_layout_runtime import (
    LAYOUT_CONTRACT_VERSION,
    CompactLayoutRuntimeError,
    layout_ids_for_size,
    load_layout_contract,
    match_compact_layout,
)
from services.compact_prompt_loader import assemble_prompts

PROMPT_SOURCE = (
    Path(__file__).resolve().parents[1]
    / "cloud/data/protocol_profiles/design-compact-dsl-fusion/prompt_source"
)
PROMPTS = assemble_prompts(PROMPT_SOURCE)
FEW_SHOT_LAYOUTS = {
    "2x2-V00": "S-center",
    "2x2-V01": "S-title-dual-content",
    "2x2-V02": "S-title-content-action",
    "2x2-V03": "S-title-anchor",
    "2x2-V04": "S-dual-info",
    "2x2-V05": "S-title-dual-column-action",
    "2x2-V06": "S-content-dual-action",
    "2x4-V00": "W-top-bottom",
    "2x4-V01": "W-top-bottom",
    "2x4-V02": "W-split-panels",
    "2x4-V03": "W-content-side-slots",
    "2x4-V04": "W-four-slots",
    "2x4-V05": "W-content-side-slots",
    "2x4-V06": "W-split-panels",
}


def _few_shots() -> list[tuple[str, str, str]]:
    examples: list[tuple[str, str, str]] = []
    for size in ("2x2", "2x4"):
        document = PROMPTS[f"fewshot_{size}"]
        for section in re.split(r"(?m)^## ", document)[1:]:
            identifier = re.search(rf"({size}-V\d\d)", section)
            source = re.search(r"```genui\s*\n(.*?)\n```", section, re.S)
            assert identifier is not None
            assert source is not None
            examples.append((identifier.group(1), size, source.group(1)))
    return examples


def _components(source: str) -> list[ComponentRow]:
    return [
        row
        for row in parse_compact_dsl_rows(source)
        if isinstance(row, ComponentRow)
    ]


def _layout_examples() -> list[tuple[str, str, str]]:
    examples: list[tuple[str, str, str]] = []
    for size in ("2x2", "2x4"):
        document = (PROMPT_SOURCE / f"layouts/{size}.md").read_text(encoding="utf-8")
        for section in re.split(r"(?m)^### `", document)[1:]:
            layout_id = section.split("`", 1)[0]
            source = re.search(r"```genui\s*\n(.*?)\n```", section, re.S)
            if layout_id.startswith(("S-", "W-")):
                assert source is not None, layout_id
                examples.append((layout_id, size, source.group(1)))
    return examples


def test_layout_contract_registers_the_documented_layouts() -> None:
    contract = load_layout_contract()
    assert contract.get("version") == LAYOUT_CONTRACT_VERSION
    assert layout_ids_for_size("2x2") == (
        "S-center",
        "S-title-content",
        "S-title-dual-content",
        "S-quad-content",
        "S-title-content-action",
        "S-title-primary-secondary-action",
        "S-title-dual-column-action",
        "S-title-anchor",
        "S-content-dual-action",
        "S-dual-info",
    )
    assert layout_ids_for_size("2x4") == (
        "W-top-bottom",
        "W-split-panels",
        "W-content-side-slots",
        "W-four-slots",
    )


@pytest.mark.parametrize(
    "identifier,size,source",
    _few_shots(),
    ids=[item[0] for item in _few_shots()],
)
def test_formal_few_shot_matches_its_layout(
    identifier: str,
    size: str,
    source: str,
) -> None:
    expected = FEW_SHOT_LAYOUTS.get(identifier)
    assert expected is not None
    result = match_compact_layout(
        _components(source),
        size=size,
        layout_scope=expected,
    )
    assert result.layout_id == expected


@pytest.mark.parametrize(
    "layout_id,size,source",
    _layout_examples(),
    ids=[item[0] for item in _layout_examples()],
)
def test_documented_example_matches_its_executable_layout(
    layout_id: str,
    size: str,
    source: str,
) -> None:
    result = match_compact_layout(
        _components(source),
        size=size,
        layout_scope=layout_id,
    )
    assert result.layout_id == layout_id


def test_layout_scope_rejects_wrong_geometry_before_expansion() -> None:
    source = '\n'.join(
        (
            '["root","Column",{"padding":8,"alignItems":"center",'
            '"justifyContent":"center"},["value"]]',
            '["value","Text",{"content":"42","fontSize":30}]',
        )
    )
    with pytest.raises(CompactDslValidationError, match="S-center"):
        validate_compact_dsl(
            source,
            task_spec={"size": "2x2"},
            card_spec={"suggestSize": "2x2"},
            layout_scope="S-center",
        )


def test_unknown_layout_scope_is_rejected() -> None:
    _, _, source = _few_shots()[0]
    with pytest.raises(CompactLayoutRuntimeError, match="Unknown Compact layout scope"):
        match_compact_layout(
            _components(source),
            size="2x2",
            layout_scope="S-unknown",
        )
