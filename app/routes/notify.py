from fastapi import APIRouter, HTTPException

from app.config import settings
from app.services.email_sender import send_email as smtp_send_email
from app.services.store import get_item, mark_sent


router = APIRouter(prefix="/notify")


@router.post("/{invoice_id}/sms")
def send_sms(invoice_id: str):
    item = mark_sent(invoice_id, "sms")
    if not item:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"status": "sent", "item": item}


@router.post("/{invoice_id}/email")
def send_email(invoice_id: str):
    if not settings.smtp_to_email:
        raise HTTPException(status_code=400, detail="SMTP_TO_EMAIL not configured")

    item = get_item(invoice_id)
    if not item:
        raise HTTPException(status_code=404, detail="Invoice not found")

    subject = f"Invoice Payment Overdue: {invoice_id}"
    plain_body = (
        f"Invoice {invoice_id} is overdue. "
        f"Customer: {item['customer']}. "
        f"Days overdue: {item['days_overdue']}. "
        f"Outstanding amount: {item['amount']}."
    )
    html_body = f"""
    <div style="font-family: Arial, sans-serif; background:#0f1115; color:#e5e7eb; padding:24px;">
      <div style="max-width:600px; margin:0 auto; background:#111827; border-radius:16px; overflow:hidden;">
        <div style="background:linear-gradient(135deg,#6366f1,#22c55e); padding:20px 24px;">
          <h2 style="margin:0; color:white;">⚠️ Invoice Payment Overdue</h2>
          <p style="margin:6px 0 0; color:#e0e7ff;">Smart Notifications Engine</p>
        </div>
        <div style="padding:24px;">
          <p style="margin:0 0 16px; font-size:14px;">Hello Customer,</p>
          <p style="margin:0 0 20px; font-size:14px;">Your invoice <strong>{invoice_id}</strong> is now <strong>{item['days_overdue']} days overdue</strong>.</p>
          <div style="background:#0b1220; border:1px solid #1f2937; border-radius:12px; padding:16px;">
            <h4 style="margin:0 0 12px; color:#93c5fd;">Invoice Details</h4>
            <table style="width:100%; font-size:13px; color:#e5e7eb;">
              <tr><td style="padding:4px 0;">Invoice ID:</td><td style="padding:4px 0;"><strong>{invoice_id}</strong></td></tr>
              <tr><td style="padding:4px 0;">Customer:</td><td style="padding:4px 0;">{item['customer']}</td></tr>
              <tr><td style="padding:4px 0;">Outstanding Amount:</td><td style="padding:4px 0;">₪{item['amount']}</td></tr>
              <tr><td style="padding:4px 0;">Days Overdue:</td><td style="padding:4px 0; color:#f97316;">{item['days_overdue']} days</td></tr>
            </table>
          </div>
          <p style="margin:20px 0 0; font-size:12px; color:#9ca3af;">Please arrange payment at your earliest convenience. If payment has already been made, please disregard this notice.</p>
        </div>
      </div>
    </div>
    """
    smtp_send_email(
        settings.smtp_to_email,
        subject=subject,
        body=plain_body,
        html_body=html_body,
    )
    item = mark_sent(invoice_id, "email")
    if not item:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"status": "sent", "item": item}


@router.get("/auto")
def auto_status():
    return {
        "enabled": settings.auto_scan_enabled,
        "interval_seconds": settings.auto_scan_seconds,
    }


@router.post("/auto/{state}")
def set_auto(state: str):
    if state not in {"on", "off"}:
        raise HTTPException(status_code=400, detail="Invalid state")
    settings.auto_scan_enabled = state == "on"
    return {"enabled": settings.auto_scan_enabled}
