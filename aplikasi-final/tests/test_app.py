"""Uji route Flask khusus WargaBot."""
import copy
import json
from pathlib import Path

import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    return app.test_client()


def test_home_mengarahkan_ke_wargabot(client):
    res = client.get("/")
    assert res.status_code == 302
    assert res.headers["Location"].endswith("/chat/kampung")


def test_halaman_chat_wargabot(client):
    res = client.get("/chat/kampung")
    assert res.status_code == 200
    assert "WargaBot" in res.get_data(as_text=True)


def test_tema_tidak_ada_404(client):
    assert client.get("/chat/tidak-ada").status_code == 404
    assert client.get("/api/history/tidak-ada").status_code == 404


def test_api_themes_hanya_memuat_wargabot(client):
    data = client.get("/api/themes").get_json()
    assert [x["id"] for x in data] == ["kampung"]


def test_api_chat_wargabot(client):
    res = client.post("/api/chat", json={"message": "sampah diambil hari apa", "theme": "kampung"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["intent"] == "jadwal_sampah"
    assert data["reply"]


@pytest.mark.parametrize("payload", [
    {"message": "", "theme": "kampung"},
    {"message": "halo", "theme": "salah"},
    {"message": "a" * 501, "theme": "kampung"},
    {},
])
def test_api_chat_input_tidak_valid(client, payload):
    assert client.post("/api/chat", json=payload).status_code == 400


def test_riwayat_tersimpan_dan_bisa_dihapus(client):
    client.post("/api/chat", json={"message": "halo", "theme": "kampung"})
    riwayat = client.get("/api/history/kampung").get_json()
    assert [r["sender"] for r in riwayat] == ["user", "bot"]
    client.delete("/api/history/kampung")
    assert client.get("/api/history/kampung").get_json() == []


def test_statistik_intent(client):
    client.post("/api/chat", json={"message": "halo", "theme": "kampung"})
    stats = client.get("/api/stats/kampung").get_json()
    assert stats[0]["intent"] == "salam"


def test_api_explain(client):
    data = client.post("/api/explain", json={"message": "jadwal sampah", "theme": "kampung"}).get_json()
    assert data["threshold"] == 0.45
    assert data["candidates"][0]["intent"] == "jadwal_sampah"


def test_admin_memuat_pertanyaan_tak_dikenali(client):
    client.post("/api/chat", json={"message": "harga beras hari ini", "theme": "kampung"})
    html = client.get("/admin/kampung").get_data(as_text=True)
    assert "harga beras hari ini" in html
    assert "tidak dikenali" in html


def test_admin_key_melindungi_halaman_admin(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "t.db"), "ADMIN_KEY": "rahasia"})
    c = app.test_client()
    assert c.get("/admin/kampung").status_code == 403
    assert c.get("/api/stats/kampung").status_code == 403
    assert c.get("/admin/kampung?key=rahasia").status_code == 200


def test_data_kampung_belum_diisi_tidak_bocor(tmp_path):
    from chatbot.engine import load_themes
    asli = load_themes(Path(__file__).resolve().parent.parent / "themes")["kampung"]
    tema = copy.deepcopy(asli)
    tema["data"]["kontak_pengurus"] = "[ISI: kontak pengurus]"
    (tmp_path / "themes").mkdir()
    (tmp_path / "themes" / "kampung.json").write_text(json.dumps(tema), encoding="utf-8")
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "t.db"), "THEMES_DIR": str(tmp_path / "themes")})
    data = app.test_client().post("/api/chat", json={"message": "nomor pak rt berapa", "theme": "kampung"}).get_json()
    assert data["intent"] == "kontak_pengurus"
    assert data["belum_diisi"] is True
    assert "[ISI" not in data["reply"]


def test_data_kampung_terisi(tmp_path):
    from chatbot.engine import load_themes
    asli = load_themes(Path(__file__).resolve().parent.parent / "themes")["kampung"]
    tema = copy.deepcopy(asli)
    tema["terakhir_diperbarui"] = "01-11-2026"
    tema["data"] = {k: f"DATA_{k}" for k in tema["data"]}
    (tmp_path / "themes").mkdir()
    (tmp_path / "themes" / "kampung.json").write_text(json.dumps(tema), encoding="utf-8")
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "t.db"), "THEMES_DIR": str(tmp_path / "themes")})
    data = app.test_client().post("/api/chat", json={"message": "sampah diambil hari apa", "theme": "kampung"}).get_json()
    assert data["intent"] == "jadwal_sampah"
    assert data["belum_diisi"] is False
    assert "DATA_jadwal_sampah" in data["reply"]
