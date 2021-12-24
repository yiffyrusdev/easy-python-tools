from abc import abstractmethod
from typing import Protocol, TypeVar


class TableTypeClass(Protocol):
    @abstractmethod
    @property
    def name(self) -> str:
        pass

    @abstractmethod
    @property
    def db_name(self) -> str:
        pass

    @abstractmethod
    @property
    def fields(self) -> dict['TableField']:
        pass

    @abstractmethod
    @property
    def foreign_keys(self) -> set['TableFK']:
        pass


TableType = TypeVar('TableType', bound=TableTypeClass)
