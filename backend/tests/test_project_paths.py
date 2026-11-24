from app.core.config import Settings


def test_local_default_paths_do_not_change_with_working_directory(tmp_path, monkeypatch):
    for key in ('DATA_DIR','MEDIA_DIR','CHROMA_PATH'):
        monkeypatch.delenv(key,raising=False)
    before=Settings(_env_file=None)
    first=(before.data_dir.resolve(),before.media_dir.resolve(),str(before.chroma_path))
    monkeypatch.chdir(tmp_path)
    after=Settings(_env_file=None)
    assert (after.data_dir.resolve(),after.media_dir.resolve(),str(after.chroma_path))==first


def test_bundle_registry_cannot_escape_input_root(tmp_path, monkeypatch):
    import json
    import pytest
    from app.core.config import get_settings
    from app.core.paths import import_bundle_path
    inputs=tmp_path/'imports'
    inputs.mkdir()
    (inputs/'registry.json').write_text(json.dumps({'bad':{'directory':'../../outside'}}))
    monkeypatch.setattr(get_settings(),'data_dir',tmp_path)
    with pytest.raises(ValueError,match='BUNDLE_PATH_OUTSIDE_IMPORTS'):
        import_bundle_path('bad')
