from dataclasses import dataclass

# The output of the data ingestion is a data artifact
@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str