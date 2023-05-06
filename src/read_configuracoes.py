import os

absPath = os.path.dirname(os.path.abspath(__file__))

from functions import readExcelPandas, treatNumberFieldInVector, treatTextFieldInVector


class ReadConfiguracoes:
    def __init__(self):
        self._wayConfiguracoes = os.path.join(absPath, "..", "configuracoes.xlsx")
        self._configuracoes = {}

    def process(self):
        for sheet in ["empresas", "contas_contabeis", "historicos", "centro_custos"]:
            settings = []
            setting = {}

            dataExcel = readExcelPandas(self._wayConfiguracoes, nameSheetToFilter=sheet)

            for key, data in enumerate(dataExcel):
                if key == 0:
                    continue

                setting.clear()

                if sheet == "empresas":
                    setting["codigo_dominio"] = treatNumberFieldInVector(data, 1, isInt=True)
                    setting["codigo_siagri"] = treatNumberFieldInVector(data, 4, isInt=True)
                    setting["cgce"] = treatNumberFieldInVector(data, 3)
                elif sheet == "contas_contabeis":
                    setting["codigo_dominio"] = treatNumberFieldInVector(data, 4, isInt=True)
                    setting["codigo_siagri"] = treatTextFieldInVector(data, 3)
                    setting["gera_centro_custo"] = treatTextFieldInVector(data, 7)
                    setting["id_tipo_docto"] = treatTextFieldInVector(data, 9)
                elif sheet == "historicos":
                    setting["codigo_dominio"] = treatNumberFieldInVector(data, 2, isInt=True)
                    setting["codigo_siagri"] = treatTextFieldInVector(data, 3)
                elif sheet == "centro_custos":
                    setting["codigo_dominio"] = f"{treatNumberFieldInVector(data, 1, isInt=True)}-{treatNumberFieldInVector(data, 2, isInt=True)}"
                    setting["codigo_siagri"] = treatTextFieldInVector(data, 4)

                try:
                    if setting["codigo_siagri"] != "" and setting["codigo_siagri"] != "-":
                        settings.append(setting.copy())
                except Exception:
                    pass

            self._configuracoes[sheet] = settings.copy()

        return self._configuracoes


if __name__ == "__main__":
    readConfiguracoes = ReadConfiguracoes()
    readConfiguracoes.process()
