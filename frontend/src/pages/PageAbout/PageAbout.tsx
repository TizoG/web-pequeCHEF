import './PageAbout.css';
import imagenCocinero from '../../assets/imagenCocinero.png';
export function PageAbout() {
    return (
        <section className="container-section">
            <div className="container-page-about">
                <div className="container-page-about__title">
                    <h1>BIENVENIDO A MI RINCÓN CULINARIO</h1>
                </div>
                <div className="container-page-about__text">
                    <p>
                        Me alegra enormemente que hayas decidido conocer más
                        sobre mí y sobre esta pasión que me impulsa día a día.
                        Mi amor por la cocina comenzó desde muy pequeño y, con
                        el tiempo, se transformó en una forma de compartir
                        momentos especiales en familia. Este espacio nace para
                        inspirarte a ti y a los más pequeños con recetas
                        sencillas, divertidas y, sobre todo, saludables.
                    </p>
                </div>
            </div>
            <div className="container-page-about__mi-historia">
                <img src={imagenCocinero} alt="imagen de un cocinero" />
                <div>
                    <h2>MI HISTORIA</h2>
                    <p>
                        Desde que tengo memoria, la cocina ha sido mi refugio y
                        mi lugar para experimentar. Recuerdo con cariño cómo me
                        fascinaba observar a mi madre y a mi abuela preparar
                        platos deliciosos, aprender sus secretos y descubrir
                        nuevos sabores. Con el paso de los años, esa pasión me
                        llevó a explorar recetas de todo el mundo, adaptándolas
                        para hacerlas accesibles a los paladares infantiles.
                    </p>
                    <p>
                        Soy un cocinero aficionado, autodidacta en muchas
                        ocasiones, pero siempre impulsado por el deseo de crear
                        platos que, además de sabrosos, sean divertidos y
                        educativos para los niños. Cada receta que preparo es
                        una pequeña aventura que busco compartir con aquellos
                        que, como yo, disfrutan del placer de cocinar y comer en
                        familia.
                    </p>
                </div>
            </div>
            <div className="container-page-about__inspiracion">
                <div className="container-page-about__inspiracion__text">
                    <h2>La inspiración detrás de la web</h2>
                    <p>
                        La idea de esta web surgió del deseo de fomentar hábitos
                        alimenticios saludables en los más pequeños y de
                        convertir la cocina en un espacio de creatividad y
                        aprendizaje. Aquí encontrarás recetas especialmente
                        pensadas para niños, con ingredientes equilibrados,
                        preparaciones sencillas y un toque de diversión. Quiero
                        que cada plato se convierta en una experiencia única que
                        se disfrute tanto en la cocina como en la mesa.
                    </p>
                    <strong className="container-page-about__inspiracion__text__strong">
                        ¿Por qué recetas para niños?
                    </strong>
                    <ul>
                        <li>
                            <strong>Salud y nutrición:</strong> Es fundamental
                            que los más pequeños disfruten de una alimentación
                            balanceada y variada.
                        </li>
                        <li>
                            <strong>Educación culinaria:</strong> Cocinar en
                            familia es una actividad educativa que enseña
                            responsabilidad, trabajo en equipo y la importancia
                            de los alimentos naturales.
                        </li>
                        <li>
                            <strong>Diversión y creatividad:</strong> La cocina
                            ofrece infinitas posibilidades para experimentar,
                            inventar y compartir momentos inolvidables.
                        </li>
                    </ul>
                </div>
                <div className="container-page-about__inspiracion__text">
                    <h2>Mi filosofía en la cocina</h2>
                    <p>
                        Creo firmemente que la comida une a las personas y que
                        una receta puede ser el inicio de una gran historia
                        familiar. Mi enfoque es sencillo: recetas accesibles,
                        ingredientes frescos y preparaciones que inviten a
                        experimentar sin miedo a equivocarse. Cada plato es una
                        invitación a acercarse a la cocina, a descubrir nuevos
                        sabores y a disfrutar de momentos de felicidad en
                        familia.
                    </p>
                    <ul>
                        <li>
                            <strong>Simplicidad:</strong> Recetas fáciles de
                            seguir, adaptadas a la rutina diaria de las
                            familias.
                        </li>
                        <li>
                            <strong>Salud y sabor:</strong> Ingredientes que
                            aportan nutrición y placer en cada bocado.
                        </li>
                        <li>
                            <strong>Pasión y amor:</strong> Cada receta lleva un
                            toque personal, una anécdota o un recuerdo que la
                            hace única.
                        </li>
                    </ul>
                </div>
            </div>
            <div className="conectemos">
                <h2>Conectemos</h2>
                <p>
                    Mi objetivo no es solo compartir recetas, sino también crear
                    una comunidad donde padres, abuelos y niños puedan
                    inspirarse, aprender y disfrutar juntos. Te invito a
                    suscribirte al newsletter, seguirme en mis redes sociales y,
                    sobre todo, a que te animes a compartir tus propias
                    creaciones en la cocina.
                </p>
                <p>
                    ¡Gracias por ser parte de esta aventura culinaria! Si tienes
                    alguna pregunta, comentario o simplemente quieres compartir
                    tu experiencia, no dudes en ponerte en contacto. Estoy aquí
                    para ayudarte y aprender junto a ti.
                </p>
            </div>
        </section>
    );
}
