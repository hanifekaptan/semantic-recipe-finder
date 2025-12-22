import sys
import builtins
import numpy as np
import pandas as pd
from pathlib import Path

from app.services.data_loader import load_npy_memmap, load_parquet, load_startup_resources


def test_load_npy_memmap_success(tmp_path: Path):
    emb = np.arange(12, dtype=np.float64).reshape(3, 4)
    ids = np.array([1, 2, 3], dtype=np.int32)
    emb_file = tmp_path / "embs.npy"
    ids_file = tmp_path / "ids.npy"
    np.save(emb_file, emb)
    np.save(ids_file, ids)

    embs_loaded, ids_loaded = load_npy_memmap(str(emb_file), str(ids_file))
    assert embs_loaded.shape == (3, 4)
    assert ids_loaded.shape == (3,)
    assert embs_loaded.dtype == np.float32
    assert ids_loaded.dtype == np.int64


def test_load_parquet_sets_index_success(tmp_path: Path):
    df = pd.DataFrame({"recipe_id": [10, 11], "name": ["A", "B"]})
    p = tmp_path / "md.parquet"
    df.to_parquet(p, index=False)

    df_loaded = load_parquet(str(p))
    assert df_loaded is not None
    # index should be set to recipe_id column if present
    assert "recipe_id" in df_loaded.columns
    assert list(df_loaded.index) == [10, 11]


def test_load_startup_resources_model_import_failure(tmp_path: Path, monkeypatch):
    # prepare valid emb/ids files
    emb = np.zeros((2, 3), dtype=np.float32)
    ids = np.array([5, 6], dtype=np.int64)
    emb_file = tmp_path / "embs2.npy"
    ids_file = tmp_path / "ids2.npy"
    np.save(emb_file, emb)
    np.save(ids_file, ids)

    # force import error for sentence_transformers
    real_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name.startswith("sentence_transformers"):
            raise ModuleNotFoundError("mocked missing")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    embs, ids_loaded, model, df, err = load_startup_resources(
        str(emb_file), str(ids_file), "some-model", str(tmp_path / "no.parquet")
    )

    assert embs is not None and ids_loaded is not None
    assert model is None
    assert err is not None and "model load error" in err
