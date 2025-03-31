import "./navbar.css";
import logoo from "../../assets/logoo.png";
import { IoSearch } from "react-icons/io5";

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
  { label: "HOME", href: "/" },
  { label: "RECIPES", href: "/recetas" },
  { label: "COOKING TIPS", href: "/tiposcocina" },
  { label: "ABOUT US", href: "/aboutus" },
];

export function Navbar() {
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
            <NavbarItem key={index} {...link} className="navbar-list__link" />
          ))}
        </ul>
      </div>

      {/* Barra de Busqueda */}
      <div className="content-search">
        <input type="text" className="input" placeholder="Busca tu receta..." />
        <div className="content-icon">
          <IoSearch className="icon" />
        </div>
      </div>
    </nav>
  );
}

// TODO: Mejorar la documentación
// TODO: Mejorar la funcionalidad
//TODO: Crear enlaces a otras secciones
