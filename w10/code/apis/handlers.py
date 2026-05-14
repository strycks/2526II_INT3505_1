from mongoengine.errors import DoesNotExist, ValidationError
from utils import wrap_with_metadata_error
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(api):
    
    @api.errorhandler(DoesNotExist)
    def handle_not_found(error = None):
        logger.warning(f"Resource not found: {str(error)}")
        return wrap_with_metadata_error(str(error)), 404

    @api.errorhandler(ValidationError)
    def handle_bad_request(error = None):
        logger.warning(f"Validation error: {str(error)}")
        return wrap_with_metadata_error(str(error)), 400