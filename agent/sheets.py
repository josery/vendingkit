"""
VendingKit Google Sheets Integration
Sincroniza incidentes a Google Sheets automáticamente
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

try:
    from google.auth.transport.requests import Request
    from google.oauth2.service_account import Credentials
    from google.sheets.v4 import SheetsServiceBuilder
    from googleapiclient.discovery import build
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    logging.warning("Google Sheets libraries not available - install: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")


class GoogleSheetsManager:
    """Gesiona la sincronización a Google Sheets"""
    
    def __init__(self):
        """Inicializa el manager de Google Sheets"""
        self.sheets_id = os.getenv("GOOGLE_SHEETS_ID")
        self.email = os.getenv("GOOGLE_CALENDAR_EMAIL")
        self.service = None
        self.range_name = "Incidentes!A:L"
        
        if not GOOGLE_AVAILABLE:
            logging.warning("Google API client not available")
            return
            
        if not self.sheets_id:
            logging.warning("GOOGLE_SHEETS_ID not configured")
            return
        
        try:
            self._authenticate()
        except Exception as e:
            logging.error(f"Error initializing Google Sheets: {e}")
            self.service = None
    
    def _authenticate(self):
        """Autentica con Google Sheets API usando credenciales del servicio"""
        try:
            # Intenta usar credenciales de entorno
            # En producción, usa GOOGLE_APPLICATION_CREDENTIALS variable
            self.service = build('sheets', 'v4')
            logging.info("✓ Google Sheets API initialized")
        except Exception as e:
            logging.error(f"Error autenticando con Google Sheets: {e}")
            self.service = None
    
    def append_incident(self, data: Dict[str, Any]) -> bool:
        """Agrega un incidente a Google Sheets"""
        if not self.service or not self.sheets_id:
            logging.warning("Google Sheets service not configured")
            return False
        
        try:
            # Prepara los valores para la fila
            values = [
                [
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Fecha/Hora
                    data.get("phone_number", ""),                  # Teléfono
                    data.get("name", ""),                          # Nombre
                    data.get("location", ""),                      # Ubicación
                    data.get("company", ""),                       # Empresa
                    data.get("floor", ""),                         # Piso
                    data.get("extension", ""),                     # Extensión
                    data.get("celular", ""),                       # Celular
                    data.get("category", ""),                      # Categoría
                    data.get("description", ""),                   # Descripción
                    data.get("response", ""),                      # Respuesta
                    data.get("monto", ""),                         # Monto
                ]
            ]
            
            # Añade la fila a la hoja
            body = {"values": values}
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheets_id,
                range=self.range_name,
                valueInputOption="RAW",
                body=body
            ).execute()
            
            logging.info(f"✓ Incident synced to Google Sheets: {data.get('category')}")
            return True
            
        except Exception as e:
            logging.error(f"Error appending to Google Sheets: {e}")
            return False
    
    def get_sheet_headers(self) -> List[str]:
        """Obtiene los encabezados de la hoja"""
        if not self.service or not self.sheets_id:
            return []
        
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheets_id,
                range="Incidentes!A1:L1"
            ).execute()
            
            values = result.get("values", [])
            return values[0] if values else []
            
        except Exception as e:
            logging.error(f"Error getting sheet headers: {e}")
            return []


def init_sheets_manager() -> Optional[GoogleSheetsManager]:
    """Inicializa el manager de Google Sheets"""
    if not GOOGLE_AVAILABLE:
        return None
    
    try:
        manager = GoogleSheetsManager()
        if manager.service:
            return manager
        return None
    except Exception as e:
        logging.error(f"Failed to initialize Google Sheets manager: {e}")
        return None
