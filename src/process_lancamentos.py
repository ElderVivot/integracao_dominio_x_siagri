class ProcessLancamentos:
    def __init__(self, lancamentos, configuracoes):
        self._lancamentos = lancamentos
        self._configuracoes = configuracoes

    def searchDePara(self, sheet, codeDominio, fieldReturn="codigo_siagri"):
        for setting in self._configuracoes[sheet]:
            if setting["codigo_dominio"] == codeDominio:
                return setting[fieldReturn]
        return ""

    def returnNewLancamento(self, lancamento):
        newLancamento = lancamento
        newLancamento["new_codi_emp"] = self.searchDePara("empresas", lancamento["codi_emp"])
        newLancamento["new_cgce_emp"] = self.searchDePara("empresas", lancamento["codi_emp"], "cgce")
        newLancamento["new_conta_deb"] = self.searchDePara("contas_contabeis", lancamento["conta_deb"])
        newLancamento["new_conta_cre"] = self.searchDePara("contas_contabeis", lancamento["conta_cre"])
        newLancamento["new_gera_centro_custo_deb"] = self.searchDePara("contas_contabeis", lancamento["conta_deb"], "gera_centro_custo")
        newLancamento["new_gera_centro_custo_cre"] = self.searchDePara("contas_contabeis", lancamento["conta_cre"], "gera_centro_custo")
        newLancamento["new_id_tipo_docto_deb"] = self.searchDePara("contas_contabeis", lancamento["conta_deb"], "id_tipo_docto")
        newLancamento["new_id_tipo_docto_cre"] = self.searchDePara("contas_contabeis", lancamento["conta_cre"], "id_tipo_docto")
        newLancamento["new_codigo_historico"] = self.searchDePara("historicos", lancamento["codigo_historico"])
        newLancamento["new_centro_custo"] = self.searchDePara("centro_custos", f"{lancamento['codi_emp']}-{lancamento['centro_custo']}")

        return newLancamento

    def showWarnings(self, numberRow, newLancamento):
        if newLancamento["new_codi_emp"] == "":
            print(f"\t- Na linha {numberRow} nao encontrou o de-para da empresa {newLancamento['codi_emp']}")
        elif newLancamento["new_conta_deb"] == "":
            print(f"\t- Na linha {numberRow} nao encontrou o de-para da conta debito {newLancamento['conta_deb']}")
        elif newLancamento["new_conta_cre"] == "":
            print(f"\t- Na linha {numberRow} nao encontrou o de-para da conta credito {newLancamento['conta_cre']}")
        elif newLancamento["new_codigo_historico"] == "":
            print(f"\t- Na linha {numberRow} nao encontrou o de-para do historico {newLancamento['codigo_historico']}")
        elif newLancamento["new_centro_custo"] == "" and newLancamento["centro_custo"] != 0:
            print(
                f"\t- Na linha {numberRow} nao encontrou o de-para do centro custo {newLancamento['centro_custo']} \
                    referente à empresa {newLancamento['codi_emp']}"
            )

    def process(self):
        lancamentos = []
        for key, lancamento in enumerate(self._lancamentos):
            numberRow = key + 1
            newLancamento = self.returnNewLancamento(lancamento)
            self.showWarnings(numberRow, newLancamento)
            lancamentos.append(newLancamento)

        return lancamentos
