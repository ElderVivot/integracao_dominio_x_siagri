import os
from random import uniform

absPath = os.path.dirname(os.path.abspath(__file__))


class GenerateTxtContasPagar():
    def __init__(self, lancamentos, nameFile):
        self._lancamentos = lancamentos
        self._nameFile = nameFile
        self._wayFile = os.path.join(absPath, '..', 'siagri', nameFile)

    def formatLancamento(self, lancamento):
        formatLancamento = {}
        formatLancamento['codi_emp'] = f"{lancamento['new_codi_emp']:>3}"
        formatLancamento['cgce_emp'] = f"{lancamento['new_cgce_emp']:0>14}"
        valorLancamento = f"{lancamento['valor_lancamento']:.2f}"
        formatLancamento['valor_lancamento'] = f"{valorLancamento.replace('.', ''):0>16}"
        formatLancamento['data_lancamento'] = lancamento['data_lancamento'].strftime("%d/%m/%Y")
        formatLancamento['conta_debito'] = f"{lancamento['new_conta_deb']:<12}"
        formatLancamento['conta_credito'] = f"{lancamento['new_conta_cre']:<12}"
        formatLancamento['id_tipo_docto'] = f"{lancamento['new_id_tipo_docto_deb']:0>9}" if lancamento['new_id_tipo_docto_deb'] != "" \
            else f"{lancamento['new_id_tipo_docto_cre']:0>9}"
        formatLancamento['codigo_historico'] = f"{lancamento['new_codigo_historico']:0>9}"
        formatLancamento['historico'] = f"{lancamento['historico'][:250]:<250}"
        formatLancamento['centro_custo'] = f"{str(lancamento['new_centro_custo']).replace('.', ''):<12}"
        return formatLancamento

    def mountDataRow(self, typeData, formatLan):
        if typeData == 'CAB':
            # idTipoDoc = f"{0:0>9}" if formatLancamento['id_tipo_docto'] == '' else formatLancamento['id_tipo_docto']
            sinalDoc = ' '
            identificaoDoc = f"{str(uniform(1, 9999999999)).split('.')[0]:0>10}"
            idCondicaoPag = f"{5:0>9}"
            idIndexador = f"{0:0>9}"
            dataIndexador = f"{0:0>10}"
            return f"CAB{formatLan['codi_emp']}{formatLan['id_tipo_docto']}{sinalDoc}{formatLan['cgce_emp']}{identificaoDoc}{formatLan['data_lancamento']}{formatLan['valor_lancamento']}{idCondicaoPag}{idIndexador}{dataIndexador}"
        elif typeData == 'PAR':
            numeroParcelas = '001'
            idPortador = f"{'11000026':0>9}"
            idTipoCobranca = f"{'11000077':0>9}"
            tipoJuro = 'S'
            camposNaoNecessario8ao13 = f"{0:0>35}"
            camposNaoNecessario14ao15 = f"{' ':<251}"
            formaPagto = 'O'
            numeroBanco = f"{0:0>3}"
            tipoConta = f"{' ':<2}"
            numeroAgencia = f"{0:0>5}"
            dvAgencia = f"{' ':<1}"
            numeroConta = f"{0:0>12}"
            dvConta = f"{' ':<1}"
            dvAgenciaConta = f"{' ':<1}"
            tipoFavorecido = f"{' ':<1}"
            cpfCnpjFavorecido = f"{0:0>14}"
            nomeFavorecido = f"{' ':<65}"
            return f"PAR{numeroParcelas}{formatLan['data_lancamento']}{formatLan['valor_lancamento']}{idPortador}{idTipoCobranca}{tipoJuro}{camposNaoNecessario8ao13}{camposNaoNecessario14ao15}{formaPagto}{numeroBanco}{tipoConta}{numeroAgencia}{dvAgencia}{numeroConta}{dvConta}{dvAgenciaConta}{tipoFavorecido}{cpfCnpjFavorecido}{nomeFavorecido}"
        elif typeData == 'CON-D':
            return f"CON{formatLan['codi_emp']}{formatLan['conta_debito']}{formatLan['valor_lancamento']}D{formatLan['codigo_historico']}{formatLan['historico']}"
        elif typeData == 'CON-C':
            return f"CON{formatLan['codi_emp']}{formatLan['conta_credito']}{formatLan['valor_lancamento']}C{formatLan['codigo_historico']}{formatLan['historico']}"
        elif typeData == 'CUS':
            return f"CUS{formatLan['centro_custo']}{formatLan['valor_lancamento']}"

    def process(self):
        with open(self._wayFile, 'w') as fileWrite:
            for lancamento in self._lancamentos:
                formatLancamento = self.formatLancamento(lancamento)

                rowHeader = self.mountDataRow('CAB', formatLancamento)
                rowParcelaContaPagar = self.mountDataRow('PAR', formatLancamento)
                rowContaDebito = self.mountDataRow('CON-D', formatLancamento)
                rowContaCredito = self.mountDataRow('CON-C', formatLancamento)
                rowCentroCusto = self.mountDataRow('CUS', formatLancamento)

                fileWrite.write(f"{rowHeader}\r\n")
                fileWrite.write(f"{rowParcelaContaPagar}\r\n")

                print(lancamento['new_id_tipo_docto_deb'], lancamento['new_id_tipo_docto_cre'])

                if lancamento['new_id_tipo_docto_deb'] == "":
                    fileWrite.write(f"{rowContaDebito}\r\n")

                if lancamento['new_gera_centro_custo_deb'] == 'SIM':
                    fileWrite.write(f"{rowCentroCusto}\r\n")

                # gera o lancamento a credito se não existir tipo_docto pro credito, ou se se existir pro débito, pq no minimo umas contas devem ser geradas
                if lancamento['new_id_tipo_docto_cre'] == "" or lancamento['new_id_tipo_docto_deb'] != "":
                    fileWrite.write(f"{rowContaCredito}\r\n")

                if lancamento['new_gera_centro_custo_cre'] == 'SIM':
                    fileWrite.write(f"{rowCentroCusto}\r\n")
