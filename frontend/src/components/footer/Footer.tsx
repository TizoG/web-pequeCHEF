import { NavbarItem } from '../header/Navbar';
import logoo from '../../assets/logoo.png';
import { FaTiktok } from 'react-icons/fa';
import { ImFacebook2 } from 'react-icons/im';
import { RiInstagramFill } from 'react-icons/ri';
import { FaYoutube } from 'react-icons/fa';
import './footer.css';
import { JSX } from 'react';

const navLinks = [
    { label: 'HOME', href: '#' },
    { label: 'RECIPES', href: '#' },
    { label: 'COOKING TIPS', href: '#' },
    { label: 'ABOUT US', href: '#' },
];
type PropIcon = {
    icon: JSX.Element;
};
function IconFooter({ icon }: PropIcon) {
    return <i>{icon}</i>;
}

const iconos = [
    { icon: <FaTiktok /> },
    { icon: <ImFacebook2 /> },
    { icon: <RiInstagramFill /> },
    { icon: <FaYoutube /> },
];
export function Footer() {
    return (
        <footer className="footer">
            <div className="container">
                <img className="logo-footer" src={logoo} alt="logo de la web" />
                {/*Componenete de los link del navbar*/}
                <ul className="footer-list">
                    {navLinks.map((link, index) => (
                        <NavbarItem key={index} {...link} />
                    ))}
                </ul>
                {iconos.map((icon, index) => (
                    <IconFooter key={index} {...icon} />
                ))}
            </div>
            <div>
                <p>COPYRIGHT: 2025</p>
            </div>
        </footer>
    );
}
