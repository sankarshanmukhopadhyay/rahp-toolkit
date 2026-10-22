from tools import render_pressure_tests as renderer


def test_instance_local_reference_without_link_does_not_point_to_dtg_catalogue(tmp_path, monkeypatch):
    root = tmp_path
    (root / "data").mkdir()
    (root / "instances" / "example" / "data").mkdir(parents=True)
    (root / "data" / "risks.yaml").write_text(
        "version: 1\nrecords:\n  - id: RK-ROOT\n    title: Root risk\n",
        encoding="utf-8",
    )
    (root / "instances" / "example" / "data" / "risks.yaml").write_text(
        "version: 1\nrecords:\n  - id: XRK-01\n    title: Local risk\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(renderer, "ROOT", root)
    index = renderer.load_reference_index()
    monkeypatch.setattr(renderer, "REFERENCE_INDEX", index)
    monkeypatch.setattr(renderer, "CATALOGUE_RELATIVE", "../../build/site/catalogue.html")

    root_link = renderer.ref_link("RK-ROOT")
    local_ref = renderer.ref_link("XRK-01")

    assert "catalogue.html#RK-ROOT" in root_link
    assert local_ref == "`XRK-01 — Local risk`"
    assert "catalogue.html" not in local_ref


def test_instance_local_explicit_link_is_preserved(tmp_path, monkeypatch):
    root = tmp_path
    (root / "data").mkdir()
    (root / "instances" / "example" / "data").mkdir(parents=True)
    (root / "instances" / "example" / "data" / "risks.yaml").write_text(
        "version: 1\nrecords:\n"
        "  - id: XRK-02\n"
        "    title: Linked local risk\n"
        "    link: /deployment/risk-register.html#xrk-02\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(renderer, "ROOT", root)
    index = renderer.load_reference_index()
    monkeypatch.setattr(renderer, "REFERENCE_INDEX", index)

    rendered = renderer.ref_link("XRK-02")
    assert rendered == "[XRK-02 — Linked local risk](/deployment/risk-register.html#xrk-02)"
