from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.db.database import session_local, engine
from app.db.crud import actualizar_receta_con_ingredientes, insertar_receta_con_ingredientes
from app.api.router.recetas import router as receta_router
from app.api.router.categorias import router as categoria_router
from app.api.router.ingredientes import router as ingredientes_router
from sqlalchemy.orm import sessionmaker

app = FastAPI()
app.include_router(receta_router)
app.include_router(categoria_router)
app.include_router(ingredientes_router)
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

# Llamar a la función para insertar datos
"""respuesta = insertar_receta_con_ingredientes(
    db=db,
    categoria_nombre="meriendas",
    titulo="Galletas sin gluten para bebés",
    descripcion="Esta es una receta muy práctica si tu bebé tiene intolerancia al gluten, pero la verdad es que estas galletas están muy ricas y le gustarán igualmente si lo tolera bien. ¡Anímate a prepararlas!",
    pasos="Saca la mantequilla de la nevera para que esté a temperatura ambiente y córtala en trocitos. Ponla en un bol grande y bátela con una cuchara o batidora hasta que esté en punto pomada (con textura de crema).",
    imagen="https://www.recetasparamibebe.com/wp-content/uploads/2025/01/Receta_arroz_calabacin-930x620.jpg",
    lista_ingredientes=[
        {"nombre": "harina de maíz", "cantidad": "165", "unidad": "gramos"},
        {"nombre": "harina de arroz integral", "cantidad": "165", "unidad": "gramos"},
        {"nombre": "mantequilla sin sal", "cantidad": "125", "unidad": "gramos"},
        {"nombre": "huevo", "cantidad": "1", "unidad": "unidad"},
        {"nombre": "leche", "cantidad": "7", "unidad": "ml"},
        {"nombre": "canela en polvo", "cantidad": "1", "unidad": "cucharadita"},
        {"nombre": "azúcar glass", "cantidad": "70", "unidad": "g"},

    ]
)

print(respuesta)
"""

"""
respuesta = actualizar_receta_con_ingredientes(
    db=db,
    receta_id=29,
    categoria_nombre="meriendas",
    titulo="Yogur con avena y mantequilla de cacahuete",
    descripcion="Este postre saludable tiene un sabor delicioso con cero azúcar, te aseguramos que tus hijos lo devorarán en segundos. Además es súper completo con el calcio y proteínas del yogurt, los hidratos de la avena y las grasas saludables y hierro del cacahuete.",
    pasos="Pon una sartén a fuego medio y echa las dos cucharadas de copos de avena. Remueve con una cuchara de madera durante unos 5 minutos hasta que veas que están un poco tostados. Lo notarás porque se oscurecen un poco y el olor es más intenso.",
    imagen="https://www.recetasparamibebe.com/wp-content/uploads/2025/01/Receta_yogur_avena_cacahuete-930x620.jpg",
    lista_ingredientes=[
        {"nombre": " yogurt natural sin azúcar", "cantidad": "1", "unidad": "unidad"},
        {"nombre": "mantequilla de cacahuete", "cantidad": "1", "unidad": "cucharada"},
        {"nombre": "avena", "cantidad": "2", "unidad": "cucharadas"},
        

    ]
)

print(f"Receta actualizada: {respuesta}")
"""
# Cerrar la sesión
db.close()


# TODO: Mejorar la documentación
