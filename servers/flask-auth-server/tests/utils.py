def decode_response_data(response):
    """Decodes Flask test client response data from bytes to string."""
    return response.data.decode("utf-8")