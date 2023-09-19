from abc import abstractmethod
from typing import Generic
from lib.bac import BaseAbstractClass
from lib.usecase_models import (
    BaseErrorResponseModel,
    BaseRequestModel,
    BaseResponseModel,
    TBaseErrorResponseModel,
    TBaseRequestModel,
    TBaseResponseModel,
)


class BaseInputPort(BaseAbstractClass, Generic[TBaseRequestModel]):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def execute(self, requestModel: TBaseRequestModel) -> None:
        pass


class BaseOutputPort(BaseAbstractClass, Generic[TBaseResponseModel, TBaseErrorResponseModel]):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def presentSuccess(self, responseModel: TBaseResponseModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def presentError(self, errorModel: TBaseErrorResponseModel) -> None:
        raise NotImplementedError
