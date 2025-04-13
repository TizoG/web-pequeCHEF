from sqlalchemy.sql import text
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db.database import BASE, session_local, engine
from db.crud import actualizar_receta_con_ingredientes, insertar_receta
from api.router.recetas import router as receta_router
from api.router.categorias import router as categoria_router
from api.router.ingredientes import router as ingredientes_router
from api.router.suscriptores import router as suscriptores
from sqlalchemy.orm import sessionmaker

from db.models import Categorias, Ingredientes, RecetaCategoria, RecetaIngredientes, Recetas


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
# Crea una receta apta para niños y la inserta en la base de datos.

# Campos requeridos:
#    - Título, descripción, pasos, imagen, ingredientes, equipamiento, valores nutricionales.
#   - Tags para clasificar, dificultad, tiempo de cocina, porciones y tips.

#  Retorna:
# - Objeto receta insertado en la base de datos.
"""
    nueva_receta = Recetas(

        titulo="Pasta  ",
        descripcion=(
            "Una pasta vibrante salpicada de verduras frescas y aromáticas, perfecta para pequeños paladares que buscan sabor y color en su plato."
        ),
        descripcion_original=(
            """ Imagina una explosión de colores en tu plato: cada bocado 
            de nuestra Pasta Colorida Mágica es una experiencia sensorial 
            que invita a soñar. Los tiernos pedazos de pasta se mezclan 
            con la frescura crujiente de zanahorias,
            pimientos y calabacín, mientras los tomates cherry aportan 
            un toque jugoso y dulce. Cada ingrediente cuenta una 
            historia, una aventura culinaria en la que los niños son 
            los protagonistas, descubriendo que comer sano puede ser 
            tan divertido como jugar en un jardín lleno de flores. 
            Esta receta no solo deleita el paladar, sino que transforma 
            cada comida en 
            una obra de arte, donde la creatividad y la nutrición 
            se unen para celebrar la magia de comer juntos.
