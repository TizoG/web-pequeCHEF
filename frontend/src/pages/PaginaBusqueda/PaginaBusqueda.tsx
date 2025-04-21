import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { CardRecetas } from '../../components/recetas/CardRecetas';
import './paginaBusqueda.css';

type Receta = {
    id: number;
    imagen: string;
    titulo: string;
    descripcion: string;
    tiempo: string;
};
export function PaginaBusqueda() {
    const [result, setResult] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const location = useLocation();
    const [recetas, setRecetas] = useState<Receta[]>(() => []);
    const [indice, setIndice] = useState(0);

    useEffect(() => {
        const queryParams = new URLSearchParams(location.search);

        async function fetchResults() {
            const query = queryParams.get('query');
            try {
                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/recetas/search/${query}`
                );
                if (!response.ok) {
                    throw new Error('Error en la busqueda de recetas');
                }
                const data = await response.json();
                setRecetas(data.recetas);
            } catch (err) {
                if (err instanceof Error) {
                    err.message;
                } else {
                    setError('Ocurrio un error desconocido');
                }
            } finally {
                setLoading(false);
            }
        }
        fetchResults();
    }, [location.search]);
    const recetasVisibles = Array.isArray(recetas)
        ? recetas.slice(indice, indice + 6)
        : [];

    if (loading) return <p>Cargando recetas ...</p>;
    if (error) return <p>{error}</p>;
    if (recetas.length === 0) return <p>No se encontraron recetas.</p>;

    return (
        <div className="container__busquedas">
            <h1 className="busquedas__titulo">Resultados de la búsqueda</h1>
            <div className="colection__cards">
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
            <div className="botones">
                <button
                    disabled={indice === 0}
                    onClick={() => setIndice(indice - 6)}
                    className="boton__anterior__posterior"
                >
                    Anterior
                </button>
                <button
                    disabled={indice + 6 >= recetas.length}
                    onClick={() => setIndice(indice + 6)}
                    className="boton__anterior__posterior"
                >
                    Siguiente
                </button>
            </div>
        </div>
    );
}
