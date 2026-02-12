from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timedelta
from app.repositories.consent_repo import ConsentRepository
from app.repositories.patient_repo import PatientRepository
from app.utils.otp import generate_otp, hash_otp, verify_otp
from app.core.config import settings

class ConsentService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ConsentRepository(db)
        self.patient_repo = PatientRepository(db)

    def request_otp(self, doctor_id, granting_hospital_id, patient_id, accessing_hospital_id):
        # Check patient exists
        patient = self.patient_repo.get(patient_id)
        if not patient:
            raise ValueError("Patient not found")

        # Create pending consent
        otp = generate_otp()
        otp_hash = hash_otp(otp)
        expiry = datetime.utcnow() + timedelta(seconds=settings.OTP_EXPIRE_SECONDS)

        consent = self.repo.create(
            id=uuid4().bytes,
            patient_id=patient_id.bytes,
            granting_hospital_id=granting_hospital_id.bytes,
            accessing_hospital_id=accessing_hospital_id.bytes,
            granted_by_user_id=doctor_id.bytes,
            otp_hash=otp_hash,
            otp_expiry=expiry,
            status='pending'
        )
        return consent, otp  # return OTP to send (mock)

    def verify_otp_and_activate(self, consent_id, otp):
        consent = self.repo.get(consent_id)
        if not consent:
            raise ValueError("Consent not found")
        if consent.status != 'pending':
            raise ValueError("Consent is not pending")
        if consent.otp_expiry < datetime.utcnow():
            raise ValueError("OTP expired")

        if not verify_otp(otp, consent.otp_hash):
            raise ValueError("Invalid OTP")

        # Activate for 1 hour
        now = datetime.utcnow()
        consent.status = 'active'
        consent.valid_from = now
        consent.valid_until = now + timedelta(hours=1)
        self.db.commit()
        return consent

    def check_access(self, patient_id, hospital_id):
        """Check if hospital has active consent for patient OR emergency override (handled separately)"""
        consent = self.repo.get_active_consent(patient_id, hospital_id)
        return consent is not None