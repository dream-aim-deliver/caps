from abc import abstractmethod
from lib.bac import BaseAbstractClass
from lib.usecase_models import BaseErrorResponseModel, BaseRequestModel, BaseResponseModel


class BaseInputPort(BaseAbstractClass):

    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def execute(self, requestModel: BaseRequestModel):
        pass

class BaseOutputPort(BaseAbstractClass):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def presentSuccess(self, responseModel: BaseResponseModel):
        raise NotImplementedError
    
    @abstractmethod
    def presentError(self, errorModel: BaseErrorResponseModel):
        raise NotImplementedError
    


