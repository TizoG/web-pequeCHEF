import { Hero } from "../components/hero/Hero";
import { Wrapper } from "../components/seccionWrapper/Wrapper";
import { Recetas } from "../components/recetas/Recetas";
import { ColeccionRecetas } from "../components/coleccionRecetas/ColeccionRecetas";

export function Home() {
  return (
    <>
      <Hero />
      <Wrapper />
      <Recetas />
      <ColeccionRecetas />
    </>
  );
}
