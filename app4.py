import streamlit as st
from PIL import Image
import pytesseract
from googletrans import Translator
import os

def define_local_tesseract():
    # Define o caminho do Tesseract no Windows
    try:
        print(os.getcwd())
        pytesseract.pytesseract.tesseract_cmd = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'
    except:
        print("Caminho do Tesseract não encontrado")

def extrair_texto_da_imagem(caminho_imagem):
    # Carrega a imagem
    imagem = Image.open(caminho_imagem)
    # Extrai o texto da imagem
    texto = pytesseract.image_to_string(imagem)
    return texto

def obter_nome_idioma(idiomas, codigo_idioma):
    return idiomas.get(codigo_idioma, 'Idioma desconhecido') 

define_local_tesseract()
tradutor = Translator()
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
        for i, imagem in enumerate(imagens):
            # Exibir a imagem
            st.image(imagem, caption=f'Imagem Carregada {i+1}', use_column_width=True)
            # Extrair texto da imagem
            texto_extraido = extrair_texto_da_imagem(imagem)
            # st.write('Texto Extraído:', texto_extraido)
            try:
                # Traduzir texto
                traducao = tradutor.translate(texto_extraido, codigo_idioma_destino)
                st.write('Idioma Detectado:', idiomas_dict[traducao.src])
                st.write('Texto Traduzido:\n', traducao.text)
            except:
                st.write('Idioma não Detectado.')

elif pagina == 'Tirar Foto':
    img_file_buffers = st.camera_input("Tire uma foto")

    if img_file_buffers is not None:
        # Extrair texto da imagem
        texto_extraido = extrair_texto_da_imagem(img_file_buffers)
        # st.write('Texto Extraído:', texto_extraido)
        try:
            # Traduzir texto
            traducao = tradutor.translate(texto_extraido, codigo_idioma_destino)
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

O Tradutor de Imagem é fruto da aplicação prática das técnicas aprendidas em sala de aula, representando um marco na finalização da disciplina de Instalação de Ambiente Computacional, conduzida pelo Professor Thiago Medeiros, na Universidade do Estado do Rio de Janeiro (UERJ). Este projeto não apenas demonstra a habilidade dos estudantes em assimilar e aplicar conhecimentos, mas também marca a criação de um micro serviço em nuvem como resultado final.

#### Objetivo:

Este projeto tem como objetivo principal desenvolver uma ferramenta que simplifique a tradução de texto em imagens, proporcionando uma solução intuitiva e eficaz para os usuários. Além disso, busca-se explorar e compreender os aspectos práticos da computação em nuvem através da publicação deste serviço na AWS.

#### Detalhes Técnicos:

O Tradutor de Imagem utiliza técnicas avançadas de processamento de imagem e reconhecimento óptico de caracteres (OCR), implementadas através da biblioteca Python Tesseract. Após a extração do texto da imagem, o serviço emprega a API Google Translate para traduzir o conteúdo para o idioma desejado pelo usuário.

#### Como Funciona:

O Tradutor de Imagem oferece uma interface simples e intuitiva, permitindo aos usuários carregar imagens contendo texto ou capturar novas fotos através da câmera de seus dispositivos. Após o processamento, o texto é automaticamente traduzido para o idioma selecionado, proporcionando uma experiência de tradução eficiente e acessível.

##### Exemplo:

- fizemos o upload da imagem abaixo na aba carregar imagens:
""")

    st.image('texto2.jpg', caption=f'Imagem Carregada')
    texto_extraido = extrair_texto_da_imagem('texto2.jpg')

    st.write("##### Saída:")

    try:
        # Traduzir texto
        traducao = tradutor.translate(texto_extraido, codigo_idioma_destino)
        st.write('Idioma Detectado:', idiomas_dict[traducao.src])
        st.write('Texto Traduzido:\n', traducao.text)
    except:
        st.write('Idioma não Detectado.')