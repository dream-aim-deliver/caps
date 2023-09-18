from abc import abstractmethod
from lib.bac import BaseAbstractClass
from lib.usecase_models import BaseErrorResponseModel, BaseRequestModel, BaseResponseModel


class BaseInputPort(BaseAbstractClass):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def execute(self, requestModel: BaseRequestModel) -> None:
        pass


class BaseOutputPort(BaseAbstractClass):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def presentSuccess(self, responseModel: BaseResponseModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def presentError(self, errorModel: BaseErrorResponseModel) -> None:
        raise NotImplementedError
