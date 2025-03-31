import './App.css';
import { ColeccionRecetas } from './components/coleccionRecetas/ColeccionRecetas';
import { Footer } from './components/footer/Footer';
import { Navbar } from './components/header/Navbar';
import { Hero } from './components/hero/Hero';
import { Newsletter } from './components/newsletter/Newsletter';
import { Recetas } from './components/recetas/Recetas';
import { Wrapper } from './components/seccionWrapper/Wrapper';

function App() {
    return (
        <>
            <Navbar />
            <Hero />
            <Wrapper />
            <Recetas />
            <ColeccionRecetas />
            <Newsletter />
            <Footer />
        </>
    );
}

export default App;
