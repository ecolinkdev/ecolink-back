import requests
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def get_lat_long_from_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Obtém a latitude e longitude a partir de um endereço usando a API Nominatim.

    :param address: Endereço a ser geocodificado.
    :return: Tupla (latitude, longitude) ou None se falhar.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "MyApp (ecolink@example.com)"
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            latitude = float(data[0]["lat"])
            longitude = float(data[0]["lon"])
            return latitude, longitude
        else:
            logger.warning(f"Endereço '{address}' não retornou resultados.")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao buscar coordenadas para o endereço '{address}': {e}")
        return None