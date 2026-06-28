import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def ddda(self):
        self._view._ddcategory.options.clear()
        self._view._ddcategory.value = None

        listaS = self._model.getDateCategory()

        for l in listaS:
            self._view._ddcategory.options.append(
                ft.dropdown.Option(
                    key=l.category_id,
                    text=l.category_name,
                )
            )
        self._view.update_page()




    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        try:
            store = str(self._view._dp1.value)[:10]
            k = str(self._view._dp2.value)[:10]
            cat = str(self._view._ddcategory.value)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("selezionare entrambi gli anni"))
        if store is None or k is None:
            self._view.txt_result.controls.append(
                ft.Text("selezionare entrambi i campi", color="red")
            )

        self._model.build_graph(store, k,cat)
        stats = self._model.get_stats()
        self._view.txt_result.controls.append(ft.Text(f"stats:{stats[0]} e {stats[1]}"))
        self._view.update_page()


    def handleBestProdotti(self, e):
        listatop=self._model.topprod()
        for a in listatop:
            self._view.txt_result.controls.append(ft.Text(f"{a[0].product_name}, {a[1]}" ))
        self._view.update_page()


    def handleCercaCammino(self, e):
        pass



    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)
