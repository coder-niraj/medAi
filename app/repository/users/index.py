from datetime import datetime
from os import name
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sympy import true
from models import triage
from models.user import User
from models.patient import PatientDemographics
from schemas.userSchema import ResearchConsent, UserCreate, UserDemoGraphics
from helpers.AES import AES256Service


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_user_demo_data(self, user_id):
        user_obj = (
            self.db.query(PatientDemographics)
            .filter(PatientDemographics.user_id == user_id)
            .first()
        )
        if user_obj:
            return False
        else:
            return True

    def create_user_demographics(self, petient_data: UserDemoGraphics, user_id):
        user_data = self.db.query(User).filter(User.id == user_id).first()
        demo_graphic_data = PatientDemographics(
            id=uuid.uuid4(),
            user_id=user_data.id,
            age_range=petient_data.age_range,
            gender=petient_data.gender,
            nationality=petient_data.nationality,
            region=petient_data.region,
            health_literacy=petient_data.health_literacy,
            chronic_conditions=petient_data.chronic_conditions,
            consent_for_research=user_data.research_consent,
            consent_given_at=user_data.consent_given_at,
            created_at=datetime.utcnow(),
        )
        self.db.add(demo_graphic_data)
        self.db.commit()
        self.db.refresh(demo_graphic_data)
        return {"demo_graphic": "updated"}

    def create_user(self, firebase_uid: str, firbase_email: str, user_dto: UserCreate):
        try:
            email_enc = AES256Service.encrypt(firbase_email)
            dob_enc = AES256Service.encrypt(user_dto.dob)

            user_model_obj = User(
                id=uuid.uuid4(),
                name=user_dto.name,
                email_enc=email_enc,
                preferred_language=user_dto.preferred_language,
                role=user_dto.role,
                firebase_uid=firebase_uid,
                created_at=datetime.utcnow(),
                research_consent=False,
                consent_given_at=None,
                triage_count=0,
                dob_enc=dob_enc,
            )
            self.db.add(user_model_obj)
            self.db.commit()
            self.db.refresh(user_model_obj)
            return user_model_obj
        except Exception as e:
            self.db.rollback()
            # Log error here
            print(e)
            raise HTTPException(status_code=500, detail="Database transaction failed")

    def get_user_by_firebase_uid(self, firebase_uid):
        return self.db.query(User).filter(User.firebase_uid == firebase_uid).first()

    def get_user_by_id(self, id):
        return self.db.query(User).filter(User.id == id).first()

    def delete_user(self, user_id):
        self.db.query(User).filter(User.firebase_uid == user_id).delete()

    def is_user_eligible_ai_feature(self, user_id):
        userObj = self.db.query(User).filter(User.id == user_id).first()
        if userObj:
            if userObj.research_consent:
                return True
            else:
                return False
        else:
            return False

    def update_consent_ToS(self, research_consent, user_id, phone):
        try:
            dateTimeGiven = datetime.utcnow()
            phone_enc = AES256Service.encrypt(phone)

            result = (
                self.db.query(User)
                .filter(User.id == user_id)
                .update(
                    {
                        "research_consent": research_consent,
                        "consent_given_at": dateTimeGiven,
                        "phone_enc": phone_enc,
                    }
                )
            )

            self.db.commit()
            if result == 0:
                print(result)
                return {"result": False, "Message": "User not found"}
            return {"result": True, "consent_given_at": dateTimeGiven}
        except Exception as e:
            self.db.rollback()
            print("error", e)
            return {"result": False, "Message": "Operation failed"}

    # def update_user(self,user_id):
    #     print("user consent accepted")
