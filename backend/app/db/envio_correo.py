import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
from models import Suscriptores
from database import session_local
import os
from dotenv import load_dotenv

load_dotenv()


def enviar_correo_a_suscriptores(db: Session, titulo_receta: str, enlace_receta: str):
    # Obtener los correos de los suscriptores
    suscriptores = db.query(Suscriptores.email).all()
    emails = [suscriptor.email for suscriptor in suscriptores]

    # Datos de autenticación de Gmail
    correo_remitente = os.getenv("EMAIL_REMITENTE")  # Tu correo de Gmail
    # Si usas verificación en dos pasos, usa la contraseña de aplicación
    contrasena = os.getenv("EMAIL_PASSWORD")

    # Crear el contenido del correo
    cuerpo = f"""
    <h1>¡Nueva receta publicada!</h1>
    <p>Enlace de la receta: <a href="{enlace_receta}">{enlace_receta}</a></p>
    <p>¡Gracias por su visita!</p>
    """

    # Configuración de la conexión SMTP de Gmail
    try:
        # Conexión al servidor SMTP de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Habilitar la seguridad TLS
        server.login(correo_remitente, contrasena)  # Iniciar sesión en Gmail

        # Enviar correo a cada suscriptor
        for email in emails:
            mensaje = MIMEMultipart()
            mensaje['From'] = correo_remitente
            mensaje['To'] = email
            mensaje['Subject'] = f"¡Nueva receta publicada: {titulo_receta}!"
            mensaje.attach(MIMEText(cuerpo, 'html'))

            server.sendmail(correo_remitente, email, mensaje.as_string())
            print(f"Correo enviado a {email}")

    except Exception as e:
        print(f"Error al enviar correos: {e}")

    finally:
        server.quit()


if __name__ == "__main__":
    db = session_local()
    enviar_correo_a_suscriptores(
        db, "Receta 1", "https://www.pequechef.com/receta1")
    db.close()
