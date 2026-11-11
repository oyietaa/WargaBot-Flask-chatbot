"""Uji unit mesin rule-based dan knowledge map WargaBot."""
from pathlib import Path
import copy
import pytest

from chatbot.engine import ChatbotEngine, load_themes, preprocess, similarity, validate_theme
from evaluate import baca_data, evaluasi

THEMES = load_themes(Path(__file__).resolve().parent.parent / "themes")
KAMPUNG = THEMES["kampung"]


def _terisi(theme):
    t = copy.deepcopy(theme)
    t["terakhir_diperbarui"] = "01-11-2026"
    t["data"] = {k: f"DATA_{k}" for k in t["data"]}
    return t


def test_hanya_tema_wargabot_dimuat():
    assert set(THEMES) == {"kampung"}


def test_preprocess_normalisasi_dan_stopword():
    assert preprocess("Gmn urus surat pengantar, kak?") == ["bagaimana", "urus", "surat", "pengantar"]


def test_similarity():
    assert similarity(["jadwal", "sampah"], ["jadwal", "sampah"]) == 1.0
    assert similarity(["gudeg"], ["jadwal", "sampah"]) < 0.3


def test_struktur_knowledge_map_wargabot():
    assert validate_theme(KAMPUNG) == []
    assert len(KAMPUNG["intents"]) == 17
    for intent in KAMPUNG["intents"]:
        assert len(intent["patterns"]) >= 5, intent["tag"]
        assert len(intent["responses"]) >= 2, intent["tag"]
    assert len(KAMPUNG["suggestions"]) == 4
    assert len(KAMPUNG["data"]) == 21


def test_normalisasi_kata_warga():
    token = preprocess("kerbak jam piro", KAMPUNG["normalisasi"], KAMPUNG["stopwords"])
    assert token == ["kerja", "bakti", "jam", "berapa"]


@pytest.mark.parametrize("pesan, intent", [
    ("assalamualaikum", "salam"),
    ("sampah diambil hari apa ya", "jadwal_sampah"),
    ("kerbak minggu ini jam berapa", "kerja_bakti"),
    ("giliran ronda saya kapan", "jadwal_ronda"),
    ("saudara nginep di rumah perlu lapor gak", "lapor_tamu"),
    ("jimpitan itu buat apa", "iuran"),
    ("syarat bikin surat pengantar rt", "surat_pengantar"),
    ("baru pindah ke sini lapor ke mana", "pindah_domisili"),
    ("posyandu hari apa", "posyandu_pkk"),
    ("ada berita lelayu hari ini", "info_duka"),
    ("got depan rumah mampet", "lapor_masalah"),
    ("butuh ambulans cepat", "darurat"),
])
def test_klasifikasi_intent_wargabot(pesan, intent):
    tag, _ = ChatbotEngine(KAMPUNG).classify(pesan)
    assert tag == intent


def test_sinonim_kata_daerah():
    engine = ChatbotEngine(KAMPUNG)
    assert engine.classify("siskamling malam ini siapa")[0] == "jadwal_ronda"
    assert engine.classify("ada maling masuk rumah tetangga")[0] == "darurat"


def test_fallback_di_luar_cakupan():
    hasil = ChatbotEngine(KAMPUNG).reply("harga beras hari ini")
    assert hasil["intent"] is None
    assert hasil["reply"] in KAMPUNG["fallback"]


def test_placeholder_dan_penanda_isian():
    hasil = ChatbotEngine(_terisi(KAMPUNG)).reply("sampah diambil hari apa ya")
    assert hasil["intent"] == "jadwal_sampah"
    assert "DATA_jadwal_sampah" in hasil["reply"]
    assert "{" not in hasil["reply"] and hasil["belum_diisi"] is False
    belum_diisi = copy.deepcopy(KAMPUNG)
    belum_diisi["data"]["kontak_pengurus"] = "[ISI: kontak pengurus]"
    kosong = ChatbotEngine(belum_diisi).reply("nomor pak rt berapa")
    assert kosong["belum_diisi"] is True and "[ISI" not in kosong["reply"]


def test_respons_darurat_menyebut_112():
    engine = ChatbotEngine(_terisi(KAMPUNG))
    for _ in range(10):
        assert "112" in engine.reply("ada kebakaran di gang sebelah")["reply"]


def test_explain_mengurutkan_skor():
    kandidat = ChatbotEngine(KAMPUNG).explain("jadwal angkut sampah")
    skor = [k["score"] for k in kandidat]
    assert skor == sorted(skor, reverse=True)


def test_validate_theme_mendeteksi_placeholder_tanpa_data():
    rusak = copy.deepcopy(KAMPUNG)
    rusak["intents"][3]["responses"][0] = "Jadwal: {kunci_tidak_ada}"
    assert any("kunci_tidak_ada" in m for m in validate_theme(rusak))


def test_akurasi_data_uji_rancangan_minimal_90_persen():
    akurasi, _ = evaluasi(KAMPUNG, baca_data("kampung"), 0.45)
    assert akurasi >= 0.9


def test_akurasi_data_uji_sulit_minimal_90_persen():
    akurasi, _ = evaluasi(KAMPUNG, baca_data("kampung_sulit"), 0.45)
    assert akurasi >= 0.9


def test_tombol_lanjutan_mengarah_ke_intent_lain():
    engine = ChatbotEngine(KAMPUNG)
    for intent in KAMPUNG["intents"]:
        for tombol in intent.get("next", []):
            tag, _ = engine.classify(tombol)
            assert tag is not None and tag != intent["tag"]
