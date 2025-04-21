import { NavbarItem } from '../header/Navbar';

import './footer.css';

const navLinks = [
    { label: 'HOME', href: '/' },
    { label: 'RECIPES', href: '/recetas' },
    { label: 'COOKING TIPS', href: 'tiposcocina' },
    { label: 'ABOUT US', href: '/aboutus' },
];

{
    /*
    import { FaTiktok } from 'react-icons/fa';
import { ImFacebook2 } from 'react-icons/im';
import { RiInstagramFill } from 'react-icons/ri';
import { FaYoutube } from 'react-icons/fa';
    import { JSX, useState } from 'react';
    type PropIcon = {
    icon: JSX.Element;
};
    function IconFooter({ icon }: PropIcon) {
        return <i>{icon}</i>;
    }
    
    const iconos = [
        { icon: <FaTiktok className="icon-footer" /> },
        { icon: <ImFacebook2 className="icon-footer" /> },
        { icon: <RiInstagramFill className="icon-footer" /> },
        { icon: <FaYoutube className="icon-footer" /> },
    ];
    
    */
}

export function Footer() {
    return (
        <footer className="footer">
            <div className="container__footer">
                {/*Componenete de los link del navbar*/}
                {/*<img
                    className="logo-footer"
                    src={footerlogo}
                    alt="logo de la web"
                />*/}
                <ul className="footer-list">
                    {navLinks.map((link, index) => (
                        <NavbarItem
                            key={index}
                            {...link}
                            className="footer-list__link"
                        />
                    ))}
                </ul>
                {/*
                    
                <div className="footer-list__container__icons">
                    {iconos.map((icon, index) => (
                        <IconFooter key={index} {...icon} />
                    ))}
                </div>
                    */}
            </div>
            <div className="footer-copyright">
                <p className="copyright">
                    Recetas hechas con amor para tus peques 2025
                </p>
            </div>
        </footer>
    );
}
