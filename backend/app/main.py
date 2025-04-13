from sqlalchemy.sql import text
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.db.database import BASE, session_local, engine
from app.api.router.recetas import router as receta_router
from app.api.router.categorias import router as categoria_router
from app.api.router.ingredientes import router as ingredientes_router
from app.api.router.suscriptores import router as suscriptores
from sqlalchemy.orm import sessionmaker
from app.db.models import Categorias, Ingredientes, RecetaCategoria, RecetaIngredientes, Recetas

app = FastAPI()
app.include_router(receta_router)
app.include_router(categoria_router)
app.include_router(ingredientes_router)
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
        titulo="Pollo Mágico con Limón y Ajo",
        descripcion="Un delicioso y tierno pollo marinado en limón y ajo, cocinado a la perfección para sorprender y enamorar a los más pequeños con sabores frescos y naturales.",
        descripcion_original="""  Imagine un suculento pollo impregnado de las vibrantes notas
 de limón y el aromático susurro del ajo. Es una
 sinfonía de sabores pensada para encantar el paladar infantil,
 donde cada trocito cuenta una historia de creatividad y cariño.
 Mientras el horno se calienta y la cocina se inunda de un
 delicioso aroma cítrico, el ambiente se transforma en un
 escenario de pequeñas grandes aventuras. Esta receta, además
 de nutritiva, es una obra de arte culinaria que invita a los
 niños a explorar, a jugar y a enamorarse de la cocina. Con cada
 mordisco, descubren que preparar comida saludable puede ser una
 aventura tan divertida como sabrosa, dejando una huella mágica
 en cada sonrisa.
 
 """,
        pasos={
            "Preparar la marinada": "En un bowl, mezcla el jugo de limón, el ajo picado, el aceite de oliva, el orégano, sal y pimienta.",
            "Marinar el pollo": "Coloca los trozos de pollo en la mezcla, asegúrate de que queden bien cubiertos. Deja reposar en el refrigerador durante al menos 30 minutos.",
            "Precalentar": "Enciende el horno y precaliéntalo a 200°C.",
            "Hornear": "Coloca el pollo en la fuente para horno y distribúyelos en una sola capa para que se doren de manera uniforme.",
            "Cocción": "Hornea durante 20-25 minutos o hasta que el pollo esté dorado y jugoso.",
            "Presentación": "Decora con rodajas de limón y hojas de perejil. Sirve acompañado de verduras al vapor o una ensalada fresca.",
        },
        imagen="https://res.cloudinary.com/dj4ynkqqi/image/upload/v1744472809/02_pollo-al-limon_itormt.png",
        preparacion_previa={"Marinar el pollo": "Cortar el pollo en trocitos adecuados y marinarlo durante al menos 30 minutos en una mezcla de jugo de limón, ajo picado (en poca cantidad, adaptado al gusto infantil) y un toque de aceite de oliva.",
                            "Precalentar el horno": "A 200°C (392°F)."
                            },
        equipamiento=[
            "Bowl", "tabla de cortar y cuchillo", "Fuente para horno", "Cuchara medidora", "Horno"
        ],
        valores_nutricionales={
            "calorias": {"cantidad": 220, "unidad": "kcal"},
            "proteinas": {"cantidad": 30, "unidad": "g"},
            "carbohidratos": {"cantidad": 5, "unidad": "g"},
            "grasas": {"cantidad": 8, "unidad": "g"},
            "fibra": {"cantidad": 1, "unidad": "g"}
        },
        tiempo_cocina="35-40 minutos",
        dificultad="Fácil",
        tags=["Pollo", "Limon", "Ajo"],
        porciones=4,
        tips=[
            "Acompaña con arroz integral o puré de papas para variar las comidas.",
            "Utiliza platos coloridos y presenta las rodajas de limón formando caritas o figuras sencillas que incentiven la creatividad."
        ],
    )

    # Categorías
    categorias_obj = []
    for nombre_categoria in ["all", "carnes", "comida", "pollo"]:
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
        {"nombre": "pechuga de pollo (sin piel y en trozos pequeños)",
         "cantidad": 500, "unidad": "gramos"},
        {"nombre": " jugo de limón", "cantidad": 1, "unidad": "unidad"},
        {"nombre": "Ajo", "cantidad": 2, "unidad": "dientes"},
        {"nombre": "Aceite de oliva virgen extra",
            "cantidad": 2, "unidad": "cucharadas"},
        {"nombre": "Sal y Pimienta", "cantidad": 1, "unidad": "al gusto"},
        {"nombre": "Orégano seco", "cantidad": 1, "unidad": "cucharada"},
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
