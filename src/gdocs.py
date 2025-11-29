"""Google Docs API helpers for template management and document creation."""

from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import Tuple

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
    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES
    )
    drive = build('drive', 'v3', credentials=creds)
    docs = build('docs', 'v1', credentials=creds)
    return drive, docs


def get_template_text(drive_service, template_id: str) -> str:
    """Export a Google Docs template as plain text.
    
    Args:
        drive_service: Authenticated Drive service
        template_id: Google Docs file ID
        
    Returns:
        Document body as plain text string
    """
    resp = drive_service.files().export(
        fileId=template_id, mimeType='text/plain'
    ).execute()
    if isinstance(resp, bytes):
        return resp.decode('utf-8')
    return str(resp)


def create_doc(docs_service, title: str) -> str:
    """Create a new blank Google Doc.
    
    Args:
        docs_service: Authenticated Docs service
        title: Title for the new document
        
    Returns:
        Document ID of the created doc
    """
    created = docs_service.documents().create(body={'title': title}).execute()
    return created.get('documentId')


def insert_text(docs_service, document_id: str, text: str):
    """Insert text at the start of a Google Doc.
    
    Args:
        docs_service: Authenticated Docs service
        document_id: Document ID to insert into
        text: Text to insert
    """
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


def get_doc_url(doc_id: str) -> str:
    """Generate the Google Docs URL for a document.
    
    Args:
        doc_id: Document ID
        
    Returns:
        Full Google Docs edit URL
    """
    return f'https://docs.google.com/document/d/{doc_id}/edit'
