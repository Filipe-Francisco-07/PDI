import numpy as np
import matplotlib.pyplot as plt
from skimage import io

def carregar_imagem(caminho):
    imagem = io.imread(caminho, as_gray=True)
    return (imagem * 255).astype(np.uint8)

def salvar_imagem(caminho, imagem):
    io.imsave(caminho, imagem.astype(np.uint8))

def gerar_planos_bits(imagem):
    planos_bits = [(imagem >> i) & 1 for i in range(8)]
    return planos_bits

def gerar_imagens_binarias(planos_bits):
    return [plano * 255 for plano in planos_bits]

def gerar_imagens_intensidades(planos_bits):
    return [plano * (2 ** i) for i, plano in enumerate(planos_bits)]

def gerar_3_bits_mais_significativos(planos_bits):
    imagem_3_bits = planos_bits[7] * 128 + planos_bits[6] * 64 + planos_bits[5] * 32
    return imagem_3_bits

def exibir_e_salvar(imagens, prefixo, caminho_base):
    for i, img in enumerate(imagens):
        plt.imshow(img, cmap="gray")
        plt.title(f"{prefixo} - Plano {i+1}")
        plt.axis("off")
        plt.show()
        salvar_imagem(f"{caminho_base}_{prefixo}_Plano_{i+1}.png", img)

caminho_imagem = "c:/Users/jukal/Desktop/Fig0314(a)(100-dollars).tif"
imagem = carregar_imagem(caminho_imagem)
planos_bits = gerar_planos_bits(imagem)
imagens_binarias = gerar_imagens_binarias(planos_bits)
imagens_intensidades = gerar_imagens_intensidades(planos_bits)
imagem_3_bits = gerar_3_bits_mais_significativos(planos_bits)
exibir_e_salvar(imagens_binarias, "Binaria", "c:/Users/jukal/Desktop/Binarias")
exibir_e_salvar(imagens_intensidades, "Intensidade", "c:/Users/jukal/Desktop/Intensidades")
plt.imshow(imagem_3_bits, cmap="gray")
plt.title("Imagem com 3 Bits Mais Significativos")
plt.axis("off")
plt.show()
salvar_imagem("c:/Users/jukal/Desktop/3_Bits_Mais_Significativos.png", imagem_3_bits)