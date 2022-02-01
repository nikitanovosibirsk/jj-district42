from baby_steps import given, then, when
from district42_exp_types.unordered import UnorderedContainsValidationError
from multidict import CIMultiDict
from th import PathHolder

from district42 import schema
from jj_district42 import HistoryResponseSchema
from jj_district42.types.istr import IStrSchema
from revolt import substitute
from valera import validate
from valera.errors import ExtraElementValidationError

from ._utils import make_history_response


def test_response_history_no_headers_validation():
    with given:
        sch = HistoryResponseSchema()
        headers = {"user_id": "1"}
        resp = make_history_response(headers=CIMultiDict(headers))

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == []


def test_response_history_dict_headers_validation():
    with given:
        headers = {"user_id": "1"}
        sch = substitute(HistoryResponseSchema(), {"headers": headers})
        resp = make_history_response(headers=CIMultiDict(headers))

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == []


def test_response_history_dict_headers_case_validation():
    with given:
        actual_headers = {"User_Id": "1"}
        expected_headers = {"user_id": "1"}
        sch = substitute(HistoryResponseSchema(), {"headers": expected_headers})
        resp = make_history_response(headers=CIMultiDict(actual_headers))

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == []


def test_response_history_list_headers_validation():
    with given:
        headers = [["user_id", "1"]]
        sch = substitute(HistoryResponseSchema(), {"headers": headers})
        resp = make_history_response(headers=CIMultiDict(headers))

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == []


def test_response_history_list_multiple_headers_validation():
    with given:
        headers = [["user_id", "1"], ["user_id", "2"]]
        sch = substitute(HistoryResponseSchema(), {"headers": headers})
        resp = make_history_response(headers=CIMultiDict(headers))

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == []


def test_response_history_dict_headers_validation_error():
    with given:
        expected_headers = {"user_id": "1"}
        actual_headers = {"user_id": "2"}
        sch = substitute(HistoryResponseSchema(), {"headers": expected_headers})
        resp = make_history_response(headers=CIMultiDict(actual_headers))

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == [
            UnorderedContainsValidationError(PathHolder()["headers"], schema.list([
                IStrSchema()("user_id"),
                schema.str("1")
            ])),
            ExtraElementValidationError(PathHolder()["headers"], ["user_id", "2"], 0)
        ]


def test_response_history_list_headers_validation_error():
    with given:
        expected_headers = [["user_id", "1"]]
        actual_headers = [["user_id", "2"]]
        sch = substitute(HistoryResponseSchema(), {"headers": expected_headers})
        resp = make_history_response(headers=CIMultiDict(actual_headers))

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == [
            UnorderedContainsValidationError(PathHolder()["headers"], schema.list([
                IStrSchema()("user_id"),
                schema.str("1")
            ])),
            ExtraElementValidationError(PathHolder()["headers"], ["user_id", "2"], 0),
        ]


def test_response_history_list_multiple_headers_validation_error():
    with given:
        expected_headers = [["user_id", "1"], ["user_id", "2"]]
        actual_headers = [["user_id", "1"]]
        sch = substitute(HistoryResponseSchema(), {"headers": expected_headers})
        resp = make_history_response(headers=CIMultiDict(actual_headers))

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == [
            UnorderedContainsValidationError(PathHolder()["headers"], schema.list([
                IStrSchema()("user_id"),
                schema.str("2")
            ])),
        ]
