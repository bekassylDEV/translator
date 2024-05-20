from typing import Union

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import (
    validation_error_definition,
    validation_error_response_definition,
)
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def http422_error_handler(
    _: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    details = exc.errors()
    modified_details = []

    for error in details:
        loc = error["loc"]
        field = loc[0] if len(loc) == 1 else loc[1]
        modified_details.append({"field": field, "message": error["msg"], "type": error["type"]})

    return JSONResponse(
        {"errors": jsonable_encoder(modified_details)},
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )


validation_error_definition["properties"] = {
    "field": {"title": "Field", "type": "string"},
    "message": {"title": "Message", "type": "string"},
    "type": {"title": "Error Type", "type": "string"},
}
validation_error_definition["required"] = ["field", "message", "type"]

validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    },
}
