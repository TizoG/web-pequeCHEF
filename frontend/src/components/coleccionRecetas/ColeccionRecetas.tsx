import { useEffect, useState } from 'react';
import { CardRecetas } from '../recetas/CardRecetas';
import './coleccionRecetas.css';

type Props = {
    href: number;
    text: string;
    setCategoria: React.Dispatch<React.SetStateAction<number>>;
    isCategoria: number;
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
    { href: 0, text: 'ALL' },
    { href: 1, text: 'VEGAN' },
    { href: 2, text: 'BREACKFAST' },
    { href: 3, text: 'LUNCH' },
    { href: 4, text: 'DINNER' },
    { href: 5, text: 'DESSERT' },
    { href: 6, text: 'QUICK BITE!' },
];

type Receta = {
    id: number;
    imagen: string;
    titulo: string;
    descripcion: string;
    tiempo: string;
};
type CategoriaRecetas = {
    id: number;
};
export function ColeccionRecetas() {
    const [isCategoria, setCategoria] = useState(0);
    const [recetas, setRecetas] = useState<Receta[]>(() => []);

    const [indice, setIndice] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    useEffect(() => {
        async function fetchRecetas({ id = 0 }: CategoriaRecetas) {
            try {
                const url =
                    id === 0
                        ? 'http://127.0.0.1:8000/recetas'
                        : `http://127.0.0.1:8000/recetas/categoria/${id}`;

                const response = await fetch(url);

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
        fetchRecetas({ id: isCategoria });
    }, [isCategoria]);
    const recetasVisibles = Array.isArray(recetas)
        ? recetas.slice(indice, indice + 6)
        : [];
    return (
        <section className="content-colection">
            <div className="colection__text">
                <p className="colection__badger">RECETAS</p>
                <h2 className="colection__title">
                    ELIGE LA RECETA QUE MAS TE GUSTE
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
