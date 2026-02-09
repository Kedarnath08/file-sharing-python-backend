
from fastapi import HTTPException, status
import traceback

def handle_internal_server_error(exc: Exception):
    """
    Function to handle internal server errors and format the response.

    Args:
        exc (Exception): The caught exception.

    Returns:
        HTTPException: An HTTPException with a 500 status code and formatted response.
    """
    exception_details = traceback.format_exc()
    print(f"An error occurred due to '{exc}' : {exception_details}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "status_code" : 500,
            "message" : "An unexpected error occurred. Please try again later."
        }
    )