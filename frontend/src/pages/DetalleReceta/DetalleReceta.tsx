import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { MdTimer } from 'react-icons/md';
import { FaWeightHanging } from 'react-icons/fa';
import { TbToolsKitchen3 } from 'react-icons/tb';
import './detalleRecetas.css';

type Ingrediente = {
    nombre: string;
    cantidad: string;
    unidad: string;
};

type Receta = {
    id: number;
    imagen: string;
    titulo: string;
    descripcion: string;
    pasos: string;
    tiempo: string;
    ingredientes: Ingrediente[];
    descripcion_original: string;
    equipamiento: string[];
    valores_nutricionales: {
        [key: string]: { cantidad: string; unidad: string };
    };
    tiempo_cocina: string;
    dificultad: 'Fácil' | 'Intermedio' | 'Difícil';
    porciones: number;
};
export function DetalleReceta() {
    const { id } = useParams<{ id: string }>();
    const parseId = Number(id);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [receta, setReceta] = useState<Receta | null>(null);
    const ordenValoresNutricionales = [
        'calorias',
        'proteinas',
        'grasas',
        'carbohidratos',
        'fibra',
    ];
    useEffect(() => {
        async function fetchRecetas() {
            try {
                const url =
                    parseId > 0
                        ? `http://127.0.0.1:8000/recetas/${parseId}`
                        : 'http://127.0.0.1:8000/recetas';

                const response = await fetch(url);

                if (!response.ok) {
                    throw new Error('Error en la carga de la receta');
                }
                const data = await response.json();
                console.log(data);

                setReceta(data);
            } catch (err) {
                if (err instanceof Error) {
                    setError(err.message);
                } else {
                    setError('Error inesperado');
                }
            } finally {
                setLoading(false);
            }
        }
        fetchRecetas();
    }, [parseId]);
    useEffect(() => {
        console.log('Estado de receta actualizado:', receta);
    }, [receta]);

    return (
        <section className="container">
            <div className="container-receta">
                <p className="explora centrado">RECETA</p>
                {loading && <p>Cargando receta...</p>}
                {error && <p>{error}</p>}
                {!loading && !error && !receta && <p>Receta no encontrada</p>}
                {receta && (
                    <div>
                        <h1 className="receta__titulo">
                            {receta.titulo.toUpperCase()}
                        </h1>
                        <p className="receta__descripcion">
                            {receta.descripcion}
                        </p>
                        <div className="experiment">
                            <p>
                                <i>
                                    <MdTimer />
                                </i>
                                {receta.tiempo_cocina} <span>·</span>
                                <i>
                                    <FaWeightHanging />
                                </i>
                                {receta.dificultad} <span>·</span>
                                <i>
                                    <TbToolsKitchen3 />
                                </i>
                                {receta.porciones} PERSONAS
                            </p>
                        </div>
                        <img
                            className="receta__imagen"
                            src={`http://localhost:8000/${receta.imagen}`}
                            alt="Imagen de la receta"
                        />
                        <div className="container__contenido">
                            <div className="container__post-receta">
                                <p className="receta__descripcion__posterior">
                                    {receta.descripcion_original}
                                </p>
                                <h1 className="instrucciones">INSTRUCCIONES</h1>

                                {/* Renderizamos los pasos*/}
                                <div className="container__pasos">
                                    {receta.pasos &&
                                        Object.entries(receta.pasos).map(
                                            ([key, value]) => (
                                                <div
                                                    key={key}
                                                    className="pasos"
                                                >
                                                    <p className="pasos__title">
                                                        {key.toUpperCase()}
                                                    </p>
                                                    <ul>
                                                        <li className="pasos__li">
                                                            {Array.isArray(
                                                                value
                                                            ) ? (
                                                                <ul>
                                                                    {value.map(
                                                                        (
                                                                            item,
                                                                            index
                                                                        ) => (
                                                                            <li
                                                                                key={
                                                                                    index
                                                                                }
                                                                            >
                                                                                {
                                                                                    item
                                                                                }
                                                                            </li>
                                                                        )
                                                                    )}
                                                                </ul>
                                                            ) : (
                                                                value
                                                            )}
                                                        </li>
                                                    </ul>
                                                </div>
                                            )
                                        )}
                                </div>
                            </div>
                            <div className="container__ingredientes__nutricion">
                                <div className="container__ingredientes">
                                    <p className="pasos__title">INGREDIENTES</p>
                                    <ul>
                                        {receta.ingredientes.map(
                                            (ing, index) => (
                                                <li key={index}>
                                                    {ing.nombre} -{' '}
                                                    {ing.cantidad} {ing.unidad}
                                                </li>
                                            )
                                        )}
                                    </ul>
                                </div>
                                <div className="container__ingredientes">
                                    <p className="pasos__title">
                                        EQUIPAMIENTO NECESARIO PARA PREPARAR
                                    </p>
                                    <ul>
                                        {receta.equipamiento.map((equip) => (
                                            <li>{equip}</li>
                                        ))}
                                    </ul>
                                </div>
                                <div className="container__ingredientes">
                                    <p className="pasos__title">
                                        VALOR NUTRICIONAL
                                    </p>
                                    {ordenValoresNutricionales.map((key) => {
                                        const value =
                                            receta.valores_nutricionales[key];
                                        return (
                                            <p
                                                key={key}
                                                className="p__calorias"
                                            >
                                                <strong>
                                                    {key
                                                        .charAt(0)
                                                        .toUpperCase() +
                                                        key.slice(1)}
                                                    :
                                                </strong>{' '}
                                                {value.cantidad} {value.unidad}
                                            </p>
                                        );
                                    })}
                                </div>
                                <p className="anotacion">
                                    NOTA: LOS VALORES NUTRICIONALES SON
                                    APROXIMADOS
                                </p>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </section>
    );
}
