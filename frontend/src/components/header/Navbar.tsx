import './navbar.css';
import logoo from '../../assets/logoo.webp';

// Componente reutilizable para los enlaces del Navbar

type Props = {
    label: string;
    href: string;
};
function NavbarItem({ label, href }: Props) {
    return (
        <li className="navbar-list__li">
            <a href={href} className="navbar-list__link">
                {label}
            </a>
        </li>
    );
}

// Array con los elementos del Navbar
const navLinks = [
    { label: 'HOME', href: '#' },
    { label: 'RECIPES', href: '#' },
    { label: 'COOKING TIPS', href: '#' },
    { label: 'ABOUT US', href: '#' },
];

export function Navbar() {
    return (
        <nav className="navbar">
            {/* Logo */}
            <div>
                <img src={logoo} alt="logo de la web" className="logo" />
            </div>

            {/* Lista de navegacion */}
            <div className="navbar-list">
                <ul className="navbar-list__ul">
                    {navLinks.map((link, index) => (
                        <NavbarItem key={index} {...link} />
                    ))}
                </ul>
            </div>

            {/* Barra de Busqueda */}
            <div>
                <input type="text" className="input" />
            </div>
        </nav>
    );
}
// TODO: Implementar bien la imagen
// TODO: Implementar iconos
// TODO: Mejorar la documentación
// TODO: Mejorar la estructura
// TODO: Mejorar la estilización
// TODO: Mejorar la funcionalidad
