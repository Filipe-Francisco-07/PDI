import numpy as np

def ler_ppm(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        cabecalho = f.readline().strip()
        if cabecalho != 'P3':
            raise ValueError('Formato inválido.')

        linha_dimensoes = f.readline().strip()
        while linha_dimensoes.startswith('#'):
            linha_dimensoes = f.readline().strip()

        largura, altura = map(int, linha_dimensoes.split())
        max_val = int(f.readline().strip())

        if max_val != 255:
            raise ValueError('Max_val inválido.')

        dados = []
        for linha in f:
            valores = map(int, linha.split())
            dados.extend(valores)

        dados = np.array(dados, dtype=np.uint8).reshape((altura, largura, 3))

    return dados, largura, altura

def escrever_ppm(caminho_arquivo, dados):
    altura, largura, _ = dados.shape
    with open(caminho_arquivo, 'w') as f:
        f.write('P3\n')
        f.write(f"{largura} {altura}\n")
        f.write("255\n")
        for linha in dados:
            for pixel in linha:
                f.write(f"{pixel[0]} {pixel[1]} {pixel[2]} ")
            f.write("\n")

def comprimir_rle(imagem):
    altura, largura, _ = imagem.shape
    dados_comprimidos = [largura, altura]

    for cor in range(3):
        for linha in imagem[:, :, cor]:
            codificacao = []
            contagem = 1
            anterior = linha[0]

            for pixel in linha[1:]:
                if pixel == anterior and contagem < 127:
                    contagem += 1
                else:
                    if contagem > 1:
                        codificacao.extend([contagem, anterior])
                    else:
                        codificacao.extend([-1, anterior])
                    contagem = 1
                    anterior = pixel

            if contagem > 1:
                codificacao.extend([contagem, anterior])
            else:
                codificacao.extend([-1, anterior])

            dados_comprimidos.extend(codificacao)

    return dados_comprimidos

def descomprimir_rle(dados_comprimidos):
    largura, altura = dados_comprimidos[:2]
    dados_comprimidos = dados_comprimidos[2:]
    imagem_descomprimida = np.zeros((altura, largura, 3), dtype=np.uint8)

    indice = 0
    for cor in range(3): 
        for linha in range(altura):
            linha_atual = []
            while len(linha_atual) < largura:
                contagem = dados_comprimidos[indice]
                indice += 1
                if contagem > 0: 
                    valor = dados_comprimidos[indice]
                    linha_atual.extend([valor] * contagem)
                    indice += 1
                else:  
                    valores = dados_comprimidos[indice:indice - contagem]
                    linha_atual.extend(valores)
                    indice -= contagem

            imagem_descomprimida[linha, :, cor] = linha_atual[:largura]

    return imagem_descomprimida

if __name__ == "__main__":
    entrada = "EntradaRGB.ppm"
    comprimido = "imagem_comprimida.rle"
    saida = "imagem_descomprimida.ppm"

    imagem, largura, altura = ler_ppm(entrada)
    dados_comprimidos = comprimir_rle(imagem)

    with open(comprimido, 'wb') as f:
        f.write(np.array(dados_comprimidos, dtype=np.int16).tobytes())

    with open(comprimido, 'rb') as f:
        dados_lidos = np.frombuffer(f.read(), dtype=np.int16).tolist()

    imagem_descomprimida = descomprimir_rle(dados_lidos)
    escrever_ppm(saida, imagem_descomprimida)

