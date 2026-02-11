from fastapi import APIRouter, HTTPException
import boto3
from app.controllers.notify_controller import (
    send_email_notification,
    send_sms_notification,
    get_auto_status,
    set_auto_state,
)


router = APIRouter(prefix="/notify")
sns = boto3.client("sns", region_name="us-east-1")

@router.post("/{invoice_id}/sms")
def send_sms(invoice_id: str):
    response = sns.publish(
        TopicArn="arn:aws:sns:us-east-1:228281126655:test",
        Message=f"Reminder: Invoice #{invoice_id} is overdue. Please arrange payment at your earliest convenience. Thank you.",
        Subject="Test Notification"  # optional (email only)
    )
    result = response.get("MessageId")

    if not result:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"status": "sent", "item": result}


@router.post("/{invoice_id}/email")
def send_email(invoice_id: str):
    result = send_email_notification(invoice_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if result == "missing_smtp":
        raise HTTPException(status_code=400, detail="SMTP_TO_EMAIL not configured")
    if result == "send_failed":
        raise HTTPException(status_code=500, detail="Email send failed")
    return {"status": "sent", "item": result}


@router.get("/auto")
def auto_status():
    return get_auto_status()


@router.post("/auto/{state}")
def set_auto(state: str):
    if state not in {"on", "off"}:
        raise HTTPException(status_code=400, detail="Invalid state")
    return set_auto_state(state)
