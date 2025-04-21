import { useEffect, useState } from 'react';
import { CardRecetas } from './CardRecetas';
import { FaChevronRight } from 'react-icons/fa6';
import { FaChevronLeft } from 'react-icons/fa';
import './recetas.css';
type Receta = {
    id: number;
    imagen: string;
    titulo: string;
    descripcion: string;
    tiempo: string;
};
export function Recetas() {
    const [recetas, setRecetas] = useState<Receta[]>(() => []);

    const [indice, setIndice] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function fetchRecetas() {
            try {
                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/destacada/nuevas`
                );

                if (!response.ok) {
                    throw new Error('Error en la carga de recetas');
                }
                const data = await response.json();
                setRecetas(data.recetas);
            } catch (err) {
                if (err instanceof Error) {
                    setError(err.message);
                } else {
                    setError('Ocurrio un error desconocido');
                }
            } finally {
                setLoading(false);
            }
        }
        fetchRecetas();
    }, []);
    const recetasVisibles = Array.isArray(recetas)
        ? recetas.slice(indice, indice + 2)
        : [];

    function avanzar() {
        if (indice + 2 < recetas.length) {
            setIndice(indice + 2);
        }
    }

    function retroceder() {
        if (indice > 0) {
            setIndice(indice - 2);
        }
    }
    return (
        <section className="content-carrousel__recetas">
            <div className="content-carrousel__content">
                <h2 className="content-carrousel__content__h2">
                    {' '}
                    ULTIMAS RECETAS
                </h2>
                <div className="content-carrousel__content__buttons">
                    <button
                        onClick={retroceder}
                        disabled={indice === 0}
                        className={`${indice === 0 ? 'btn__disabled' : 'btn'}`}
                    >
                        <FaChevronLeft
                            className={`${
                                indice === 0 ? 'btn-icon__disabled' : 'btn-icon'
                            }`}
                        />
                    </button>
                    <button
                        onClick={avanzar}
                        disabled={indice + 2 >= recetas.length}
                        className={`${
                            indice + 2 >= recetas.length
                                ? 'btn__disabled'
                                : 'btn'
                        }`}
                    >
                        <FaChevronRight
                            className={`${
                                indice + 2 >= recetas.length
                                    ? 'btn-icon__disabled'
                                    : 'btn-icon'
                            }`}
                        />
                    </button>
                </div>
            </div>
            {loading && <p>Cargando recetas...</p>}
            {error && <p>Error: {error}</p>}

            <div className="content-recetas">
                {!loading && !error && recetasVisibles.length > 0
                    ? recetasVisibles.map((receta) => (
                          <CardRecetas
                              key={receta.id}
                              description={receta.descripcion}
                              {...receta}
                          />
                      ))
                    : !loading && <p>No hay recetas disponibles</p>}
            </div>
        </section>
    );
}
