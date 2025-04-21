import { useState } from 'react';
import './newwsletter.css';
export function Newsletter() {
    const [isEmail, setEmail] = useState('');
    const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setEmail(e.target.value);
    };
    const handleEmail = async () => {
        if (!isEmail.trim()) {
            alert('Introduce un email');
        }

        try {
            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/suscribirse`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email: isEmail }),
                }
            );

            if (!response.ok) {
                alert('Error al suscribirte');
                setEmail('');
                throw new Error('Error al suscribirte');
            }
            const data = await response.json();
            alert('Te has suscrito correctamente.');
            setEmail('');
        } catch (error) {
            if (error instanceof Error) {
                error.message;
            } else {
                ('Ocurrio un error desconocido');
            }
        }
    };

    return (
        <section className="newsletter">
            <div className="newsletter__container">
                <p className="newsletter__container__p">SUSCRIBETE</p>
                <h1 className="newsletter__container__h1">
                    ÚNETE A LA DIVERSION ¡SUSCRIBETE AHORA!
                </h1>
                <p className="newsletter__container__p__text">
                    Suscríbete a nuestro boletín para recibir una porción
                    semanal de recetas, consejos de cocina y conocimientos
                    exclusivos directamente en tu bandeja de entrada.
                </p>
                <div className="newsletter__container__input">
                    <input
                        className="input"
                        type="text"
                        placeholder="Ingresa tu correo"
                        value={isEmail}
                        onChange={handleEmailChange}
                        onKeyDown={(e) => e.key === 'Enter' && handleEmail()}
                    />
                    <button
                        className="input-button"
                        type="submit"
                        onClick={handleEmail}
                    >
                        SUSCRIBETE
                    </button>
                </div>
            </div>
        </section>
    );
}
