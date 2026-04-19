from fastapi import APIRouter

from app.api.users.index import UsersController

router = APIRouter(prefix="/users")
router.get("/me/data-export")(UsersController.user_data_export)
router.delete("/me")(UsersController.delete_account)
