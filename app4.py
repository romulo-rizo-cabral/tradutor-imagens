import streamlit as st
from PIL import Image
import pytesseract
from googletrans import Translator
import os, cv2
import numpy as np

os.chdir(os.getcwd())

def define_local_tesseract():
    # Define o caminho do Tesseract no Windows
    try:
        pytesseract.pytesseract.tesseract_cmd = f'OCR\\tesseract.exe'
        # pytesseract.pytesseract.tesseract_cmd = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
    except:
        print("Caminho do Tesseract não encontrado")

def extrair_texto_da_imagem(caminho_imagem):
    # Carrega a imagem
    imagem = Image.open(caminho_imagem)

    imagem_cv = np.array(imagem)
    imagem_cv = cv2.cvtColor(imagem_cv, cv2.COLOR_RGB2BGR)
    
    # Extrai o texto da imagem
    texto = pytesseract.image_to_string(imagem)
    data = pytesseract.image_to_data(imagem, output_type='dict')

    # Desenhar retângulos ao redor do texto detectado
    boxes = len(data['level'])
    for i in range(boxes):
        (x, y, w, h, text) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i], data['text'][i])
        if text.strip():  # Verifica se o texto não está vazio
            # sub_img = imagem_cv[y:y+h, x:x+w]
            # blur = cv2.GaussianBlur(sub_img, (15, 15), 0)
            # imagem_cv[y:y+h, x:x+w] = blur
            imagem_cv = cv2.rectangle(imagem_cv, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Convertendo de volta para o formato PIL
    imagem_rec = Image.fromarray(cv2.cvtColor(imagem_cv, cv2.COLOR_BGR2RGB))
    
    return texto, imagem_rec


def obter_nome_idioma(idiomas, codigo_idioma):
    return idiomas.get(codigo_idioma, 'Idioma desconhecido') 

tradutor = Translator()
define_local_tesseract()
# Configuração da página
st.title('Tradutor de Imagem')

# Botões para selecionar o conteúdo
pagina = st.sidebar.radio("Escolha a página:", ['Página Inicial', 'Carregar Imagens', 'Tirar Foto'])

# Seleção do idioma de destino
idiomas_dict = {
    'af': 'Afrikaans', 'sq': 'Albanês', 'am': 'Amárico', 'ar': 'Árabe', 'hy': 'Armênio', 'az': 'Azerbaijano',
    'eu': 'Basco', 'be': 'Bielorrusso', 'bn': 'Bengali', 'bs': 'Bósnio', 'bg': 'Búlgaro', 'ca': 'Catalão',
    'ceb': 'Cebuano', 'ny': 'Chichewa', 'zh-cn': 'Chinês (Simplificado)', 'zh-tw': 'Chinês (Tradicional)',
    'co': 'Córsico', 'hr': 'Croata', 'cs': 'Tcheco', 'da': 'Dinamarquês', 'nl': 'Holandês', 'en': 'Inglês',
    'eo': 'Esperanto', 'et': 'Estoniano', 'tl': 'Filipino', 'fi': 'Finlandês', 'fr': 'Francês', 'fy': 'Frísio',
    'gl': 'Galego', 'ka': 'Georgiano', 'de': 'Alemão', 'el': 'Grego', 'gu': 'Gujarati', 'ht': 'Haitiano Creole',
    'ha': 'Hausa', 'haw': 'Havaiano', 'he': 'Hebraico', 'hi': 'Hindi', 'hmn': 'Hmong', 'hu': 'Húngaro',
    'is': 'Islandês', 'ig': 'Igbo', 'id': 'Indonésio', 'ga': 'Irlandês', 'it': 'Italiano', 'ja': 'Japonês',
    'jw': 'Javanês', 'kn': 'Kannada', 'kk': 'Cazaque', 'km': 'Khmer', 'rw': 'Kinyarwanda', 'ko': 'Coreano',
    'ku': 'Curdo (Kurmanji)', 'ky': 'Quirguiz', 'lo': 'Laosiano', 'la': 'Latim', 'lv': 'Letão', 'lt': 'Lituano',
    'lb': 'Luxemburguês', 'mk': 'Macedônio', 'mg': 'Malgaxe', 'ms': 'Malaio', 'ml': 'Malaiala', 'mt': 'Maltês',
    'mi': 'Maori', 'mr': 'Marathi', 'mn': 'Mongol', 'my': 'Myanmar (Burmês)', 'ne': 'Nepalês', 'no': 'Norueguês',
    'or': 'Oriya', 'ps': 'Pashto', 'fa': 'Persa', 'pl': 'Polonês', 'pt': 'Português', 'pa': 'Punjabi',
    'ro': 'Romeno', 'ru': 'Russo', 'sm': 'Samoano', 'gd': 'Gaélico Escocês', 'sr': 'Sérvio', 'st': 'Sesotho',
    'sn': 'Shona', 'sd': 'Sindi', 'si': 'Cingalês', 'sk': 'Eslovaco', 'sl': 'Esloveno', 'so': 'Somali',
    'es': 'Espanhol', 'su': 'Sundanês', 'sw': 'Swahili', 'sv': 'Sueco', 'tg': 'Tajique', 'ta': 'Tâmil',
    'tt': 'Tártaro', 'te': 'Telugu', 'th': 'Tailandês', 'tr': 'Turco', 'tk': 'Turcomeno', 'uk': 'Ucraniano',
    'ur': 'Urdu', 'ug': 'Uyghur', 'uz': 'Uzbeque', 'vi': 'Vietnamita', 'cy': 'Galês', 'xh': 'Xhosa',
    'yi': 'Iídiche', 'yo': 'Ioruba', 'zu': 'Zulu'
}
idiomas_nomes = list(idiomas_dict.values())
idioma_selecionado = st.sidebar.selectbox('Selecione o idioma de destino', idiomas_nomes, index=idiomas_nomes.index('Português'))
codigo_idioma_destino = list(idiomas_dict.keys())[list(idiomas_dict.values()).index(idioma_selecionado)]

if pagina == 'Carregar Imagens':
    # Upload das imagens
    imagens = st.file_uploader('Carregar Imagens', type=['jpg', 'png'], accept_multiple_files=True)

    # Se uma ou mais imagens forem carregadas
    if imagens is not None:
        for i, caminho_imagem in enumerate(imagens):
            # Exibir a imagem
            st.image(caminho_imagem, caption=f'Imagem Carregada {i+1}', use_column_width=True)
            # Extrair texto da imagem
            texto_extraido, imagem_rec = extrair_texto_da_imagem(caminho_imagem)
            st.image(imagem_rec, caption=f'Texto demarcado {i+1}', use_column_width=True)
            # st.write('Texto Extraído:', texto_extraido)
            try:
                # Traduzir texto
                traducao = tradutor.translate(texto_extraido, codigo_idioma_destino)
                # print(traducao.text)
                st.write('Idioma Detectado:', idiomas_dict[traducao.src])
                st.write('Texto Traduzido:\n', traducao.text)
            except:
                st.write('Idioma não Detectado.')

elif pagina == 'Tirar Foto':
    img_file_buffers = st.camera_input("Tire uma foto")

    if img_file_buffers is not None:
        # Extrair texto da imagem
        texto_extraido, imagem_rec = extrair_texto_da_imagem(img_file_buffers)
        st.image(imagem_rec, caption=f'Texto demarcado', use_column_width=True)
        # st.write('Texto Extraído:', texto_extraido)
        try:
            # Traduzir texto
            traducao = tradutor.translate(texto_extraido, codigo_idioma_destino)
            # print(traducao.text)
            st.write('Idioma Detectado:', idiomas_dict[traducao.src])
            st.write('Texto Traduzido:\n', traducao.text)
        except:
            st.write('Idioma não Detectado.')
else:
    st.write("""
### Bem-vindo ao Tradutor de Imagem!

#### Autor: 

Rômulo Rizo Cabral

#### Sobre o Projeto:

O Tradutor de Imagem é um software de aplicação prática das técnicas aprendidas em sala de aula, representando o trabalho final da disciplina de Instalação de Ambiente Computacional, conduzida pelo Professor Thiago Medeiros, na Universidade do Estado do Rio de Janeiro (UERJ).

#### Objetivo:

Este projeto tem como objetivo principal desenvolver uma ferramenta que simplifique a tradução de texto em imagens, proporcionando uma solução intuitiva e eficaz para os usuários. Além disso, busca-se explorar e compreender os aspectos práticos da computação em nuvem através da publicação deste serviço na AWS.

#### Detalhes Técnicos:

O Tradutor de Imagem utiliza técnicas avançadas de processamento de imagem e reconhecimento óptico de caracteres (OCR), implementadas através da biblioteca Python Tesseract. Após a extração do texto da imagem, o serviço emprega a API Google Translate para traduzir o conteúdo para o idioma desejado pelo usuário.

#### Como Funciona:

O Tradutor de Imagem oferece uma interface simples e intuitiva, permitindo aos usuários carregar imagens contendo texto ou capturar novas fotos através da câmera de seus dispositivos. 

##### Exemplo:

- fizemos o upload da imagem abaixo na aba carregar imagens:
""")

    st.image('texto2.jpg', caption=f'Imagem Carregada')
    texto_extraido, imagem_rec = extrair_texto_da_imagem('texto2.jpg')
    st.write( """
- Após o processamento, o texto é identificado e demarcado na imagem, como mostrado na figura abaixo. 
""" )
    st.image(imagem_rec, caption=f'Texto demarcado', use_column_width=True)
    # st.write('Texto Extraído:', texto_extraido)
    st.write( """
- Em seguida printada a saída com o idioma identificado no texto e sua tradução para o idioma selecionado, proporcionando uma experiência de tradução eficiente e acessível.
""" )
    st.write("##### Saída:")

    try:
        # Traduzir texto
        traducao = tradutor.translate(texto_extraido, codigo_idioma_destino)
        # print(traducao.text)
        st.write('Idioma Detectado:', idiomas_dict[traducao.src])
        st.write('Texto Traduzido:\n', traducao.text)
    except:
        st.write('Idioma não Detectado.')
