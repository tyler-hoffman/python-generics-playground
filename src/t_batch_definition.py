from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar
from typing_extensions import Self


_TBatchDefinition = TypeVar("_TBatchDefinition", bound="BatchDefinition")


# batch definitions

class BatchDefinition(ABC):

    def get_batch_request(self: Self) -> BatchRequest[Self]:
        return BatchRequest(batch_definition=self)


@dataclass
class SqlBatchDefinition(BatchDefinition):
    column_name: str

@dataclass
class SparkBatchDefinition(BatchDefinition):
    batching_regex: str


# assets

@dataclass
class DataAsset(ABC, Generic[_TBatchDefinition]):
    batch_definition: list[BatchDefinition] = field(default_factory=list)

    def add_batch_definition(self, batch_definition: _TBatchDefinition) -> _TBatchDefinition:
        self.batch_definition.append(batch_definition)
        return batch_definition

    @abstractmethod
    def get_batches(self, batch_request: BatchRequest[_TBatchDefinition]) -> list[Batch]:
        ...

class SqlDataAsset(DataAsset[SqlBatchDefinition]):

    def add_batch_definition_for_column(self, column_name: str) -> SqlBatchDefinition:
        batch_definition = SqlBatchDefinition(column_name=column_name)
        return self.add_batch_definition(batch_definition)

    def get_batches(self, batch_request: BatchRequest[SqlBatchDefinition]) -> list[Batch]:
        name = f"I was created with {batch_request.batch_definition.column_name}"
        return [Batch(name=name)]

class SparkDataAsset(DataAsset[SparkBatchDefinition]):

    def add_batch_definition_for_directory(self, regex: str) -> SparkBatchDefinition:
        batch_definition = SparkBatchDefinition(batching_regex=regex)
        return self.add_batch_definition(batch_definition)

    def get_batches(self, batch_request: BatchRequest[SparkBatchDefinition]) -> list[Batch]:
        name = f"I was created with {batch_request.batch_definition.batching_regex}"
        return [Batch(name=name)]



# batches and their requests

@dataclass
class BatchRequest(Generic[_TBatchDefinition]):
    batch_definition: _TBatchDefinition


@dataclass
class Batch:
    name: str

def _sql():
    asset = SqlDataAsset()
    batch_definition = asset.add_batch_definition_for_column(column_name="column_name")
    batch_request = batch_definition.get_batch_request()
    batches = asset.get_batches(batch_request)

    print(batch_request.batch_definition.column_name)
    print(batches)

def _spark():
    asset = SparkDataAsset()
    batch_definition = asset.add_batch_definition_for_directory(regex="my-regex")
    batch_request = batch_definition.get_batch_request()
    batches = asset.get_batches(batch_request)

    print(batch_request.batch_definition.batching_regex)
    print(batches)
    

if __name__ == "__main__":
    _sql()
    _spark()