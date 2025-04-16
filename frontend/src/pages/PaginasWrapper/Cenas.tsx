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
export function Cenas() {
    const [recetas, setRecetas] = useState<Receta[]>([]);
    const [isLoading, setLoading] = useState(true);
    const indice = 0;
    useEffect(() => {
        async function getRecetas() {
            try {
                const response = await fetch(
                    'http://localhost:8000/recetas/categoria/cenas'
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
        <section className="content-recetas__wrapper colection__cards">
            <h1>Cenas</h1>
            <div>
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
