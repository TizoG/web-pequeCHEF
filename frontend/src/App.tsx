import './App.css';
import { Navbar } from './components/header/Navbar';
import { Hero } from './components/hero/Hero';
import { Wrapper } from './components/seccionWrapper/Wrapper';

function App() {
    return (
        <>
            <Navbar />
            <Hero />
            <Wrapper />
        </>
    );
}

export default App;
