import { useEffect, useState } from 'react';
import { CardRecetas } from '../../components/recetas/CardRecetas';
import './paginawrapper.css';

type Receta = {
    id: number;
    imagen: string;
    titulo: string;
    descripcion: string;
    tiempo: string;
};
export function Comidas() {
    const [recetas, setRecetas] = useState<Receta[]>([]);
    const [isLoading, setLoading] = useState(true);
    const indice = 0;
    useEffect(() => {
        async function getRecetas() {
            try {
                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/recetas/categoria/comida`
                );

                if (!response.ok) {
                    throw new Error('Error en la carga de recetas');
                }
                const data = await response.json();
                setRecetas(data.recetas);
            } catch (err) {
                if (err instanceof Error) {
                    err.message;
                } else {
                    ('Ocurrio un error desconocido');
                }
            } finally {
                setLoading(false);
            }
        }
        getRecetas();
    }, []);
    const recetasVisibles = Array.isArray(recetas) ? recetas.slice(indice) : [];
    return (
        <section className="content-recetas__wrapper colection__cards spacing">
            <div className="colection__text">
                <p className="colection__badger">COMIDAS</p>
                <h2 className="colection__title">
                    ELIGE LA RECETA QUE MAS TE GUSTE
                </h2>
            </div>
            <div className="content-recetas__cards">
                {!isLoading && recetasVisibles.length > 0
                    ? recetasVisibles.map((receta) => (
                          <CardRecetas
                              key={receta.id}
                              description={receta.descripcion}
                              {...receta}
                          />
                      ))
                    : !isLoading && <p>No tenemos ninguna receta.</p>}
            </div>
        </section>
    );
}
