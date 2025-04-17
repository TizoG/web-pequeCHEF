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
        titulo="Tacos Suaves de Pescado con Guacamole",
        descripcion="Tacos ligeros y sabrosos con filetes de pescado, guacamole casero y verduras frescas, ideales para una cena rápida y saludable.",
        descripcion_original="""Una opción fresca y deliciosa para cualquier día de la semana. 
Estos tacos suaves de pescado combinan sabores vibrantes con una preparación sencilla. 
El guacamole casero y las verduras crujientes aportan textura y color, creando una comida nutritiva que encantará a grandes y pequeños.""",
        pasos={
            "Preparar los ingredientes": [
                "Sazona los filetes de pescado con pimentón, sal y pimienta.",
                "Lava y ralla las verduras.",
                "Prepara el guacamole machacando el aguacate con lima, sal y pimienta."
            ],
            "Cocinar el pescado": [
                "Cocina el pescado en una sartén con un poco de aceite hasta que esté dorado y cocido.",
                "Desmenúzalo en trozos medianos para los tacos."
            ],
            "Montar los tacos": [
                "Calienta ligeramente las tortillas.",
                "Agrega el pescado, el guacamole, el repollo rallado y la zanahoria.",
                "Puedes añadir un poco más de lima por encima antes de servir."
            ]
        },
        # reemplaza por la URL real que uses
        imagen="https://res.cloudinary.com/dj4ynkqqi/image/upload/v1744885426/08_tacos_pescado_qwerty.png",
        preparacion_previa={
            "Sazonar y cocinar pescado": "Sazona con especias y cocina hasta dorar.",
            "Preparar guacamole": "Machaca el aguacate con lima, sal y pimienta.",
            "Rallar verduras": "Lava y ralla la zanahoria y repollo."
        },
        equipamiento=[
            "Sartén",
            "Espátula",
            "Tabla de cortar y cuchillo",
            "Rallador"
        ],
        valores_nutricionales={
            "calorias": {"cantidad": 320, "unidad": "kcal"},
            "proteinas": {"cantidad": 22, "unidad": "g"},
            "carbohidratos": {"cantidad": 26, "unidad": "g"},
            "grasas": {"cantidad": 15, "unidad": "g"},
            "fibra": {"cantidad": 5, "unidad": "g"}
        },
        tiempo_cocina="20 minutos",
        dificultad="Fácil",
        tags=["Tacos", "Pescado", "Guacamole",
              "Cocina para Niños", "Cena Ligera"],
        porciones=4,
        tips=[
            "Puedes sustituir el pescado por tofu crujiente para una versión vegana.",
            "Agrega unas gotas de salsa picante suave si los niños disfrutan sabores más atrevidos."
        ]
    )

    # Categorías
    categorias_obj = []
    for nombre_categoria in ["all", "cena", "tacos", "pescado", "guacamole", "cocina para niños"]:
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
        {"nombre": "filetes de pescado blanco", "cantidad": 2, "unidad": "unidad"},
        {"nombre": "pimentón dulce", "cantidad": 1, "unidad": "cucharadita"},
        {"nombre": "sal y pimienta", "cantidad": 1, "unidad": "al gusto"},
        {"nombre": "aceite de oliva", "cantidad": 1, "unidad": "cucharada"},
        {"nombre": "repollo morado rallado", "cantidad": 0.5, "unidad": "taza"},
        {"nombre": "zanahoria rallada", "cantidad": 1, "unidad": "unidad"},
        {"nombre": "aguacate", "cantidad": 1, "unidad": "unidad"},
        {"nombre": "lima", "cantidad": 0.5, "unidad": "unidad"},
        {"nombre": "tortillas pequeñas", "cantidad": 4, "unidad": "unidad"}
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