"""
        ),
        pasos={
            "Cocer la pasta": "En una olla grande, hierve agua con sal y cocina la pasta según las instrucciones del paquete (normalmente 8-10 minutos). Escurre y reserva.",
            "Saltear las verduras": ["Calienta el aceite de oliva en una sartén. Agrega el ajo picado (si decides usarlo de forma muy suave) y cocina por 1 minuto.", "Añade la zanahoria, el pimiento, el calabacín y los tomates cherry. Saltea durante 5-7 minutos hasta que las verduras estén tiernas pero conservando su color y textura."],
            "Integrar la pasta": ["Incorpora la pasta cocida a la sartén con las verduras. Mezcla suavemente para que se integren los sabores.", "Añade sal y pimienta al gusto y retira la sartén del fuego."],
            "Finalizar y decorar": "Sirve la pasta en platos individuales, espolvorea con el queso rallado mientras aún está caliente para que se funda ligeramente y decora con hojas de albahaca fresca.",

        },
        imagen="static/imagenes/02_pasta.png",
        preparacion_previa={
            "Lavar y cortar": " Lava bien las verduras y córtalas en dados pequeños o en tiras finas para facilitar su integración en la pasta.",
            "Precalentar la olla": " Pon a hervir agua con una pizca de sal para la cocción de la pasta."
        },

        equipamiento=[
            "Olla grande para cocinar la pasta", "Sartén grande para saltear las verduras", "Tabla de cortar y cuchillos afilados", "Colador", "Cucharón y espátula"
        ],
        valores_nutricionales={
            "calorias": {"cantidad": 310, "unidad": "kcal"},
            "proteinas": {"cantidad": 12, "unidad": "g"},
            "grasas": {"cantidad": 8, "unidad": "g"},
            "carbohidratos": {"cantidad": 50, "unidad": "g"},
            "fibra": {"cantidad": 4, "unidad": "g"}
        },
        tiempo_cocina="25-30 minutos",
        dificultad="Fácil",
        tags=["Pasta"],
        porciones=4,
        tips=[
            " Puedes variar los colores con otras verduras como brócoli o espinacas.",
            "Si a tus pequeños les gusta la textura suave, puedes cocinar las verduras unos minutos más para que se ablanden."
        ],
    )
    # Insertar las categorías
    categorias_obj = []
    for nombre_categoria in ["all", "pastas", "comida", "verduras"]:
        categoria_obj = db.query(Categorias).filter(
            Categorias.nombre == nombre_categoria).first()
        if not categoria_obj:
            categoria_obj = Categorias(nombre=nombre_categoria)
            db.add(categoria_obj)
            db.commit()  # Commit para asegurarse de que la categoría se inserte
            db.refresh(categoria_obj)
        categorias_obj.append(categoria_obj)

    nueva_receta.categorias.extend([
        RecetaCategoria(receta_id=nueva_receta.id, categoria_id=categoria.id)
        for categoria in categorias_obj
    ])

    # Insertar la receta
    db.add(nueva_receta)
    ingredientes = [
        {"nombre": "Pasta(penne, fusilli o la que prefieras)",
         "cantidad": 250, "unidad": "gramos"},
        {"nombre": "Zanahoria", "cantidad": 1, "unidad": "unidad"},
        {"nombre": "Pimiento rojo", "cantidad": 1, "unidad": "unidad"},
        {"nombre": "Calabacín",
         "cantidad": 1, "unidad": "unidad"},
        {"nombre": "Tomates cherry ", "cantidad": 1, "unidad": "taza"},
        {"nombre": "Ajo ", "cantidad": 2, "unidad": "dientes"},
        {"nombre": "Aceite de oliva virgen extra ",
            "cantidad": 2, "unidad": "cucharadas"},
        {"nombre": "Queso ", "cantidad": 1/2, "unidad": "unidad"},
        {"nombre": "Sal y Pimienta ", "cantidad": 1, "unidad": "al gusto"},
        {"nombre": "Albahaca ", "cantidad": 1, "unidad": "hoja"},
    ]

    ingredientes_obj = []
    for ingrediente in ingredientes:
        ingrediente_obj = db.query(Ingredientes).filter(
            Ingredientes.nombre == ingrediente["nombre"]).first()
        if not ingrediente_obj:
            ingrediente_obj = Ingredientes(nombre=ingrediente["nombre"])
            db.add(ingrediente_obj)
            db.commit()  # Commit para insertar el ingrediente
            db.refresh(ingrediente_obj)
        ingredientes_obj.append(ingrediente_obj)

    # Añadir ingredientes a la receta utilizando la tabla intermedia
    for ingrediente in ingredientes_obj:
        nuevo_ingrediente = RecetaIngredientes(
            receta_id=nueva_receta.id,
            ingrediente_id=ingrediente.id,
            cantidad=ingrediente["cantidad"],
            unidad=ingrediente["unidad"]
        )
        db.add(nuevo_ingrediente)

    # Commit final
    try:
        db.commit()
        db.refresh(nueva_receta)
    except Exception as e:
        db.rollback()
        print(f"Error al insertar receta y sus relaciones: {e}")
        return None

    return nueva_receta


"""
Eliminamos las tablas de la base de datos
"""

# Función para eliminar tablas (con manejo de relaciones)


def eliminar_tablas():
    try:
        # Eliminar claves foráneas
        with engine.connect() as conn:
            conn.execute(text(
                "ALTER TABLE recetas_categorias DROP FOREIGN KEY recetas_categorias_ibfk_1"))
            conn.execute(text(
                "ALTER TABLE recetas_categorias DROP FOREIGN KEY recetas_categorias_ibfk_2"))

        # Eliminar todas las tablas
        BASE.metadata.drop_all(bind=engine)
        print("Tablas eliminadas correctamente.")
    except Exception as e:
        print(f"Error al eliminar tablas: {e}")


# Función para crear tablas
def crear_tablas():
    try:
        BASE.metadata.create_all(bind=engine)
        print("Tablas creadas correctamente.")
    except Exception as e:
        print(f"Error al crear tablas: {e}")


# Inicialización (eliminar y crear tablas al iniciar)
if __name__ == "__main__":
    insertar_recetas()

    print("¡Base de datos inicializada correctamente!")
# Cerrar la sesión
db.close()

# TODO: Mejorar la documentación
