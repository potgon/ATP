def get_required_fields(request, fields: list[str]) -> dict:
    missing_fields = [field for field in fields if field not in request.data]
    if missing_fields:
        raise Exception(
            f"Missing required fields: {', '.join(missing_fields)}")

    return {field: request.data.get(field) for field in fields}
