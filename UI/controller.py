import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._current_album = None

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO

        self._view.dd_album.options.clear()
        self._view.lista_visualizzazione_1.controls.clear()

        try:
            minuti = int(self._view.txt_durata.value)
        except ValueError:
            self._view.show_alert('Inserire un intero (numero di minuti)')
            return

        millisecondi = minuti * 60000
        self._model.build_grafo(millisecondi)
        nodi = self._model.G.number_of_nodes()
        archi = self._model.G.number_of_edges()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Grafo creato: {nodi} album, {archi} archi"))

        album = self._model.get_nodes()

        if not album:
            self._view.show_alert('Non è stato possibile caricare le regioni.')
            return

        for a in album:
            option = ft.dropdown.Option(text=a.title, data=a)
            self._view.dd_album.options.append(option)

        self._view.dd_album.update()

        self._view.dd_album.on_change = self.get_selected_album

        self._view.pulsante_analisi_comp.disabled = False

        self._view.update()

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        # TODO

        selected_option = e.control.value
        if not selected_option:
            self._current_album = None
            return

        found = None
        for opt in e.control.options:
            if opt.text == selected_option:
                found = opt.data
                break

        self._current_album = found

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        # TODO

        self._view.lista_visualizzazione_2.controls.clear()

        album = self._current_album

        if not album:
            self._view.show_alert('Selezionare un album prima di premere il bottone.')
            return

        num, lungh = self._model.analisi_componente(album)

        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Dimensione componente: {lungh}'))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Durata totale: {num:.2f} minuti'))

        self._view.pulsante_set_album.disabled = False

        self._view.update()

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO

        self._view.lista_visualizzazione_3.controls.clear()

        try:
            dTOT = int(self._view.txt_durata_totale.value)
        except ValueError:
            self._view.show_alert('Inserire un intero (numero di minuti)')
            return

        result_set = self._model.get_set_album(self._current_album, dTOT)

        num = 0
        for item in result_set:
            num += item.durata

        self._view.lista_visualizzazione_3.controls.append(ft.Text(f'Set trovato ({len(result_set)} album, durata {num:.2f} minuti)'))

        for item in result_set:
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f'- {item.title} ({item.durata:.2f} min)'))

        self._view.update()