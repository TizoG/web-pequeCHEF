import './hero.css';
import pasta from '../../assets/pasta.jpg';
import { Button } from '../Button';

export function Hero() {
    return (
        <section className="content">
            <img src={pasta} alt="Imagen del hero" className="content__img" />
            <div className="content__text">
                <h1 className="content__text__h1">
                    LIBERE LA EXCELENCIA CULINARIA
                </h1>
                {/* Hemos quitado un div que englobaba el parrafo , puedes verlo en el css */}
                <p className="content__text__p">
                    Explora un mundo de sabores, descubre recetas artesanales y
                    deja que el aroma de nuestra pasión por la cocina llene tu
                    cocina.
                </p>
                {/**Aqui hemos quitado el div, que engloba el boton */}
                <Button
                    type="button"
                    text="EXPLORE RECIPES"
                    className="button"
                />
            </div>
        </section>
    );
}

//TODO: Mejorar la documentación
//TODO: Mejorar la funcionalidad para que se adapte a diferentes tamaños de pantalla
//TODO: Crear enlaces a otras secciones
