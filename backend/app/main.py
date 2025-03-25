from fastapi import FastAPI
from app.db.database import session_local, engine
from app.db.crud import insertar_receta_con_ingredientes
from app.api.router.recetas import router as receta_router
from app.api.router.categorias import router as categoria_router
from app.api.router.ingredientes import router as ingredientes_router
from sqlalchemy.orm import sessionmaker

app = FastAPI()
app.include_router(receta_router)
app.include_router(categoria_router)
app.include_router(ingredientes_router)


session_local = sessionmaker(autocommit=False, bind=engine, autoflush=False)
# Crear sesión de base de datos
db = session_local()

# Llamar a la función para insertar datos
"""respuesta = insertar_receta_con_ingredientes(
    db=db,
    categoria_nombre="Pures",
    titulo="Puré de Zanahorias y repollo",
    descripcion="Este es un puré muy sabroso, en casa siempre decimos que nos recuerda al sabor del caldo de cocido a pesar de que la receta no lleva nada de carne. El repollo es un alimento rico en fibra, vitamina B6 y folato que ayuda al desarrollo del sistema nervioso. La zanahoria suaviza su sabor con un toque dulce y además le da un color muy atractivo, porque ya sabemos que muchos peques comen primero con los ojos.",
    pasos="Paso 1: Pela las zanahorias y córtalas en rodajas.",
    imagen="https://www.recetasparamibebe.com/wp-content/uploads/2024/12/Receta_pure_zanahoria_repollo-930x620.jpg",
    lista_ingredientes=[
        {"nombre": "zanahorias", "cantidad": "3", "unidad": "unidad"},
        {"nombre": "repollo", "cantidad": "1/2", "unidad": "unidad"},
        {"nombre": "cebolla", "cantidad": "1/2", "unidad": "unidad"}
    ]
)

print(respuesta)
"""
# Cerrar la sesión
db.close()


# TODO: Mejorar la documentación
