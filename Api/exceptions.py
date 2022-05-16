import traceback

from flask import Flask, jsonify
from .logger import logger


class ValidationException(Exception):
    pass

def register_error_handler(app: Flask):

    @app.errorhandler(Exception)
    def handle_exception_error(e):
        logger.error(str(e))
        logger.error(traceback.print_exc())
        return jsonify({'msg': 'Predictor Service Internal Server Error.'}), 500

    @app.errorhandler(405)
    def handle_405_error(e):
        logger.error(str(e))
        return jsonify({'msg': 'Method not allowed'}), 405

    @app.errorhandler(403)
    def handle_403_error(e):
        logger.error(str(e))
        return jsonify({'msg': 'Forbidden error'}), 403

    @app.errorhandler(404)
    def handle_404_error(e):
        logger.error(str(e))
        return jsonify({'msg': 'Not Found error'}), 404

    @app.errorhandler(ValidationException)
    def handle_redis_exception(e):
        logger.error(str(e))
        return jsonify({'msg': f"Validation error: {str(e)}"}), 400
