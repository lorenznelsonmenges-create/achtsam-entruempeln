#!/usr/bin/env python3
"""
Wendepunkt — Schlanker Kontaktformular-Mailer
Empfängt Kontaktanfragen per POST /api/kontakt und versendet sie per SMTP über Hetzner.
Keine externen Abhängigkeiten erforderlich (reine Python 3 Standard-Bibliothek).
"""

import os
import sys
import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, formataddr
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path


# Unbuffered Output für sofortige Anzeige in journalctl
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)

script_dir = Path(__file__).resolve().parent

def load_env(env_path=None):
    """Lädt Schlüssel-Wert-Paare aus einer .env-Datei."""
    if env_path is None:
        env_file = script_dir / ".env"
    else:
        env_file = Path(env_path)

    if not env_file.is_file():
        print(f"[WARNUNG] Keine .env Datei unter {env_file} gefunden!", flush=True)
        return
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key not in os.environ:
                os.environ[key] = val


# Konfiguration laden
load_env()

SMTP_SERVER = os.environ.get("SMTP_SERVER", "mail.your-server.de")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER", "info@wendepunkt-ruf.de")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
MAIL_TO = os.environ.get("MAIL_TO", "info@wendepunkt-ruf.de")
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 8088))


def send_contact_email(sender_email: str, message: str, name: str = "") -> None:
    if not SMTP_PASS or SMTP_PASS == "hier_dein_passwort_eintragen":
        raise ValueError("SMTP_PASS ist nicht in der .env konfiguriert (Passwort ist leer oder noch der Platzhalter).")

    msg = MIMEMultipart("alternative")
    if name:
        msg["Subject"] = f"Neue Terminanfrage von {name} (Wendepunkt Website)"
        msg["Reply-To"] = formataddr((name, sender_email))
    else:
        msg["Subject"] = "Neue Terminanfrage (Wendepunkt Website)"
        msg["Reply-To"] = sender_email

    msg["From"] = formataddr(("Wendepunkt Kontaktformular", SMTP_USER))
    msg["To"] = MAIL_TO
    msg["Date"] = formatdate(localtime=True)

    name_row_text = f"Name: {name}\n" if name else ""
    text_body = f"""Neue Terminanfrage über die Website wendepunkt-ruf.de

{name_row_text}E-Mail: {sender_email}
Datum: {formatdate(localtime=True)}

Anliegen & Zeitfenster:
----------------------------------------
{message}
----------------------------------------

(Hinweis: Sie können direkt auf diese E-Mail antworten, um an {sender_email} zu schreiben.)
"""

    name_row_html = f'<div class="meta-row"><span class="meta-label">Name:</span> <strong>{name}</strong></div>' if name else ""
    html_body = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #31332c; line-height: 1.6; background-color: #fbf9f3; margin: 0; padding: 20px; }}
  .card {{ background-color: #ffffff; max-width: 600px; margin: 0 auto; border-radius: 12px; padding: 32px; box-shadow: 0 4px 12px rgba(49,51,44,0.06); }}
  .header {{ border-bottom: 2px solid #526447; padding-bottom: 16px; margin-bottom: 24px; }}
  .header h2 {{ color: #526447; margin: 0 0 6px 0; font-size: 22px; }}
  .meta {{ margin-bottom: 20px; font-size: 15px; }}
  .meta-row {{ margin-bottom: 8px; }}
  .meta-label {{ font-weight: bold; color: #526447; display: inline-block; width: 90px; }}
  .message-box {{ background-color: #f5f4ec; padding: 20px; border-radius: 8px; white-space: pre-wrap; font-size: 15px; border-left: 4px solid #526447; }}
  .footer {{ margin-top: 24px; font-size: 12px; color: #888888; text-align: center; }}
</style>
</head>
<body>
  <div class="card">
    <div class="header">
      <h2>Neue Terminanfrage</h2>
      <div style="font-size: 13px; color: #666;">Eingegangen über die Website wendepunkt-ruf.de</div>
    </div>
    <div class="meta">
      {name_row_html}
      <div class="meta-row"><span class="meta-label">E-Mail:</span> <a href="mailto:{sender_email}">{sender_email}</a></div>
      <div class="meta-row"><span class="meta-label">Datum:</span> {formatdate(localtime=True)}</div>
    </div>
    <div><strong>Anliegen &amp; Zeitfenster:</strong></div>
    <div class="message-box">{message}</div>
    <div class="footer">
      Sie können direkt auf diese E-Mail antworten, um {sender_email} zu kontaktieren.
    </div>
  </div>
</body>
</html>"""

    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=20) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)


class ContactHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, data: dict):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS, GET")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send_json(204, {})

    def do_GET(self):
        if self.path == "/api/health":
            self._send_json(200, {"status": "ok", "service": "wendepunkt-mailer"})
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/api/kontakt":
            self._send_json(404, {"error": "Not found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 65536:
                self._send_json(413, {"error": "Anfrage zu groß"})
                return

            raw_data = self.rfile.read(content_length)
            data = json.loads(raw_data.decode("utf-8"))

            # Spam-Schutz (Honeypot-Feld)
            # Wenn ein Bot das unsichtbare 'website'-Feld ausfüllt, antworten wir mit Erfolg, versenden aber nichts.
            if data.get("website"):
                print("Spam-Bot erkannt (Honeypot ausgelöst). Mail wird verworfen.", flush=True)
                self._send_json(200, {"success": True, "message": "Anfrage übermittelt."})
                return

            email = (data.get("email") or "").strip()
            message = (data.get("message") or "").strip()
            name = (data.get("name") or "").strip()

            if not email or not message:
                self._send_json(400, {"error": "Bitte füllen Sie Anliegen und E-Mail-Adresse aus."})
                return

            if "@" not in email or "." not in email:
                self._send_json(400, {"error": "Bitte geben Sie eine gültige E-Mail-Adresse ein."})
                return

            send_contact_email(sender_email=email, message=message, name=name)
            log_who = f"{name} ({email})" if name else email
            print(f"[{formatdate(localtime=True)}] E-Mail von {log_who} erfolgreich versendet.", flush=True)
            self._send_json(200, {"success": True, "message": "Ihre Anfrage wurde erfolgreich versendet."})

        except ValueError as ve:
            print(f"Konfigurationsfehler: {ve}", file=sys.stderr)
            self._send_json(500, {"error": "Mailserver ist noch nicht vollständig konfiguriert."})
        except Exception as e:
            print(f"Fehler beim Senden: {e}", file=sys.stderr)
            self._send_json(500, {"error": "Beim Senden ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut."})

    def log_message(self, format, *args):
        # Sauberes Logging ohne unnötiges Rauschen
        sys.stdout.write(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}\n")
        sys.stdout.flush()


def run():
    pass_state = "GESETZT" if SMTP_PASS and SMTP_PASS != "hier_dein_passwort_eintragen" else "NICHT GESETZT"
    print(f"Wendepunkt Mailer startet auf http://{HOST}:{PORT} ...", flush=True)
    print(f"SMTP Server: {SMTP_SERVER}:{SMTP_PORT} | Benutzer: {SMTP_USER} | Passwort: {pass_state}", flush=True)
    server = HTTPServer((HOST, PORT), ContactHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMailer wird beendet.", flush=True)
        server.server_close()


if __name__ == "__main__":
    run()
