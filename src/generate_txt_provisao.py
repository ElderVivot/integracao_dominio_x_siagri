import os

absPath = os.path.dirname(os.path.abspath(__file__))


class GenerateTxtProvisao:
    def __init__(self, lancamentos, nameFile):
        self._lancamentos = lancamentos
        self._nameFile = nameFile
        self._wayFile = os.path.join(absPath, "..", "siagri", nameFile)

    def formatLancamento(self, lancamento):
        formatLancamento = {}
        formatLancamento["codi_emp"] = f"{lancamento['new_codi_emp']:>3}"
        valorLancamento = f"{lancamento['valor_lancamento']:.2f}"
        formatLancamento["valor_lancamento"] = f"{valorLancamento.replace('.', ''):0>16}"
        formatLancamento["data_lancamento"] = lancamento["data_lancamento"].strftime("%d/%m/%Y")
        formatLancamento["conta_debito"] = f"{lancamento['new_conta_deb']:<12}"
        formatLancamento["conta_credito"] = f"{lancamento['new_conta_cre']:<12}"
        formatLancamento["codigo_historico"] = f"{lancamento['new_codigo_historico']:0>9}"
        formatLancamento["historico"] = f"{lancamento['historico'][:250]:<250}"
        formatLancamento["centro_custo"] = f"{str(lancamento['new_centro_custo']).replace('.', ''):<12}"
        return formatLancamento

    def mountDataRow(self, typeData, formatLancamento):
        if typeData == "FOL":
            return f"FOL{formatLancamento['codi_emp']}{formatLancamento['valor_lancamento']}{formatLancamento['data_lancamento']}"
        elif typeData == "CON-D":
            return f"CON{formatLancamento['codi_emp']}{formatLancamento['conta_debito']}{formatLancamento['valor_lancamento']}D{formatLancamento['codigo_historico']}{formatLancamento['historico']}"
        elif typeData == "CON-C":
            return f"CON{formatLancamento['codi_emp']}{formatLancamento['conta_credito']}{formatLancamento['valor_lancamento']}C{formatLancamento['codigo_historico']}{formatLancamento['historico']}"
        elif typeData == "CUS":
            return f"CUS{formatLancamento['centro_custo']}{formatLancamento['valor_lancamento']}"

    def process(self):
        with open(self._wayFile, "w") as fileWrite:
            for lancamento in self._lancamentos:
                formatLancamento = self.formatLancamento(lancamento)

                rowHeader = self.mountDataRow("FOL", formatLancamento)
                rowContaDebito = self.mountDataRow("CON-D", formatLancamento)
                rowContaCredito = self.mountDataRow("CON-C", formatLancamento)
                rowCentroCusto = self.mountDataRow("CUS", formatLancamento)

                fileWrite.write(f"{rowHeader}\r\n")
                fileWrite.write(f"{rowContaDebito}\r\n")
                fileWrite.write(f"{rowCentroCusto}\r\n")
                fileWrite.write(f"{rowContaCredito}\r\n")
                fileWrite.write(f"{rowCentroCusto}\r\n")
