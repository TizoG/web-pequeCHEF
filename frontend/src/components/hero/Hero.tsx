import './hero.css';

import { Button } from '../Button';
import { useEffect, useState } from 'react';

type RecetaDestacada = {
    id: number;
    titulo: string;
    descripcion: string;
    imagen: string;
};
export function Hero() {
    const [isRecetaDestacada, setRecetaDestacada] =
        useState<RecetaDestacada | null>(null);
    useEffect(() => {
        fetch('http://127.0.0.1:8000/destacada')
            .then((res) => res.json())
            .then((data) => {
                setRecetaDestacada(data);
            });
    }, []);
    return (
        <section className="content">
            <img
                src={isRecetaDestacada?.imagen}
                alt={isRecetaDestacada?.titulo}
                className="content__img"
            />
            <div className="content__text">
                <h1 className="content__text__h1">
                    {isRecetaDestacada?.titulo
                        ? isRecetaDestacada.titulo.toUpperCase()
                        : 'LIBERE LA EXCELENCIA CULINARIA'}
                </h1>
                {/* Hemos quitado un div que englobaba el parrafo , puedes verlo en el css */}
                <p className="content__text__p">
                    {isRecetaDestacada?.descripcion ||
                        'Explora un mundo de sabores, descubre recetas artesanales y deja que el aroma de nuestra pasión por la cocina llene tu cocina.'}
                </p>
                {/**Aqui hemos quitado el div, que engloba el boton */}
                <Button
                    type="button"
                    text="EXPLORE RECIPES"
                    className="button"
                    to={`/recetas/${isRecetaDestacada?.id}`}
                />
            </div>
        </section>
    );
}

//TODO: Mejorar la documentación
//TODO: Mejorar la funcionalidad para que se adapte a diferentes tamaños de pantalla
//TODO: Crear enlaces a otras secciones
