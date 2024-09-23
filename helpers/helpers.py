import requests


def get_request_headers(response: requests.Response) -> str:
    headers = response.request.headers
    return "".join(f" --header '{k}: {headers.get(k)}'" for k in headers)


def get_request_body(response: requests.Response) -> str:
    if not response.request.body:
        return ""
    return f" --data-raw '{response.request.body.decode('utf8')}'"


def get_response_body(response: requests.Response) -> str:
    try:
        return response.json()
    except requests.JSONDecodeError:
        return ""


def get_request_info(response: requests.Response) -> str:
    return (
        f"Request:\n"
        f"curl --location --request {response.request.method} '{response.request.url}'"
        f"{get_request_headers(response)}"
        f"{get_request_body(response)}"
        f"\n\nResponse:\n"
        f"{get_response_body(response)}\n"
    )
