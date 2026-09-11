from last_seen import write_last_seen,read_last_seen

def test_last_seen(tmp_path,monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_last_seen(300)
    result=read_last_seen()
    assert result==300

def test_read_last_seen_no_file(tmp_path,monkeypatch):
    monkeypatch.chdir(tmp_path)
    result=read_last_seen()
    assert result==None

def test_invalid_json(tmp_path,monkeypatch):
    monkeypatch.chdir(tmp_path)
    d=tmp_path/"state.json"
    d.write_text("not json")
    result=read_last_seen()
    assert result is None
