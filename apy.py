from flask import Flask, request, jsonify
from google_play_scraper import search, app
import logging
import random

app_flask = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app_flask.route('/buscar_app', methods=['POST'])
def buscar_app():
    try:
        # Obtener datos de la solicitud
        data = request.json  # Espera un JSON con {"app_name": "WhatsApp", "category": "Action", "n_hits": 10}
        app_flask.logger.debug(f"Request data: {data}")

        if not isinstance(data, dict):
            return jsonify({"error": "El JSON debe ser un objeto"}), 400

        app_name = data.get("app_name", "")
        category = data.get("category", "")
        n_hits = data.get("n_hits", 10)  # Número de resultados a devolver, por defecto 10
        app_flask.logger.debug(f"App name: {app_name}, Category: {category}, Number of hits: {n_hits}")

        if app_name:
            # Buscar aplicaciones con el nombre proporcionado
            results = search(app_name, n_hits=100)
        elif category:
            # Buscar aplicaciones de la categoría proporcionada
            results = search(category, n_hits=100)
        else:
            # Devolver juegos aleatorios
            results = search("game", n_hits=100)

        # Barajar los resultados y seleccionar los primeros n_hits
        random.shuffle(results)
        results = results[:n_hits]

        apps = []
        for result in results:
            apps.append({
                "Nombre": result["title"],
                "Desarrollador": result["developer"],
                "Categoria": result["genre"],
                "Puntuación": result["score"],
                "Descargas": result["installs"],
                "Descripción": result["description"][:200],
                "Imagenes": [result["icon"]] + result["screenshots"],
            })
        return jsonify(apps)

    except Exception as e:
        # Registrar el error exacto
        app_flask.logger.error(f"Error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app_flask.run(host='0.0.0.0', port=5000, debug=True)
