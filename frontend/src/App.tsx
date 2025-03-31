import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";

import { Footer } from "./components/footer/Footer";
import { Navbar } from "./components/header/Navbar";
import { Home } from "./pages/Home";
import { Newsletter } from "./components/newsletter/Newsletter";
import { PageRecetas } from "./pages/Recetas/PageRecetas";
import { PageTiposCocina } from "./pages/PageTiposCocina/PageTiposCocina";
import { PageAbout } from "./pages/PageAbout/PageAbout";
import { PageNoticias } from "./pages/Noticias/PageNoticias";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />}></Route>
        <Route path="/recetas" element={<PageRecetas />}></Route>
        <Route path="/tiposcocina" element={<PageTiposCocina />}></Route>
        <Route path="/aboutus" element={<PageAbout />}></Route>
        <Route path="/noticias" element={<PageNoticias />}></Route>
      </Routes>
      <Newsletter />
      <Footer />
    </Router>
  );
}

export default App;
