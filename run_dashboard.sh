#!/bin/bash
# Script para iniciar el Dashboard de Minería de Datos localmente
cd "$(dirname "$0")"

export PYTHONPATH="/Users/camilapava/Documents/OCTAVO SEMESTRE/MINERIA 3 CORTE/.local_python/lib/python3.11/site-packages:$PYTHONPATH"
export MPLCONFIGDIR="/tmp/mpl"

echo "================================================================="
echo "🚔 Iniciando Dashboard de Hurto Vehicular en Colombia (Tolima)..."
echo "Docente: Esteban Ernesto Morales Castro · UNIMINUTO"
echo "================================================================="
/opt/homebrew/bin/python3.11 -m streamlit run app.py
