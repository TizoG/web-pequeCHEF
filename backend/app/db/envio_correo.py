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
    <!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>¡Nueva Receta de Tortilla de Espinacas!</title>
    </head>
    <body
        style="
            font-family: 'Arial', sans-serif;
            background-color: #f8f8f8;
            padding: 20px;
        "
    >
        <div
            style="
                background-color: #ffffff;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
            "
        >
            <div style="text-align: center; margin-bottom: 25px">
                <img
                    src="https://via.placeholder.com/150/8fbc8f/ffffff?Text=Tortilla"
                    alt="Tortilla de Espinacas"
                    style="
                        display: block;
                        margin: 0 auto 15px;
                        border-radius: 50%;
                    "
                />
                <h1 style="color: #333333; margin-top: 0; margin-bottom: 10px">
                    ¡Una Tortilla Súper Sabrosa! 🍳
                </h1>
                <p style="color: #555555; font-size: 16px">
                    Descubre cómo hacer una tortilla de espinacas y queso muy
                    fácil y rica.
                </p>
            </div>

            <div
                style="
                    margin-bottom: 20px;
                    border-left: 5px solid #8fbc8f;
                    padding-left: 15px;
                "
            >
                <h2 style="color: #333333; margin-top: 0; margin-bottom: 10px">
                    ¿Qué vamos a cocinar hoy?
                </h2>
                <p style="color: #666666; font-size: 15px">
                    ¡Una deliciosa tortilla de espinacas con mucho queso! Es
                    perfecta para desayunar, cenar o como una comida rápida.
                </p>
            </div>

            <div
                style="
                    margin-top: 25px;
                    padding: 15px;
                    background-color: #f9f9f9;
                    border-radius: 5px;
                    border: 1px solid #eee;
                "
            >
                <h3 style="color: #333333; margin-top: 0; margin-bottom: 10px">
                    Ingredientes que necesitamos:
                </h3>
                <ul style="color: #666666; padding-left: 20px; font-size: 15px">
                    <li>4 huevos</li>
                    <li>1 taza de espinacas frescas picadas</li>
                    <li>½ taza de queso rallado (¡el que más te guste!)</li>
                    <li>¼ taza de leche</li>
                    <li>Un poquito de sal y pimienta</li>
                    <li>1 cucharada de aceite de oliva</li>
                </ul>
            </div>

            <div
                style="
                    margin-top: 25px;
                    padding: 15px;
                    background-color: #f9f9f9;
                    border-radius: 5px;
                    border: 1px solid #eee;
                "
            >
                <h3 style="color: #333333; margin-top: 0; margin-bottom: 10px">
                    Pasos para cocinar:
                </h3>
                <ol style="color: #666666; padding-left: 20px; font-size: 15px">
                    <li>
                        Bate los huevos con la leche, la sal y la pimienta en un
                        tazón.
                    </li>
                    <li>
                        Añade las espinacas picadas y el queso rallado a los
                        huevos y mezcla bien.
                    </li>
                    <li>Calienta el aceite en una sartén a fuego medio.</li>
                    <li>Vierte la mezcla de huevo en la sartén.</li>
                    <li>
                        Cocina a fuego lento hasta que la tortilla esté casi
                        hecha por abajo.
                    </li>
                    <li>
                        Con cuidado, dale la vuelta para que se cocine por el
                        otro lado hasta que esté dorada y esponjosa.
                    </li>
                    <li>¡Listo! Sirve tu deliciosa tortilla caliente.</li>
                </ol>
            </div>

            <p
                style="
                    color: #777777;
                    font-size: 14px;
                    margin-top: 30px;
                    text-align: center;
                "
            >
                ¡Esperamos que disfrutes mucho cocinando y comiendo esta rica
                tortilla! 😊
            </p>
        </div>
    </body>
</html>

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

    print("¡Correos enviados correctamente!")
