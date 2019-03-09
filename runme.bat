SET mypath=%~dp0
chcp 65001
pip install xlsxwriter
pip install excel2img
python FMCranksParserV2.py
pause
