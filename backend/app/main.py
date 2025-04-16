from sqlalchemy.sql import text
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.db.database import BASE, session_local, engine
from app.api.router.recetas import router as receta_router
from app.api.router.categorias import router as categoria_router
from app.api.router.ingredientes import router as ingredientes_router
from app.api.router.destacada import router as destacada_router
from app.api.router.suscriptores import router as suscriptores
from sqlalchemy.orm import sessionmaker
from app.db.models import Categorias, Ingredientes, RecetaCategoria, RecetaIngredientes, Recetas

app = FastAPI()
app.include_router(receta_router)
app.include_router(categoria_router)
app.include_router(ingredientes_router)
app.include_router(destacada_router)
app.include_router(suscriptores)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_local = sessionmaker(autocommit=False, bind=engine, autoflush=False)
db = session_local()


def insertar_recetas():
    nueva_receta = Recetas(
        titulo="Tortilla de Espinacas y Queso",
        descripcion="Tortilla de espinacas con queso, esponjosa y llena de sabor, perfecta para comenzar el día o terminarlo de manera saludable.",
        descripcion_original="""Una tortilla esponjosa y cargada de sabor, enriquecida con espinacas frescas y queso derretido.
Este plato es ideal tanto para un desayuno abundante como para una cena ligera, brindando un aporte extra de verduras y proteínas de forma deliciosa.""",
        pasos={
            "Preparar los ingredientes": [
                "Lava y pica finamente las espinacas.",
                "Ralla el queso (puedes usar mozzarella, cheddar suave o una mezcla)."
            ],
            "Preparar la mezcla": [
                "Bate los huevos junto con la leche en un tazón, añade sal y pimienta.",
                "Incorpora las espinacas picadas, el ajo (si lo usas) y el queso rallado a la mezcla."
            ],
            "Cocinar la tortilla": [
                "Calienta el aceite de oliva en la sartén a fuego medio.",
                "Vierte la mezcla en la sartén y cocina a fuego lento, permitiendo que se cuaje por abajo.",
                "Voltea cuidadosamente la tortilla para dorar el otro lado."
            ],
            "Servir": [
                "Una vez cocida y esponjosa, retira la tortilla del fuego.",
                "Sirve caliente y disfruta."
            ]
        },
        imagen="https://res.cloudinary.com/dj4ynkqqi/image/upload/v1744729077/06_tortilla_francesa_dmpz24.png",
        preparacion_previa={
            "Lavar espinacas": "Lava y pica finamente las espinacas.",
            "Rallar queso": "Ralla el queso en un recipiente aparte (puedes usar una mezcla de quesos)."
        },
        equipamiento=[
            "Sartén antiadherente",
            "Tazón para batir los huevos",
            "Espátula",
            "Tabla de cortar y cuchillo"
        ],
        valores_nutricionales={
            "calorias": {"cantidad": 180, "unidad": "kcal"},
            "proteinas": {"cantidad": 14, "unidad": "g"},
            "carbohidratos": {"cantidad": 3, "unidad": "g"},
            "grasas": {"cantidad": 12, "unidad": "g"},
            "fibra": {"cantidad": 1, "unidad": "g"}
        },
        tiempo_cocina="20-22 minutos",
        dificultad="Fácil",
        tags=["Desayuno", "Cena Ligera", "Tortilla", "Cocina Infantil"],
        porciones=3,
        tips=[
            "Si deseas una tortilla aún más esponjosa, separa las claras, bátelas a punto de nieve y agrégalas a la mezcla final.",
            "Deja que los niños participen ayudando a batir los huevos con supervisión."
        ]
    )

    # Categorías
    categorias_obj = []
    for nombre_categoria in ["all", "cena", "almuerzo"]:
        categoria_obj = db.query(Categorias).filter(
            Categorias.nombre == nombre_categoria).first()
        if not categoria_obj:
            categoria_obj = Categorias(nombre=nombre_categoria)
            db.add(categoria_obj)
            db.commit()
            db.refresh(categoria_obj)
        categorias_obj.append(categoria_obj)

    db.add(nueva_receta)

    nueva_receta.recetas_categorias.extend([
        RecetaCategoria(categoria=categoria) for categoria in categorias_obj
    ])

    # Ingredientes
    ingredientes = [
        {"nombre": "huevos", "cantidad": 4, "unidad": "unidad"},
        {"nombre": "espinacas frescas picadas", "cantidad": 1, "unidad": "taza"},
        {"nombre": "queso rallado", "cantidad": 0.5, "unidad": "taza"},
        {"nombre": "leche", "cantidad": 0.25, "unidad": "taza"},
        {"nombre": "ajo finamente picado", "cantidad": 1, "unidad": "diente"},
        {"nombre": "sal y pimienta", "cantidad": 1, "unidad": "al gusto"},
        {"nombre": "aceite de oliva", "cantidad": 1, "unidad": "cucharada"}
    ]

    for i_data in ingredientes:
        ingrediente = db.query(Ingredientes).filter(
            Ingredientes.nombre == i_data["nombre"]
        ).first()
        if not ingrediente:
            ingrediente = Ingredientes(nombre=i_data["nombre"])
            db.add(ingrediente)
            db.commit()
            db.refresh(ingrediente)

        nueva_receta.receta_ingredientes.append(
            RecetaIngredientes(
                ingrediente=ingrediente,
                cantidad=i_data["cantidad"],
                unidad=i_data["unidad"]
            )
        )

    # Guardar la receta

    try:
        db.commit()
        db.refresh(nueva_receta)
        print("Receta insertada correctamente.")
    except Exception as e:
        db.rollback()
        print(f"Error al insertar receta y sus relaciones: {e}")
        return None

    return nueva_receta


def eliminar_tablas():
    try:
        BASE.metadata.drop_all(bind=engine)
        print("Tablas eliminadas correctamente.")
    except Exception as e:
        print(f"Error al eliminar tablas: {e}")


def crear_tablas():
    try:
        BASE.metadata.create_all(bind=engine)
        print("Tablas creadas correctamente.")
    except Exception as e:
        print(f"Error al crear tablas: {e}")


if __name__ == "__main__":
    insertar_recetas()
    print("¡Base de datos inicializada correctamente!")

    db.close()
