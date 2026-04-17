import time
from fastapi import   HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def logger(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    process_time = time.time() - start
    print(f"{request.method} {request.url} completed in {process_time:.3f}s")

    return response

async def validation_exception_handler(request: Request, exc: RequestValidationError)->JSONResponse:
    errors = []
    for err in exc.errors():
        errors.append({
            "field": str(err["loc"][-1]),
            "message": err["msg"],
            "type": err["type"]
        })
        
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_FAILED",
                "message": "Input validation failed. Please check the required fields.",
                "message_ar": "فشل التحقق من البيانات. يرجى التحقق من الحقول المطلوبة.",
                "details": {"fields": errors}
            }
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException)->JSONResponse:
    # This allows you to pass a dict as 'detail' for complex errors
    # or a simple string for quick errors.
    detail = exc.detail
    if isinstance(detail, str):
        detail = {"message": detail, "code": "HTTP_ERROR"}

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": detail.get("code", "ERROR"),
                "message": detail.get("message"),
                "message_ar": detail.get("message_ar", "خطأ في النظام"),
                "details": detail.get("details", {})
            }
        }
    )

async def global_exception_handler(request: Request, exc: Exception)->JSONResponse:
    # Log the full error to your backend console/GCP Logs
    print(f"System Error: {str(exc)}") 
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please try again later.",
                "message_ar": "حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى لاحقاً.",
                "trace_id": "req_audit_log_id" # You can generate a UUID here
            }
        }
    )


# raise HTTPException(status_code=403, detail={
#     "code": "GUEST_LIMIT_EXCEEDED",
#     "message": "Guest limit reached. Please login.",
#     "message_ar": "تم الوصول إلى الحد الأقصى للضيوف. يرجى تسجيل الدخول."
# })

# raise HTTPException(status_code=403, detail={
#     "code": "CONSENT_REQUIRED",
#     "message": "You must accept the terms to use AI features.",
#     "message_ar": "يجب الموافقة على الشروط لاستخدام ميزات الذكاء الاصطناعي."
# })