import { useEffect, useState } from 'react';
import { CardRecetas } from '../recetas/CardRecetas';
import './coleccionRecetas.css';

type Props = {
    href: string;
    text: string;
    setCategoria: React.Dispatch<React.SetStateAction<string>>;
    isCategoria: string;
};

function ColeccionButton({ href, text, setCategoria, isCategoria }: Props) {
    return (
        <div>
            <button
                className={`coleccion-button ${
                    href === isCategoria ? 'active' : ''
                }`}
                type="button"
                onClick={() => setCategoria(href)}
            >
                {text}
            </button>
        </div>
    );
}

const coleccionLinks = [
    { href: 'all', text: 'ALL' },
    { href: 'vegano', text: 'VEGANO' },
    { href: 'carnes', text: 'CARNES' },
    { href: 'pastas', text: 'PASTAS' },
    { href: 'pescado', text: 'PESCADOS' },
    { href: 'sopas', text: 'SOPAS' },
    { href: 'guisos', text: 'GUISOS' },
    { href: 'arroz', text: 'ARROCES' },
];

type Receta = {
    id: number;
    imagen: string;
    titulo: string;
    descripcion: string;
    tiempo: string;
};

export function ColeccionRecetas() {
    const [isCategoria, setCategoria] = useState<string>('all');
    const [recetas, setRecetas] = useState<Receta[]>(() => []);

    const [indice] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    useEffect(() => {
        async function fetchRecetas() {
            try {
                const url =
                    isCategoria === 'all'
                        ? `${import.meta.env.VITE_API_URL}/recetas`
                        : `${
                              import.meta.env.VITE_API_URL
                          }/recetas/categoria/${isCategoria}`;

                const response = await fetch(url);

                if (!response.ok) {
                    throw new Error('Error en la carga de recetas');
                }
                const data = await response.json();
                console.log(data);
                setRecetas(data.recetas);
            } catch (err) {
                if (err instanceof Error) {
                    setError(err.message);
                } else {
                    setError('Ocurrió un error desconocido');
                }
            } finally {
                setLoading(false);
            }
        }
        fetchRecetas();
    }, [isCategoria]);
    const recetasVisibles = Array.isArray(recetas)
        ? recetas.slice(indice, indice + 6)
        : [];
    return (
        <section className="content-colection">
            <div className="colection__text">
                <p className="colection__badger">RECETAS</p>
                <h2 className="colection__title">
                    ALGUNAS DE NUESTRAS RECETAS
                </h2>
                <p className="colection__p">
                    Con nuestra variada colección de recetas tenemos algo para
                    satisfacer todos los paladares.
                </p>
            </div>
            <div className="colection__buttons">
                {coleccionLinks.map((link, index) => (
                    <ColeccionButton
                        isCategoria={isCategoria}
                        setCategoria={setCategoria}
                        key={index}
                        {...link}
                    />
                ))}
            </div>
            {loading && <p>Cargando recetas...</p>}
            {error && <p>Error: {error}</p>}
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
        </section>
    );
}
