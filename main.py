# o app está dentro do arquivo __init__.py por isso importa o app direto e não o arquivo
from comunidadeimpressionadora import app

if __name__ == '__main__':
    # colocando debug=True, todas as mudanças no código e automaticamente implementada no navegador
    app.run(debug=True)
