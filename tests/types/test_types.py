"""
Tests for type hinting
"""

from abc import abstractmethod
from typing import Any, Generic, Type, TypeVar
from lib.bac import BaseAbstractClass
from lib.primary_ports import BaseInputPort, BaseOutputPort
from lib.usecase_models import BaseErrorResponseModel, BaseRequestModel, BaseResponseModel

from tests.types.mypytest_prototype import (
    get_mypy_version,
    absolute_path_mypy_result,
    get_type_errors_and_line_numbers,
    object_mypy_error_report)


mypy_version = get_mypy_version()
print(f"mypy version: {mypy_version}")

mypy_result = absolute_path_mypy_result(__file__)
errors, errors_line_numbers = get_type_errors_and_line_numbers(mypy_result)

print(f"\nmypy errors for the whole file: {errors}")
print(f"\nmypy error line numbers: {errors_line_numbers}\n")


class ResponseModel(BaseResponseModel):
    name: str


class RequestModel(BaseRequestModel):
    name: str
    type: str



def test_subtypes():
    """
    Directly from mypy 1.5.1 docs:
    https://mypy.readthedocs.io/en/stable/kinds_of_types.html#the-type-of-class-objects
    """

    class User:
        # Defines fields like name, email
        pass

    class BasicUser(User):
        def upgrade(self):
            """Upgrade to Pro"""

    class ProUser(User):
        def pay(self):
            """Pay bill"""


    U = TypeVar('U', bound=User)

    def new_user(user_class: type[U]) -> U:
        user = user_class()
        # (Here we could write the user object to a database)
        return user


    mypy_test_error_report = object_mypy_error_report(new_user, __file__)

    # assert that the class is not in the mypy error report
    assert len(mypy_test_error_report) == 0


    beginner = new_user(BasicUser)  # Inferred type by the IDE is BasicUser
    beginner.upgrade()  # OK for the IDE



def test_badly_typed_subtype_intuition():
    """
    This will very clearly fail, as we have not type hinted appropriatedly
    """

    class BadlyTypedUseCase(BaseInputPort):
        def __init__(self, presenter: BaseOutputPort):
            super().__init__()
            self.presenter = presenter

        # mypy should capture that RequestModel is not BaseRequestModel, when written like this
        def execute(self, requestModel: RequestModel):
            pass

    mypy_test_error_report = object_mypy_error_report(BadlyTypedUseCase, __file__)

    # assert that the class is in the mypy error report
    assert len(mypy_test_error_report) != 0
    # assert how many intentional type errors you coded
    assert len(mypy_test_error_report) == 1


def test_badly_typed_type_and_subtype():
    """
    However, straightfowardly applying the docs to our example, we DON'T get a pass from mypy
    see: https://mypy.readthedocs.io/en/stable/kinds_of_types.html#the-type-of-class-objects
    """

    TRequestModel = TypeVar('TRequestModel', bound=BaseRequestModel)

    class BaseInputPort_MypyDocs(BaseAbstractClass):
        def __init__(self):
            super().__init__()

        @abstractmethod
        def execute(self, requestModel: type[TRequestModel]):
            pass


    class UseCase(BaseInputPort_MypyDocs):
        def __init__(self, presenter: BaseOutputPort):
            super().__init__()
            self.presenter = presenter

        # from the docs, it looks like mypy should capture that RequestModel IS BaseRequestModel,
        # when written like this...
        def execute(self, requestModel: RequestModel):
            pass

    mypy_test_error_report_1 = object_mypy_error_report(BaseInputPort_MypyDocs, __file__)
    # The BaseInputPort_MypyDocs works fine    
    assert len(mypy_test_error_report_1) == 0

    mypy_test_error_report_2 = object_mypy_error_report(UseCase, __file__)
    # ...but UseCase doesn't!
    assert len(mypy_test_error_report_2) != 0
    # We should get a single mypy error at def execute...
    # ...in fact, it is the same error as in the previous test
    assert len(mypy_test_error_report_2) == 1


def test_generic_typed_type_and_subtype():
    """
    Generic NOW SOLVES OUR PROBLEMS!!!!!
    """

    TRequestModel = TypeVar('TRequestModel', bound=BaseRequestModel)

    class BaseInputPort_Generic(BaseAbstractClass, Generic[TRequestModel]):
        # NOTE: the Generic here did the trick
        def __init__(self):
            super().__init__()

        @abstractmethod
        def execute(self, requestModel: TRequestModel):
            pass

    class UseCase(BaseInputPort_Generic):
        def __init__(self, presenter: BaseOutputPort):
            super().__init__()
            self.presenter = presenter

        def execute(self, requestModel: RequestModel):
            pass

    # Now everything works as expected
    mypy_test_error_report_1 = object_mypy_error_report(BaseInputPort_Generic, __file__)
    mypy_test_error_report_2 = object_mypy_error_report(UseCase, __file__)

    assert len(mypy_test_error_report_1) == 0
    assert len(mypy_test_error_report_2) == 0


