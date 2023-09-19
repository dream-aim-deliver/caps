from abc import abstractmethod
from typing import Generic
from lib.bac import BaseAbstractClass
from lib.usecase_models import (
    TBaseErrorResponseModel,
    TBaseRequestModel,
    TBaseResponseModel,
)


class BaseInputPort(BaseAbstractClass, Generic[TBaseRequestModel]):
    """
    Abstract base class for input ports.

    :param requestModel: The request model to use.
    :type requestModel: TBaseRequestModel
    """

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
