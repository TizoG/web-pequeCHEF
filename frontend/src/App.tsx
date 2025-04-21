import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

import { Footer } from './components/footer/Footer';
import { Navbar } from './components/header/Navbar';
import { Home } from './pages/Home';
import { Newsletter } from './components/newsletter/Newsletter';
import { PageRecetas } from './pages/Recetas/PageRecetas';
import { PageTiposCocina } from './pages/PageTiposCocina/PageTiposCocina';
import { PageAbout } from './pages/PageAbout/PageAbout';
import { DetalleReceta } from './pages/DetalleReceta/DetalleReceta';
import { PaginaBusqueda } from './pages/PaginaBusqueda/PaginaBusqueda';
import { Desayunos } from './pages/PaginasWrapper/Desayunos';
import { Comidas } from './pages/PaginasWrapper/Comidas';
import { Meriendas } from './pages/PaginasWrapper/Meriendas';
import { Cenas } from './pages/PaginasWrapper/Cenas';
import { Postres } from './pages/PaginasWrapper/Postres';

function App() {
    return (
        <Router>
            <Navbar />
            <Routes>
                <Route path="/" element={<Home />}></Route>
                <Route path="/recetas" element={<PageRecetas />}></Route>
                <Route path="/recetas/:id" element={<DetalleReceta />}></Route>
                <Route
                    path="/tiposcocina"
                    element={<PageTiposCocina />}
                ></Route>
                <Route path="/aboutus" element={<PageAbout />}></Route>
                <Route path="/search" element={<PaginaBusqueda />}></Route>
                <Route path="/desayunos" element={<Desayunos />}></Route>
                <Route path="/comidas" element={<Comidas />}></Route>
                <Route path="/meriendas" element={<Meriendas />}></Route>
                <Route path="/cenas" element={<Cenas />}></Route>
                <Route path="/postres" element={<Postres />}></Route>
            </Routes>
            <Newsletter />
            <Footer />
        </Router>
    );
}

export default App;
