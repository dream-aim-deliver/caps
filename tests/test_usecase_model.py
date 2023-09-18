from lib.primary_ports import BaseInputPort, BaseOutputPort
from lib.usecase_models import BaseErrorResponseModel, BaseRequestModel, BaseResponseModel


class ResponseModel(BaseResponseModel):
    name: str


class RequestModel(BaseRequestModel):
    name: str
    type: str


#class UseCase(BaseInputPort):
    #def __init__(self, presenter: BaseOutputPort):
        #super().__init__()
        #self.presenter = presenter

    #def execute(self, requestModel: RequestModel):
        #self.logger.info(f"Executing {self} with {requestModel}")
        #responseModel = ResponseModel(name=requestModel.name)
        #self.logger.info(f"Returning {responseModel}")
        #self.presenter.presentSuccess(responseModel)


#class Presenter(BaseOutputPort):
    #def __init__(self):
        #super().__init__()

    #def presentSuccess(self, responseModel: BaseErrorResponseModel):
        #print(f"Success: {responseModel}")

    #def presentError(self, errorModel: BaseErrorResponseModel):
        #print(f"Error: {errorModel}")


#def test_usecase_models(caplog, capfd):
    #usecase: BaseInputPort = UseCase(presenter=Presenter())
    #requestModel = RequestModel(name="Test", type="Test")
    #usecase.execute(requestModel=requestModel)
    ## capture log output
    #out, err = capfd.readouterr()
    #assert out == "Success: status=True name='Test'\n"
