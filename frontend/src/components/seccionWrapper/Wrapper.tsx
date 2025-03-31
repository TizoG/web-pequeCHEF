import { Button } from '../Button';
import './wrapper.css';
import { MdOutlineBreakfastDining } from 'react-icons/md';
import { LuSalad } from 'react-icons/lu';
import { MdOutlineLunchDining } from 'react-icons/md';
import { LuDessert } from 'react-icons/lu';
import { LiaCookieBiteSolid } from 'react-icons/lia';
import { JSX } from 'react';

type ProprsIcons = {
    icon: JSX.Element;
    text: string;
};
function WrapperIcons({ icon, text }: ProprsIcons) {
    return (
        <div className="content-icons__container">
            {icon}
            <p className="text__icons">{text}</p>
        </div>
    );
}

const icons = [
    { icon: <MdOutlineBreakfastDining className="icons" />, text: 'BREAKFAST' },
    { icon: <LuSalad className="icons" />, text: 'LUNCH' },
    { icon: <MdOutlineLunchDining className="icons" />, text: 'DINNER' },
    { icon: <LuDessert className="icons" />, text: 'DESSERT' },
    { icon: <LiaCookieBiteSolid className="icons" />, text: 'QUICK BITE!' },
];

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
            <div className="content-icons">
                {icons.map((icon, index) => (
                    <WrapperIcons key={index} {...icon} />
                ))}
            </div>
        </section>
    );
}
