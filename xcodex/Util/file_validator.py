import os
import h5py
from typing import Union, Tuple


def validate_nc4_file(file_path: str) -> Tuple[bool, str]:
    """
    Verifica se um arquivo NC4 é válido.

    Args:
        file_path: Caminho do arquivo NC4

    Returns:
        Tuple[bool, str]: (status, mensagem)
            - status: True se válido, False se inválido
            - mensagem: Descrição do resultado da validação
    """
    if not os.path.exists(file_path):
        return False, f"Arquivo não encontrado: {file_path}"

    if os.path.getsize(file_path) < 1024:
        return False, f"Arquivo vazio ou muito pequeno: {file_path}"

    try:
        with h5py.File(file_path, 'r') as f:
            # Verifica estrutura básica
            required_vars = ['XCO2', 'lat', 'lon', 'time']
            missing_vars = [var for var in required_vars if var not in f]

            if missing_vars:
                return False, f"Variáveis ausentes: {', '.join(missing_vars)}"

            # Verifica se há dados
            if any(f[var].size == 0 for var in required_vars):
                return False, "Uma ou mais variáveis estão vazias"

        return True, "Arquivo válido"

    except Exception as e:
        return False, f"Erro ao verificar arquivo: {str(e)}"
