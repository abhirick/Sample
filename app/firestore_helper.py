from google.cloud import firestore
from config import get_config
import logging
import uuid
import time
from .logging_config import setup_logging
from google.api_core.exceptions import GoogleAPIError

# Initialize Firestore client
db = firestore.Client()
config = get_config()
COLLECTION_NAME = config.get("COLLECTION")
# Run setup_logging to configure logging
setup_logging()
# Create a logger
logger = logging.getLogger(__name__)


def collection_exists():
    """Check if a collection exists.
    Returns:
        bool: True if the collection exists, False otherwise.
    """
    logger.info(f"Checking if Firstore has a collection named : {COLLECTION_NAME}")
    try:
        docs = db.collection(COLLECTION_NAME).limit(1).stream()
        exists = any(docs)
        logger.info(f"Firestore collection '{COLLECTION_NAME}' exists: {exists}")
        return exists
    except Exception as e:
        logger.error(f"Error checking collection existence: {e}")
        return False


def add_document_to_collection(document):
    """Add a document to a collection, creating the collection if it doesn't exist.
    Args:
        document (dict): A dictionary representing the document.

    Returns:
        dict: The added document if successful, None otherwise.
    """
    try:
        if not collection_exists():
            logger.info(
                f"Collection {COLLECTION_NAME} does not exist. Creating collection."
            )

        document_id = str(int(time.time() * 1000))

        def transaction_operation(transaction):
            doc_ref = db.collection(COLLECTION_NAME).document(document_id)
            transaction.set(doc_ref, document)

        # Use Firestore transaction
        transaction = db.transaction()
        transaction_operation(transaction)
        transaction.commit()

        # Retrieve the document after committing the transaction
        doc_ref = db.collection(COLLECTION_NAME).document(document_id)
        added_doc = doc_ref.get()
        logger.info(f"Document ID:: {doc_ref.id}")
        added_document = added_doc.to_dict()

        logger.info(
            f"Document {document_id} added to collection {COLLECTION_NAME}: {added_document}"
        )
        return doc_ref.id
    except GoogleAPIError as e:
        logger.error(f"Error adding document to collection: {e}")
        return None


def retrieve_document_from_collection(user_id):
    """Retrieve a document from a collection.
    Args:
        user_id (str): The ID of the user to retrieve.
    Returns:
        dict: The user document if found, otherwise None.
    """
    try:
        logger.info(
            f"Retrieving document with ID {user_id} from collection {COLLECTION_NAME}"
        )
        doc_ref = db.collection(COLLECTION_NAME).document(user_id)

        doc = doc_ref.get()

        if doc.exists:
            user_data = doc.to_dict()
            logger.info(f"User data retrieved: {user_data}")
            return user_data
        else:
            logger.warning(f"No such user with ID {user_id}")
            return None
    except GoogleAPIError as e:
        logger.error(f"Error retrieving document: {e}")
        return None

