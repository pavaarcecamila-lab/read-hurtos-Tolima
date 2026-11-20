"""
Paquete modular de procesamiento, modelos y analítica.
"""

try:
    from .hurto import Hurto
except ImportError:
    Hurto = None

try:
    from .recuperacion import Recuperacion
except ImportError:
    Recuperacion = None

try:
    from .parque_automotor import ParqueAutomotor
except ImportError:
    ParqueAutomotor = None

try:
    from .integracion import Integracion
except ImportError:
    Integracion = None

try:
    from .transformacion import Transformacion
except ImportError:
    Transformacion = None

try:
    from .eda import EDA
except ImportError:
    EDA = None

try:
    from .clasificacion import TorneoClasificacion
except ImportError:
    TorneoClasificacion = None

try:
    from .clustering import SegmentacionClustering
except ImportError:
    SegmentacionClustering = None

try:
    from .ui_templates import *
except ImportError:
    pass

__all__ = [
    "Hurto",
    "Recuperacion",
    "ParqueAutomotor",
    "Integracion",
    "Transformacion",
    "EDA",
    "TorneoClasificacion",
    "SegmentacionClustering"
]
