from src.ocr_cleaning import clean_ocr_text


def test_clean_ocr_text_basic():
    raw = "N,N-dimethy-\ntryptam1ne"
    cleaned = clean_ocr_text(raw)
    assert "dimethyltryptamine" not in cleaned  # we didn't fix spelling yet
    assert "N,N-dimethy" in cleaned
