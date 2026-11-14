from src.train_register import build_dataset

def test_training_dataset_shape_and_target():
    df = build_dataset()
    assert len(df) == 600
    assert "churn" in df.columns
    assert set(df["churn"].unique()) == {0, 1}
    assert df.drop(columns=["churn"]).shape[1] == 6
