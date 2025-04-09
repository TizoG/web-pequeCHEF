from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.db.database import BASE, session_local, engine
from app.db.crud import actualizar_receta_con_ingredientes, insertar_receta
from app.api.router.recetas import router as receta_router
from app.api.router.categorias import router as categoria_router
from app.api.router.ingredientes import router as ingredientes_router
from app.api.router.suscriptores import router as suscriptores
from sqlalchemy.orm import sessionmaker


app = FastAPI()
app.include_router(receta_router)
app.include_router(categoria_router)
app.include_router(ingredientes_router)
app.include_router(suscriptores)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 Permite cualquier origen (cámbialo en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_local = sessionmaker(autocommit=False, bind=engine, autoflush=False)
# Crear sesión de base de datos
db = session_local()

app.mount("/static", StaticFiles(directory="static"), name="static")

# insertar recetas


def insertar_recetas():
    """
    Crea una receta apta para niños y la inserta en la base de datos.

    Campos requeridos:
    - Título, descripción, pasos, imagen, ingredientes, equipamiento, valores nutricionales.
    - Tags para clasificar, dificultad, tiempo de cocina, porciones y tips.

    Retorna:
    - Objeto receta insertado en la base de datos.
    """
    nueva_receta = insertar_receta(
        db=db,
        categoria_nombre=[
            "carnes",
            "comida",
        ],
        titulo="Pollo Mágico con Limón y Ajo",
        descripcion=(
            "Un delicioso y tierno pollo marinado en limón y ajo, cocinado a la perfección para sorprender y enamorar a los más pequeños con sabores frescos y naturales."
        ),
        descripcion_original=(
            """
            Imagine un suculento pollo impregnado de las vibrantes notas 
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
            """
        ),
        pasos={
            "Preparar la marinada": "En un bowl, mezcla el jugo de limón, el ajo picado, el aceite de oliva, el orégano, sal y pimienta.",
            "Marinar el pollo": "Coloca los trozos de pollo en la mezcla, asegúrate de que queden bien cubiertos. Deja reposar en el refrigerador durante al menos 30 minutos.",
            "Precalentar": "Enciende el horno y precaliéntalo a 200°C.",
            "Hornear": "Coloca el pollo en la fuente para horno y distribúyelos en una sola capa para que se doren de manera uniforme.",
            "Cocción": "Hornea durante 20-25 minutos o hasta que el pollo esté dorado y jugoso.",
            "Presentación": "Decora con rodajas de limón y hojas de perejil. Sirve acompañado de verduras al vapor o una ensalada fresca."
        },
        imagen="static/imagenes/01_pollo-al-limon.png",
        preparacion_previa={
            "Marinar el pollo": "Cortar el pollo en trocitos adecuados y marinarlo durante al menos 30 minutos en una mezcla de jugo de limón, ajo picado (en poca cantidad, adaptado al gusto infantil) y un toque de aceite de oliva.",
            "Precalentar el horno": "A 200°C (392°F)."
        },
        ingredientes=[
            {"nombre": "Pechuga de pollo (sin piel y en trozos pequeños)",
             "cantidad": 500, "unidad": "gramos"},
            {"nombre": "Jugo de limón", "cantidad": 1, "unidad": "unidad"},
            {"nombre": "Ajo", "cantidad": 2, "unidad": "dientes"},
            {"nombre": "Aceite de oliva virgen extra",
                "cantidad": 2, "unidad": "cucharadas"},
            {"nombre": "Sal y pimienta ", "cantidad": 1, "unidad": "al gusto"},
            {"nombre": "Oregano seco ", "cantidad": 1, "unidad": "cucharada"},
            {"nombre": "Limón ", "cantidad": 3, "unidad": "rodajas"},
            {"nombre": "Hoja de perejil ", "cantidad": 2, "unidad": "hojas"},
        ],
        equipamiento=[
            "Bowl", "tabla de cortar y cuchillo", "Fuente para horno", "Cuchara medidora", "Horno"
        ],
        valores_nutricionales={
            "calorias": {"cantidad": 220, "unidad": "kcal"},
            "proteinas": {"cantidad": 30, "unidad": "g"},
            "grasas": {"cantidad": 8, "unidad": "g"},
            "carbohidratos": {"cantidad": 5, "unidad": "g"},
            "fibra": {"cantidad": 1, "unidad": "g"}
        },
        tiempo_cocina={
            "Preparación": "10-15 minutos",
            "Horneado": "20-25 minutos",
            "Total": "35-40 minutos"
        },
        dificultad="Fácil",
        tags=["Pollo", "Limon", "Ajo"],
        porciones=4,
        tips=[
            "Acompaña con arroz integral o puré de papas para variar las comidas.",
            "Utiliza platos coloridos y presenta las rodajas de limón formando caritas o figuras sencillas que incentiven la creatividad."
        ]

    )
    try:
        db.add(nueva_receta)
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error al insertar receta: {e}")
        return None

    return nueva_receta


"""
Eliminamos las tablas de la base de datos
"""

"""
def eliminar_tablas():
    BASE.metadata.drop_all(bind=engine)

    eliminar_tablas()


def crear_tablas():
    BASE.metadata.create_all(bind=engine)

    crear_tablas()
"""
# Cerrar la sesión
db.close()

# TODO: Mejorar la documentación
