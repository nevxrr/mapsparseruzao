import runpy
from pathlib import Path

import mapsparseruzao.bootstrap as bootstrap
from mapsparseruzao.cli import run


def test_install_help_mentions_requirements_and_bat() -> None:
    text = bootstrap.install_help_text(["openpyxl"])
    assert "requirements.txt" in text
    assert "install.bat" in text
    assert "openpyxl" in text


def test_preflight_ok_when_deps_present() -> None:
    assert bootstrap.preflight() is None


def test_preflight_reports_missing(monkeypatch) -> None:
    monkeypatch.setattr(bootstrap, "missing_dependencies", lambda: ["openpyxl"])
    message = bootstrap.preflight()
    assert message is not None
    assert "openpyxl" in message


def test_cli_prints_install_help_when_deps_missing(monkeypatch, capsys) -> None:
    monkeypatch.setattr("mapsparseruzao.cli.preflight", lambda: bootstrap.install_help_text(["requests"]))
    assert run([]) == 2
    err = capsys.readouterr().err
    assert "requirements.txt" in err


def test_run_py_exists_and_is_standalone() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (root / "run.py").is_file()
    assert (root / "requirements.txt").is_file()
    assert (root / "install.bat").is_file()
    assert (root / "run.bat").is_file()
    source = (root / "run.py").read_text(encoding="utf-8")
    assert "mapsparseruzao.cli" in source
    assert "sys.path.insert" in source


def test_run_py_exits_on_missing_deps(monkeypatch) -> None:
    monkeypatch.setattr("mapsparseruzao.bootstrap.preflight", lambda: "нет библиотек")

    raised = False

    def fake_exit(code: int) -> None:
        nonlocal raised
        raised = True
        raise SystemExit(code)

    monkeypatch.setattr("sys.exit", fake_exit)
    try:
        runpy.run_path(str(Path(__file__).resolve().parents[1] / "run.py"), run_name="__main__")
    except SystemExit as exc:
        assert exc.code == 2
        assert raised
