VAL_ERR_MAP = {
    "missing": "هذا الحقل مطلوب",
    "value_error.missing": "هذا الحقل مطلوب",
    "string_too_short": "النص قصير جداً",
    "value_error.email": "البريد الإلكتروني غير صحيح",
    "type_error.integer": "يجب أن يكون الرقم صحيحاً",
    "greater_than_equal": "القيمة يجب أن تكون أكبر من أو تساوي {limit_value}",
}
MESSAGES = {
    "errors": {
        "missing": {"en": "This field is required.", "ar": "هذا الحقل مطلوب."},
        "value_error.missing": {
            "en": "This field is required.",
            "ar": "هذا الحقل مطلوب.",
        },
        "string_too_short": {"en": "Input is too short.", "ar": "المدخل قصير جدًا."},
        "value_error.email": {
            "en": "Invalid email address.",
            "ar": "عنوان البريد الإلكتروني غير صالح.",
        },
        "type_error.integer": {
            "en": "Must be a valid integer.",
            "ar": "يجب أن يكون رقمًا صحيحًا صالحًا.",
        },
        "greater_than_equal": {"en": "Value is too small.", "ar": "القيمة صغيرة جدًا."},
        "consent_required": {"en": "Consent is required.", "ar": "الموافقة مطلوبة."},
        "research_consent_required": {
            "en": "Research consent is required.",
            "ar": "الموافقة على البحث مطلوبة.",
        },
        "tos_required": {
            "en": "Terms of Service consent required.",
            "ar": "الموافقة على شروط الخدمة مطلوبة.",
        },
        "token_expired": {"en": "Token expired.", "ar": "انتهت صلاحية الرمز المميز."},
        "invalid_credentials": {
            "en": "Could not validate credentials.",
            "ar": "تعذر التحقق من صحة بيانات الاعتماد.",
        },
        "guest_access_denied": {
            "en": "Access denied. Guests are not authorized to use this feature.",
            "ar": "تم رفض الوصول. الضيوف غير مصرح لهم باستخدام هذه الميزة.",
        },
        "report_not_found": {
            "en": "Report not found.",
            "ar": "لم يتم العثور على التقرير.",
        },
        "user_not_found": {
            "en": "User not found.",
            "ar": "لم يتم العثور على المستخدم.",
        },
        "db_failed": {
            "en": "Database transaction failed.",
            "ar": "فشلت معاملة قاعدة البيانات.",
        },
        "operation_failed": {"en": "Operation failed.", "ar": "فشلت العملية."},
        "already_registered": {"en": "Already registered.", "ar": "مسجل بالفعل."},
        "registration_failed": {
            "en": "Could not complete registration",
            "ar": "لا يمكن إكمال التسجيل",
        },
        "firebase_invalid": {
            "en": "Invalid or expired Firebase Token.",
            "ar": "رمز Firebase غير صالح أو منتهي الصلاحية.",
        },
        "update_failed": {"en": "Update failed.", "ar": "فشل التحديث."},
        "demographic_exists": {
            "en": "Demographic data already exists.",
            "ar": "البيانات الديموغرافية موجودة بالفعل.",
        },
        "input_validation_failed": {
            "en": "Input validation failed. Please check the required fields.",
            "ar": "فشل التحقق من صحة المدخلات. يرجى التحقق من الحقول المطلوبة.",
        },
        "unexpected_error_occured": {
            "en": "An unexpected error occurred. Please try again later.",
            "ar": "حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى لاحقاً.",
        },
        "invalid_file_type": {"en": "Invalid file type.", "ar": "نوع ملف غير صالح."},
        "file_too_large": {
            "en": "File size is too large.",
            "ar": "حجم الملف كبير جدًا.",
        },
        "storage_failed": {
            "en": "Failed to save report to storage.",
            "ar": "فشل حفظ التقرير في وحدة التخزين.",
        },
        "image_only": {
            "en": "Image stored. Please also upload the written report from your radiologist for AI explanation.",
            "ar": "تم حفظ الصورة. يرجى أيضًا تحميل التقرير المكتوب من أخصائي الأشعة لشرحه بواسطة الذكاء الاصطناعي.",
        },
    },
}
