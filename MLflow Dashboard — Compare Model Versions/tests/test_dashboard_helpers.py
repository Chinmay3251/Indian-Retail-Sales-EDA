from app.dashboard import version_rows

class FakeVersion:
    version = "2"
    run_id = "run-123"
    status = "READY"
    creation_timestamp = 1700000000000
    description = "second model version"
    source = "runs:/run-123/model"
    aliases = ["champion"]

class FakeRunData:
    metrics = {"accuracy": 0.91, "f1_score": 0.88}
    params = {"model_type": "LogisticRegression"}
    tags = {"mlflow.source.name": "train.py"}

class FakeRun:
    data = FakeRunData()

class FakeClient:
    def get_run(self, run_id):
        assert run_id == "run-123"
        return FakeRun()

class FakeModel:
    latest_versions = [FakeVersion()]

def test_version_rows_extracts_version_and_run_metadata():
    rows = version_rows(FakeClient(), FakeModel())
    assert len(rows) == 1
    assert rows[0]["version"] == "2"
    assert rows[0]["metrics"]["accuracy"] == 0.91
    assert rows[0]["params"]["model_type"] == "LogisticRegression"
    assert rows[0]["aliases"] == "champion"
