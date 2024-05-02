from cx_Freeze import setup, Executable
import os 

pasta_data = "./data"
pasta_scripts = "./scripts"
pasta_imagens = "./imagens_tela_inicial"



# Definindo as opções de build
build_exe_options = {
    "packages": ["os", "pygame", "sys"],  # Lista de pacotes que precisam ser incluídos
    "include_files": [pasta_data, pasta_scripts, pasta_imagens, "Screen.py", "game.py", "editor.py"]  # incluir a pasta de imagens
}

# Configuração do setup
setup(
    name="Clube da Luta",
    version="0.1",
    description="O Melhor jogo de Luta",
    options={"build_exe": build_exe_options},
    executables=[Executable("editor.py")]
)