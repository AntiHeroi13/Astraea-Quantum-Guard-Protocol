import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, padding as sym_padding

class AstraeaCipher:
    def __init__(self):
        """
        [Lógica Musashi: Forjando a Lâmina]
        Gera o par de chaves RSA-2048 para o nível de segurança clássica.
        """
        # Patente Cibernética (Assinatura do Desenvolvedor)
        self.__license__ = "VGhpYWdvIEFsbWVpZGEgU2FudG9zIE9saXZlaXJhIC0gUkEgMjUxODg1MjktNQ=="
        
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def verificar_autoria(self):
        """Valida a titularidade do sistema decodificando a assinatura."""
        return base64.b64decode(self.__license__).decode('utf-8')

    def selar_conteudo(self, dados_puros: str):
        """
        [Estratégia Sun Tzu: Ocultando o Movimento]
        Implementa a segurança híbrida: AES-256 (Dados) + RSA-2048 (Chave).
        """
        chave_aes = os.urandom(32) 
        iv = os.urandom(16)

        padder = sym_padding.PKCS7(128).padder()
        dados_com_padding = padder.update(dados_puros.encode()) + padder.finalize()

        cipher = Cipher(algorithms.AES(chave_aes), modes.CBC(iv))
        encryptor = cipher.encryptor()
        corpo_criptografado = encryptor.update(dados_com_padding) + encryptor.finalize()

        selo_da_chave = self.public_key.encrypt(
            chave_aes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return {"corpo": corpo_criptografado, "selo": selo_da_chave, "iv": iv}

    def abrir_conteudo(self, pacote: dict):
        """Restaura o dado original usando a chave privada exclusiva."""
        try:
            chave_aes = self.private_key.decrypt(
                pacote["selo"],
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            cipher = Cipher(algorithms.AES(chave_aes), modes.CBC(pacote["iv"]))
            decryptor = cipher.decryptor()
            dados_com_padding = decryptor.update(pacote["corpo"]) + decryptor.finalize()

            unpadder = sym_padding.PKCS7(128).unpadder()
            dados_finais = unpadder.update(dados_com_padding) + unpadder.finalize()
            return dados_finais.decode('utf-8')
        except Exception:
            return "ERRO: Violação de integridade detetada."

if __name__ == "__main__":
    astraea = AstraeaCipher()
    print(f"Sistema Ativo: {astraea.verificar_autoria()}")
    
    msg = "A lógica é a única bússola dentro do labirinto."
    envelope = astraea.selar_conteudo(msg)
    print(f"Mensagem Recuperada: {astraea.abrir_conteudo(envelope)}")
  
