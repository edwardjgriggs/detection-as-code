"""Enforce the rule requirements listed in CONTRIBUTING.md."""

import uuid
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parent.parent
RULE_FILES = sorted((REPO / "rules").glob("**/*.yml"))
REQUIRED_KEYS = ("title", "id", "description", "references", "falsepositives", "level", "tags")


def load(path):
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def mapped_logsources():
    """Return the (product, service) pairs pipelines/sentinel.yml assigns a table to."""
    pipeline = load(REPO / "pipelines" / "sentinel.yml")
    return {
        (condition.get("product"), condition.get("service"))
        for transformation in pipeline["transformations"]
        for condition in transformation.get("rule_conditions", [])
        if condition.get("type") == "logsource"
    }


@pytest.fixture(params=RULE_FILES, ids=lambda path: path.relative_to(REPO).as_posix())
def rule(request):
    return load(request.param)


def test_rules_are_present():
    assert RULE_FILES


def test_required_keys_are_filled(rule):
    for key in REQUIRED_KEYS:
        assert rule.get(key), f"missing {key}"


def test_id_is_a_uuid(rule):
    uuid.UUID(str(rule["id"]))


def test_references_link_an_attack_technique(rule):
    assert any("attack.mitre.org/techniques/" in ref for ref in rule["references"])


def test_tags_name_an_attack_technique(rule):
    assert any(tag.startswith("attack.t") for tag in rule["tags"])


def test_logsource_has_a_table_in_the_pipeline(rule):
    logsource = rule["logsource"]
    assert (logsource.get("product"), logsource.get("service")) in mapped_logsources()


def test_ids_are_unique():
    ids = [load(path)["id"] for path in RULE_FILES]
    assert len(ids) == len(set(ids))
