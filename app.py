import tkinter as tk
from tkinter import messagebox, simpledialog

# Classe pour représenter un joueur
class Joueur:
    def __init__(self, nom, poste, numero):
        self.nom = nom
        self.poste = poste
        self.numero = numero

    def __str__(self):
        return f"{self.numero} - {self.nom} ({self.poste})"

# Classe principale de l'application
class GestionEquipe:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion d'Équipe de Football")
        self.root.geometry("400x400")

        self.joueurs = []

        # Interface graphique
        self.label = tk.Label(root, text="Liste des joueurs :")
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(pady=10)

        self.btn_ajouter = tk.Button(root, text="Ajouter Joueur", command=self.ajouter_joueur)
        self.btn_ajouter.pack(pady=5)

        self.btn_supprimer = tk.Button(root, text="Supprimer Joueur", command=self.supprimer_joueur)
        self.btn_supprimer.pack(pady=5)

        self.btn_quitter = tk.Button(root, text="Quitter", command=root.quit)
        self.btn_quitter.pack(pady=5)

    def ajouter_joueur(self):
        nom = simpledialog.askstring("Nom", "Entrez le nom du joueur :")
        if not nom:
            return
        poste = simpledialog.askstring("Poste", "Entrez le poste du joueur :")
        if not poste:
            return
        numero = simpledialog.askinteger("Numéro", "Entrez le numéro du joueur :")
        if not numero:
            return

        joueur = Joueur(nom, poste, numero)
        self.joueurs.append(joueur)
        self.update_listbox()

    def supprimer_joueur(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un joueur à supprimer")
            return
        index = selection[0]
        del self.joueurs[index]
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for joueur in self.joueurs:
            self.listbox.insert(tk.END, str(joueur))

# Création de la fenêtre Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    app = GestionEquipe(root)
    root.mainloop()
