
from flask import Flask, render_template, request, jsonify

import truststore
truststore.inject_into_ssl()

from supabase import create_client
from datetime import datetime
import os   


app = Flask(__name__)


# =========================================
# SUPABASE
# =========================================

SUPABASE_URL = os.environ.get("SUPABASE_URL")

SUPABASE_KEY = os.environ.get("SUPABASE_KEY")


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================
# PÁGINA PRINCIPAL
# =========================================

@app.route("/")
def inicio():

    return render_template("index.html")


# =========================================
# GUARDAR ELECCIÓN
# =========================================

@app.route("/guardar-eleccion", methods=["POST"])
def guardar_eleccion():

    try:

        datos = request.get_json()

        nombre = datos.get(
            "nombre",
            "Gaby"
        )

        clima = datos.get(
            "clima",
            ""
        )

        plan = datos.get(
            "plan",
            ""
        )


        fecha = datetime.now().isoformat()


        # Guardar en Supabase

        respuesta = supabase.table(
            "elecciones"
        ).insert({

            "nombre": nombre,

            "clima": clima,

            "plan": plan,

            "fecha": fecha

        }).execute()


        return jsonify({

            "success": True

        })


    except Exception as error:

        print(
            "ERROR GUARDANDO ELECCIÓN:",
            error
        )


        return jsonify({

            "success": False,

            "error": str(error)

        }), 500


# =========================================
# RESULTADOS
# =========================================

@app.route("/resultado")
def resultado():

    try:

        respuesta = supabase.table(
            "elecciones"
        ).select(
            "*"
        ).order(
            "id",
            desc=True
        ).execute()


        elecciones = respuesta.data


        return render_template(
            "resultado.html",
            elecciones=elecciones
        )


    except Exception as error:

        print(
            "ERROR OBTENIENDO RESULTADOS:",
            error
        )


        return """

        <h1>
            No se pudieron cargar los resultados.
        </h1>

        <p>
            Revisa la configuración de Supabase.
        </p>

        """, 500


# =========================================
# SERVIDOR
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )