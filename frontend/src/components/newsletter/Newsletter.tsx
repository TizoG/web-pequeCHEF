import './newwsletter.css';
export function Newsletter() {
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
                    />
                    <button className="input-button" type="submit">
                        SUSCRIBETE
                    </button>
                </div>
            </div>
        </section>
    );
}
