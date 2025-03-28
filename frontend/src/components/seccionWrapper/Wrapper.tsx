import { Button } from '../Button';
import './wrapper.css';

export function Wrapper() {
    return (
        <section className="content-wrapper">
            <div className="text-wrapper">
                <p className="explora">EXPLORA</p>
                <h2 className="title">NUESTROS DIVERSOS PLATOS</h2>
                <p className="parrafo">
                    Si eres un entusiasta del desayuno, un conocedor de delicias
                    saladas o estás en busca de postres irresistibles, nuestra
                    selección curada tiene algo para satisfacer todos los
                    paladares.
                </p>
                <Button className="button-wrapper" text="VER MAS" />
            </div>
            <div>
                <div>
                    <i></i>
                    <p></p>
                </div>
                <div>
                    <i></i>
                    <p></p>
                </div>
                <div>
                    <i></i>
                    <p></p>
                </div>
                <div>
                    <i></i>
                    <p></p>
                </div>
                <div>
                    <i></i>
                    <p></p>
                </div>
            </div>
        </section>
    );
}
