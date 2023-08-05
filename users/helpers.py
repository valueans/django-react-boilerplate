from datetime import datetime
import base64
import pyotp
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from .models import User


def generateRandom(email):
    return str(email) + str(datetime.date(datetime.now()))


def sendOtpEmail(user):
    keygen = generateRandom(user.email)
    key = base64.b32encode(keygen.encode())
    OTP = pyotp.HOTP(key, digits=4)
    otp = OTP.at(user.otp_counter)
    send_mail(
        "OTP verification",
        f"Your Verification OTP is {otp}",
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
    user = User.objects.filter(email=user.email).update(
        otp_counter=F("otp_counter") + 1
    )
    return True


def verifyOtp(user, otp):
    keygen = generateRandom(user.email)
    key = base64.b32encode(keygen.encode())
    OTP = pyotp.HOTP(key, digits=4)
    if OTP.verify(otp, user.otp_counter - 1):
        user = User.objects.filter(email=user.email).update(is_verified=True)
        return True
    return False
