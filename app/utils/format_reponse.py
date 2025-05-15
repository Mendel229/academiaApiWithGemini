from fastapi.responses import JSONResponse

def create_response(success: bool, status: int, message):
    return JSONResponse(
        status_code=status,
        content={
            "success": success,
            "status": status,
            "message": message
        }
    )
