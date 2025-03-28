import './App.css';
import { ColeccionRecetas } from './components/coleccionRecetas/ColeccionRecetas';
import { Navbar } from './components/header/Navbar';
import { Hero } from './components/hero/Hero';
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
        </>
    );
}

export default App;
