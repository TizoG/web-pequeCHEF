import { Button } from '../Button';
import './recetas.css';
type Props = {
    id: number;
    imagen: string;
    titulo: string;
    description: string;
    tiempo: string;
};

export function CardRecetas({
    id,
    imagen,
    titulo,
    description,
    tiempo,
}: Props) {
    return (
        <div className="card-receta">
            <img
                src={
                    imagen.startsWith('http')
                        ? imagen
                        : `http://localhost:8000/${imagen}`
                }
                alt="Imagen de la receta"
                className="img"
            />
            <div className="card-receta__content">
                <h3 className="card-receta__content__h3">{titulo}</h3>
                <p className="card-receta__content__p">{description}</p>
                <div className="card-receta__content__button">
                    <p>{tiempo}</p>

                    <Button
                        text="VER RECETA"
                        className="card-button"
                        to={`/recetas/${id}`}
                    />
                </div>
            </div>
        </div>
    );
}
