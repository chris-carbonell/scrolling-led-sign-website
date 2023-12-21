# Dependencies

# fastapi
import fastapi
from fastapi import routing

# Fixes

# in swagger docs, the name was originally title cased
# fix it to remove title casing
def new_generate_operation_summary(*, route: routing.APIRoute, method: str) -> str:
    if route.summary:
        return route.summary
    return route.name.replace("_", " ")
fastapi.openapi.utils.generate_operation_summary = new_generate_operation_summary  # replace