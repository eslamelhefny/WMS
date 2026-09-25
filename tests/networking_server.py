"""Serve a disposable database for networking integration tests."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server

if __name__ == "__main__":
    server.DATA_DIR = Path(__file__).resolve().parent / "test-data"
    server.DATA_DIR.mkdir(exist_ok=True)
    server.DB_PATH = server.DATA_DIR / "test.db"
    server.STORE_PATH = server.DATA_DIR / "store.json"
    server.EXCEL_PATH = server.DATA_DIR / "tasks.xlsx"
    sample = server.new_store(master_data={"networking": {"contacts": [{"id": "c1", "name": "Persistence test"}], "visits": [{"id": "v1", "contactId": "c1", "activity": "Instructors"}]}})
    server.save_store(sample)
    assert server.load_store()["masterData"]["networking"] == sample["masterData"]["networking"]
    assert server.normalize_store({})["masterData"] == {}
    server.save_store(server.new_store(user={"name": "Review Manager", "position": "Academy Manager", "email": "review@andalusia.net", "defaultView": "plan"}))
    print("Disposable test server: http://127.0.0.1:8876", flush=True)
    server.ThreadingHTTPServer(("127.0.0.1", 8876), server.Handler).serve_forever()
