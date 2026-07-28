import os

os.environ["OMP_NUM_THREADS"] = "1"

from src.pipeline.train_pipeline import TrainPipeline

if __name__ == "__main__":
    pipeline = TrainPipeline()

    artifact = pipeline.run_pipeline()

    print("\n" + "=" * 60)
    print("Training Pipeline Executed Successfully!")
    print("=" * 60)
    print(artifact)