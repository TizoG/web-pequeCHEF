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
};
export function DetalleReceta() {
    const { id } = useParams<{ id: string }>();
    const parseId = Number(id);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [receta, setReceta] = useState<Receta | null>(null);
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
                        <h1 className="receta__titulo">{receta.titulo}</h1>
                        <p className="receta__descripcion">
                            {receta.descripcion}
                        </p>
                        <div className="experiment">
                            <p>
                                <i>
                                    <MdTimer />
                                </i>
                                1 HORA <span>·</span>
                                <i>
                                    <FaWeightHanging />
                                </i>
                                DIFICIL <span>·</span>
                                <i>
                                    <TbToolsKitchen3 />
                                </i>
                                4 PERSONAS
                            </p>
                        </div>
                        <img
                            className="receta__imagen"
                            src={receta.imagen}
                            alt="Imagen de la receta"
                        />
                        <div className="container__contenido">
                            <div className="container__post-receta">
                                <p className="receta__descripcion__posterior">
                                    Imagine un suculento pollo con las vibrantes
                                    notas de limón y la riqueza aromática del
                                    ajo. Es una sinfonía de sabores que
                                    deleitará su paladar. Acompáñenos a
                                    profundizar en el arte de asar y descubrir
                                    los secretos para crear una obra maestra que
                                    no es solo una comida, sino una celebración
                                    de la artesanía culinaria. Mientras
                                    precalienta el horno, imagine la cocina
                                    llenándose del tentador aroma a hierbas y
                                    cítricos, preparando el escenario para una
                                    deliciosa comida que trasciende lo común. La
                                    expectación crece a medida que el pollo se
                                    asa a la perfección dorada, prometiendo una
                                    experiencia gastronómica que combina
                                    simplicidad y sofisticación. Tanto si es un
                                    chef experimentado como si es un novato en
                                    la cocina, esta receta le invita a
                                    convertirse en un artista culinario, creando
                                    una obra maestra que dejará una huella
                                    imborrable en sus invitados y seres
                                    queridos.
                                </p>
                                <h1 className="instrucciones">INSTRUCCIONES</h1>
                                <p className="instrucciones__p">
                                    Este puré es mucho más que una simple mezcla
                                    de ingredientes; es un abrazo cálido en cada
                                    cucharada. Su sabor, profundo y
                                    reconfortante, nos transporta al hogar,
                                    recordándonos el inconfundible aroma de un
                                    buen caldo de cocido, aunque en su
                                    preparación no haya ni rastro de carne. El
                                    repollo, con su riqueza en fibra, vitamina
                                    B6 y folato, aporta no solo nutrición, sino
                                    también una textura suave y envolvente. La
                                    zanahoria, con su dulzura natural, equilibra
                                    los sabores y tiñe el plato con un color
                                    vibrante que invita a degustarlo incluso
                                    antes de probarlo. Cada bocado es un
                                    homenaje a la sencillez bien lograda, una
                                    combinación armoniosa de ingredientes que,
                                    con su calidez, convierten este plato en una
                                    experiencia reconfortante e inolvidable.
                                </p>
                                <p className="pasos__title">
                                    PREPARAR LOS INGREDIENTES
                                </p>
                                <ul>
                                    <li className="pasos__li">
                                        Pela las zanahorias y córtalas en
                                        rodajas.
                                    </li>
                                    <li className="pasos__li">
                                        Pica la cebolla finamente.
                                    </li>
                                    <li className="pasos__li">
                                        Retira las hojas exteriores del repollo
                                        si están dañadas y corta el resto en
                                        tiras finas.
                                    </li>
                                </ul>
                                <p className="pasos__title">
                                    SALTEAR LAS VERDURAS
                                </p>
                                <ul>
                                    <li className="pasos__li">
                                        Calienta un chorrito de aceite de oliva
                                        en una olla a fuego medio.
                                    </li>
                                    <li className="pasos__li">
                                        Agrega las zanahorias y la cebolla,
                                        remueve ocasionalmente y sofríe durante
                                        un par de minutos.
                                    </li>
                                </ul>

                                <p className="pasos__title">
                                    COCINAR A FUEGO LENTO
                                </p>
                                <ul>
                                    <li className="pasos__li">
                                        Añade el repollo y mezcla bien con las
                                        demás verduras.
                                    </li>
                                    <li className="pasos__li">
                                        Vierte suficiente caldo o agua hasta
                                        cubrir completamente los ingredientes,
                                        más un poco extra.
                                    </li>
                                    <li className="pasos__li">
                                        Lleva a ebullición, luego reduce el
                                        fuego y deja cocer durante 15 minutos, o
                                        hasta que las zanahorias estén tiernas.
                                    </li>
                                    <li className="pasos__li">
                                        Si el líquido se evapora demasiado
                                        rápido, añade un poco más de agua.
                                    </li>
                                </ul>

                                <p className="pasos__title">
                                    TRITURAR HASTA OBTENER UNA TEXTURA SUAVE
                                </p>
                                <ul>
                                    <li className="pasos__li">
                                        Cuando las verduras estén bien cocidas,
                                        pásalas a la batidora junto con un poco
                                        del caldo de cocción.
                                    </li>
                                    <li className="pasos__li">
                                        Tritura hasta obtener una textura
                                        cremosa.
                                    </li>
                                    <li className="pasos__li">
                                        Si el puré queda demasiado espeso,
                                        agrega más caldo hasta lograr la
                                        consistencia deseada.
                                    </li>
                                </ul>

                                <p className="pasos__title">
                                    SERVIR Y DISFRUTAR
                                </p>
                                <ul>
                                    <li className="pasos__li">
                                        Sirve una ración en un cuenco, añade un
                                        chorrito de aceite de oliva virgen
                                        extra, mezcla bien y disfruta del puré
                                        tibio.
                                    </li>
                                </ul>
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
                                        <li>Rista de pan</li>
                                        <li>Trituradora</li>
                                        <li>Cuchillo</li>
                                        <li>Y mas ejemplos..</li>
                                    </ul>
                                </div>
                                <div className="container__ingredientes">
                                    <p className="pasos__title">
                                        VALOR NUTRICIONAL
                                    </p>
                                    <p className="pasos__subtitle">
                                        Ej: Cada 100gramos
                                    </p>
                                    <p className="p__calorias">
                                        <strong>Calorias:</strong> 250
                                    </p>
                                    <p className="p__calorias">
                                        <strong>Proteinas:</strong>30g
                                    </p>
                                    <p className="p__calorias">
                                        <strong>Total Fat:</strong>13g
                                    </p>
                                    <p className="p__calorias">
                                        <strong>Carbohidratos:</strong>5g
                                    </p>
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
