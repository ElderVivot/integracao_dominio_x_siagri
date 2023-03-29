import os
import sys

absPath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(absPath, '..'))

from read_configuracoes import ReadConfiguracoes
from read_lanc_dominio import ReadLancamentosDominio
from process_lancamentos import ProcessLancamentos
from generate_txt_provisao import GenerateTxtProvisao
from generate_txt_contas_pagar import GenerateTxtContasPagar


class MainLancamentos():
    def __init__(self):
        self._wayLancDominio = 'dominio'
        self._readLancamentosDominio = ReadLancamentosDominio()
        self._readConfiguracoes = ReadConfiguracoes()
        self._configuracoes = self._readConfiguracoes.process()
        self._typeProcess = 2  # when 1 then layout provisao, when 2 then layout contas a pagar

    def process(self, wayFile):
        lancamentos = self._readLancamentosDominio.process(wayFile)

        process_lancamentos = ProcessLancamentos(lancamentos, self._configuracoes)
        lancamentos = process_lancamentos.process()

        nameFile = os.path.basename(wayFile)
        if self._typeProcess == 1:
            generate_txt_provisao = GenerateTxtProvisao(lancamentos, nameFile)
            generate_txt_provisao.process()
        elif self._typeProcess == 2:
            generate_txt_contas_pagar = GenerateTxtContasPagar(lancamentos, nameFile)
            generate_txt_contas_pagar.process()

    def processAll(self):
        for root, _, files in os.walk(self._wayLancDominio):
            for file in files:
                if file.lower().endswith(('.txt')):
                    wayFile = os.path.join(root, file)
                    print(f'- Processando arquivo {file}')
                    self.process(wayFile)


if __name__ == "__main__":
    main = MainLancamentos()
    main.processAll()
