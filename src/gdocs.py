"""Google Docs API helpers for template management and document creation."""

import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import Tuple

logger = logging.getLogger('character_creation')

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents'
]


def create_services(service_account_file: str):
    """Create authenticated Drive and Docs service clients.
    
    Args:
        service_account_file: Path to service account JSON file
        
    Returns:
        Tuple of (drive_service, docs_service)
    """
    logger.debug(f"Creating Google services from: {service_account_file}")
    try:
        creds = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES
        )
        logger.debug("Service account credentials loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load service account credentials: {e}")
        raise
    
    drive = build('drive', 'v3', credentials=creds)
    docs = build('docs', 'v1', credentials=creds)
    logger.info("Google Drive and Docs services created successfully")
    return drive, docs


def get_template_text(drive_service, template_id: str) -> str:
    """Export a Google Docs template as plain text.
    
    Args:
        drive_service: Authenticated Drive service
        template_id: Google Docs file ID
        
    Returns:
        Document body as plain text string
    """
    logger.debug(f"Fetching template text from doc: {template_id}")
    try:
        resp = drive_service.files().export(
            fileId=template_id, mimeType='text/plain'
        ).execute()
        if isinstance(resp, bytes):
            text = resp.decode('utf-8')
        else:
            text = str(resp)
        logger.info(f"Template text fetched successfully ({len(text)} characters)")
        return text
    except Exception as e:
        logger.error(f"Failed to fetch template text: {e}")
        raise


def create_doc(docs_service, title: str) -> str:
    """Create a new blank Google Doc.
    
    Args:
        docs_service: Authenticated Docs service
        title: Title for the new document
        
    Returns:
        Document ID of the created doc
    """
    logger.debug(f"Creating new Google Doc with title: {title}")
    try:
        created = docs_service.documents().create(body={'title': title}).execute()
        doc_id = created.get('documentId')
        logger.info(f"Google Doc created successfully. ID: {doc_id}")
        return doc_id
    except Exception as e:
        logger.error(f"Failed to create Google Doc: {e}")
        raise


def insert_text(docs_service, document_id: str, text: str):
    """Insert text at the start of a Google Doc.
    
    Args:
        docs_service: Authenticated Docs service
        document_id: Document ID to insert into
        text: Text to insert
    """
    logger.debug(f"Inserting text into document {document_id} ({len(text)} characters)")
    try:
        requests = [
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': text
                }
            }
        ]
        docs_service.documents().batchUpdate(
            documentId=document_id, body={'requests': requests}
        ).execute()
        logger.info(f"Text inserted successfully into document: {document_id}")
    except Exception as e:
        logger.error(f"Failed to insert text into document: {e}")
        raise


def get_doc_url(doc_id: str) -> str:
    """Generate the Google Docs URL for a document.
    
    Args:
        doc_id: Document ID
        
    Returns:
        Full Google Docs edit URL
    """
    return f'https://docs.google.com/document/d/{doc_id}/edit'
