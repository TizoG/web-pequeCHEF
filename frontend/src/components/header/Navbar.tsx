import './navbar.css';
import logoo from '../../assets/logoo.png';
import { IoSearch } from 'react-icons/io5';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

// Componente reutilizable para los enlaces del Navbar

type Props = {
    label: string;
    href: string;
    className: string;
};
export function NavbarItem({ label, href, className }: Props) {
    return (
        <li className="navbar-list__li">
            <a href={href} className={className}>
                {label}
            </a>
        </li>
    );
}

// Array con los elementos del Navbar
const navLinks = [
    { label: 'HOME', href: '/' },
    { label: 'RECIPES', href: '/recetas' },
    { label: 'COOKING TIPS', href: '/tiposcocina' },
    { label: 'ABOUT US', href: '/aboutus' },
];
export function Navbar() {
    const [search, setSearch] = useState('');
    const navigate = useNavigate();
    const [resultados, setResultados] = useState([]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSearch(e.target.value);
    };
    const handleSearch = async () => {
        if (!search.trim()) {
            alert('por favor, escribe algo para buscar.');
        }
        navigate(`/search?query=${encodeURIComponent(search)}`);
    };
    return (
        <nav className="navbar">
            {/* Logo */}
            <div className="container-logo">
                <a href="/" className="navbar-logo__link">
                    <img src={logoo} alt="logo de la web" className="logo" />
                    <p className="text-logo">
                        peque<span className="text-logo__span">CHEF</span>
                    </p>
                </a>
            </div>

            {/* Lista de navegacion */}
            <div className="navbar-list">
                <ul className="navbar-list__ul">
                    {navLinks.map((link, index) => (
                        <NavbarItem
                            key={index}
                            {...link}
                            className="navbar-list__link"
                        />
                    ))}
                </ul>
            </div>

            {/* Barra de Busqueda */}
            <div className="content-search">
                <input
                    type="text"
                    className="input"
                    placeholder="Busca tu receta..."
                    value={search}
                    onChange={handleChange}
                    onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                />
                <div className="content-icon" onClick={handleSearch}>
                    <IoSearch className="icon" />
                </div>
            </div>
        </nav>
    );
}

// TODO: Mejorar la documentación
// TODO: Mejorar la funcionalidad
//TODO: Crear enlaces a otras secciones
