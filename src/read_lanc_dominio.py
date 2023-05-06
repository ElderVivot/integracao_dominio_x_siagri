from functions import readTxt, treatDateFieldInVector, treatDecimalFieldInVector, treatNumberFieldInVector, treatTextFieldInVector


class ReadLancamentosDominio:
    def process(self, wayFile):
        lancamentos = []
        lancamentoDaFolha = {}

        dataTxt = readTxt(wayFile, removeBlankLines=True)

        for data in dataTxt:
            lancamentoDaFolha.clear()
            lancamentoDaFolha["codi_emp"] = treatNumberFieldInVector(data, 3, isInt=True, positionInFileEnd=10)
            lancamentoDaFolha["conta_deb"] = treatNumberFieldInVector(data, 11, isInt=True, positionInFileEnd=17)
            lancamentoDaFolha["conta_cre"] = treatNumberFieldInVector(data, 18, isInt=True, positionInFileEnd=24)
            lancamentoDaFolha["valor_lancamento"] = treatDecimalFieldInVector(data, 25, positionInFileEnd=39)
            lancamentoDaFolha["codigo_historico"] = treatNumberFieldInVector(data, 40, isInt=True, positionInFileEnd=46)
            lancamentoDaFolha["historico"] = treatTextFieldInVector(data, 47, positionInFileEnd=296)
            lancamentoDaFolha["centro_custo"] = treatNumberFieldInVector(data, 297, isInt=True, positionInFileEnd=303)
            lancamentoDaFolha["data_lancamento"] = treatDateFieldInVector(data, 304, positionInFileEnd=313)
            if lancamentoDaFolha["codi_emp"] > 0:
                lancamentos.append(lancamentoDaFolha.copy())

        return lancamentos
