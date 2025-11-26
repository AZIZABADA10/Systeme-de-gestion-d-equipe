import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import json
import os
from datetime import datetime
import shutil

# Matplotlib for charts
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuration du thème
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Player:
    def __init__(self, id, nom_complet, telephone, image_path, date_naissance, poste, numero):
        self.id = id
        self.nom_complet = nom_complet
        self.telephone = telephone
        self.image_path = image_path
        self.date_naissance = date_naissance  # format attendu: "JJ/MM/AAAA"
        self.poste = poste
        self.numero = numero

class ModernPlayerModal(ctk.CTkToplevel):
    def __init__(self, parent, player):
        super().__init__(parent)
        self.title(f"Détails - {player.nom_complet}")
        self.geometry("500x650")
        self.resizable(False, False)
        self.configure(fg_color="#0f0f0f")

        # Centrer la fenêtre
        self.transient(parent)
        self.grab_set()

        # Container principal avec effet de verre
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=25, pady=25)

        # Carte principale
        card_frame = ctk.CTkFrame(
            main_container,
            fg_color="#1e1e1e",
            corner_radius=20,
            border_color="#3498db",
            border_width=2
        )
        card_frame.pack(fill="both", expand=True)

        # En-tête
        header_frame = ctk.CTkFrame(
            card_frame,
            fg_color="#2c3e50",
            corner_radius=18,
            height=80
        )
        header_frame.pack(fill="x", padx=10, pady=10)
        header_frame.pack_propagate(False)

        ctk.CTkLabel(
            header_frame,
            text="👤 FICHE DU JOUEUR",
            font=("Segoe UI", 20, "bold"),
            text_color="#ecf0f1"
        ).pack(expand=True)

        # Photo
        photo_container = ctk.CTkFrame(card_frame, fg_color="transparent")
        photo_container.pack(pady=20)

        if player.image_path and os.path.exists(player.image_path):
            try:
                img = Image.open(player.image_path)
                img = ImageOps.fit(img, (140, 140), method=Image.Resampling.LANCZOS)
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(140, 140))
                img_label = ctk.CTkLabel(photo_container, image=photo, text="")
                img_label.image = photo
                img_label.pack()
            except Exception:
                self.show_default_avatar(photo_container)
        else:
            self.show_default_avatar(photo_container)

        # Informations
        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=30, pady=10)

        details = [
            ("👤 NOM COMPLET", player.nom_complet),
            ("📞 TÉLÉPHONE", player.telephone),
            ("🎂 DATE DE NAISSANCE", player.date_naissance),
            ("⚽ POSTE", player.poste),
            ("🔢 NUMÉRO", f"#{player.numero}")
        ]

        for i, (label, value) in enumerate(details):
            item_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=8)

            ctk.CTkLabel(
                item_frame,
                text=label,
                font=("Segoe UI", 12, "bold"),
                text_color="#7f8c8d",
                anchor="w"
            ).pack(fill="x")

            value_bg = "#2c3e50" if i % 2 == 0 else "#34495e"
            value_frame = ctk.CTkFrame(
                item_frame,
                fg_color=value_bg,
                corner_radius=8,
                height=35
            )
            value_frame.pack(fill="x", pady=(5, 0))
            value_frame.pack_propagate(False)

            ctk.CTkLabel(
                value_frame,
                text=value,
                font=("Segoe UI", 14, "bold"),
                text_color="#ecf0f1"
            ).pack(expand=True)

        # Bouton fermer
        button_container = ctk.CTkFrame(card_frame, fg_color="transparent")
        button_container.pack(fill="x", padx=30, pady=20)

        ctk.CTkButton(
            button_container,
            text="✕ FERMER",
            command=self.destroy,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            font=("Segoe UI", 14, "bold"),
            height=45,
            corner_radius=10
        ).pack(fill="x")

    def show_default_avatar(self, parent):
        avatar_frame = ctk.CTkFrame(
            parent,
            fg_color="#34495e",
            width=140,
            height=140,
            corner_radius=70
        )
        avatar_frame.pack()
        avatar_frame.pack_propagate(False)

        ctk.CTkLabel(
            avatar_frame,
            text="👤",
            font=("Segoe UI", 40),
            text_color="#bdc3c7"
        ).pack(expand=True)

class ModernTeamManagementSystem(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("⚽ Gestion d'Équipe - Manager Pro")
        self.geometry("1300x800")
        self.minsize(1200, 700)

        # Variables
        self.players = []
        self.next_id = 1
        self.selected_image_path = None
        self.current_edit_id = None

        # Couleurs modernes
        self.colors = {
            "primary": "#3498db",
            "secondary": "#2c3e50",
            "success": "#27ae60",
            "danger": "#e74c3c",
            "warning": "#f39c12",
            "dark": "#1a1a1a",
            "darker": "#0f0f0f"
        }

        # Créer le dossier pour les images
        self.images_dir = "player_images"
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)

        # UI setup
        self.load_data()
        self.create_modern_ui()
        self.show_dashboard()

    def create_modern_ui(self):
        # Configuration de la grille principale
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar moderne
        self.create_sidebar()

        # Content area
        self.create_content_area()

    def show_dashboard(self):
        # Vider le contenu actuel
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        dash = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        dash.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        dash.grid_columnconfigure(0, weight=1)
        dash.grid_columnconfigure(1, weight=1)
        dash.grid_rowconfigure(1, weight=1)

        # ----------------------------#
        #     STATISTICS CARDS
        # ----------------------------#
        stats_frame = ctk.CTkFrame(dash, fg_color=self.colors["secondary"], corner_radius=15)
        stats_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        stats_frame.grid_columnconfigure((0,1,2,3), weight=1)

        total_players = len(self.players)
        g = len([p for p in self.players if p.poste == "Gardien"])
        d = len([p for p in self.players if p.poste == "Défenseur"])
        m = len([p for p in self.players if p.poste == "Milieu"])
        a = len([p for p in self.players if p.poste == "Attaquant"])

        # Calcul moyenne d'âge (si date fournie)
        ages = []
        for p in self.players:
            try:
                if p.date_naissance:
                    day, month, year = map(int, p.date_naissance.split("/"))
                    dob = datetime(year, month, day)
                    age = (datetime.now() - dob).days // 365
                    ages.append(age)
            except Exception:
                continue
        avg_age = int(sum(ages) / len(ages)) if ages else "-"

        cards = [
            ("👥 Total Joueurs", total_players),
            ("⚽ Moyenne d'âge", avg_age),
            ("🧤 Gardiens", g),
            ("🛡️ Défenseurs", d),
        ]

        for i, (title, value) in enumerate(cards):
            card = ctk.CTkFrame(stats_frame, fg_color="#1e1e1e", corner_radius=12)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(card, text=title, font=("Segoe UI", 14), text_color="#bdc3c7").pack(pady=5)
            ctk.CTkLabel(card, text=str(value), font=("Segoe UI", 24, "bold"), text_color=self.colors["primary"]).pack()

        # ----------------------------#
        #     CHART: distribution par poste
        # ----------------------------#
        chart_frame = ctk.CTkFrame(dash, fg_color=self.colors["dark"])
        chart_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        chart_frame.grid_rowconfigure(0, weight=1)
        chart_frame.grid_columnconfigure(0, weight=1)

        positions = ["Gardien", "Défenseur", "Milieu", "Attaquant"]
        counts = [g, d, m, a]
        fig = Figure(figsize=(4.5, 3.0), dpi=100)
        ax = fig.add_subplot(111)
        bars = ax.bar(positions, counts)
        ax.set_title("Répartition par poste")
        ax.set_ylabel("Nombre de joueurs")
        ax.bar_label(bars, labels=[str(x) for x in counts], padding=3)

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True, padx=5, pady=5)

        # ----------------------------#
        #     LAST ADDED PLAYERS
        # ----------------------------#
        list_frame = ctk.CTkFrame(dash, fg_color=self.colors["dark"])
        list_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        list_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(list_frame, text="🆕 Derniers joueurs ajoutés",
                     font=("Segoe UI", 18, "bold"), text_color="#ecf0f1").pack(pady=10)

        last_list = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        last_list.pack(fill="both", expand=True, padx=10, pady=10)

        for p in self.players[-5:][::-1]:
            item = ctk.CTkFrame(last_list, fg_color="#2c3e50", corner_radius=10)
            item.pack(fill="x", pady=5)
            ctk.CTkLabel(item, text=f"{p.nom_complet} - {p.poste} (#{p.numero})",
                         font=("Segoe UI", 14), text_color="#ecf0f1").pack(padx=10, pady=8, anchor="w")

        # ----------------------------#
        #     UPCOMING BIRTHDAYS
        # ----------------------------#
        bday_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        bday_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0,10))
        bday_frame.grid_columnconfigure((0,1), weight=1)

        left = ctk.CTkFrame(bday_frame, fg_color=self.colors["dark"])
        left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        right = ctk.CTkFrame(bday_frame, fg_color=self.colors["dark"])
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(left, text="🎂 Anniversaires du mois",
                     font=("Segoe UI", 18, "bold"), text_color="#ecf0f1").pack(pady=10)

        ctk.CTkLabel(right, text="🔎 Rapide",
                     font=("Segoe UI", 18, "bold"), text_color="#ecf0f1").pack(pady=10)

        bday_list = ctk.CTkScrollableFrame(left, fg_color="transparent")
        bday_list.pack(fill="both", expand=True, padx=10, pady=10)

        current_month = datetime.now().month
        birthdays = []
        for p in self.players:
            try:
                if p.date_naissance:
                    parts = p.date_naissance.split("/")
                    if len(parts) >= 2 and int(parts[1]) == current_month:
                        birthdays.append(p)
            except Exception:
                continue

        if birthdays:
            for p in birthdays:
                item = ctk.CTkFrame(bday_list, fg_color="#2c3e50", corner_radius=10)
                item.pack(fill="x", pady=5)
                ctk.CTkLabel(item, text=f"{p.nom_complet} — {p.date_naissance}",
                             font=("Segoe UI", 14), text_color="#ecf0f1").pack(padx=10, pady=8, anchor="w")
        else:
            ctk.CTkLabel(bday_list, text="Aucun anniversaire ce mois.",
                         font=("Segoe UI", 14), text_color="#7f8c8d").pack(pady=20)

        # Quick stats on right
        stats_quick = ctk.CTkFrame(right, fg_color="#1e1e1e", corner_radius=10)
        stats_quick.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(stats_quick, text=f"Joueurs totaux: {total_players}", font=("Segoe UI", 16), text_color="#ecf0f1").pack(pady=8)
        ctk.CTkLabel(stats_quick, text=f"Gardiens: {g}", font=("Segoe UI", 14), text_color="#bdc3c7").pack(pady=4)
        ctk.CTkLabel(stats_quick, text=f"Défenseurs: {d}", font=("Segoe UI", 14), text_color="#bdc3c7").pack(pady=4)
        ctk.CTkLabel(stats_quick, text=f"Milieux: {m}", font=("Segoe UI", 14), text_color="#bdc3c7").pack(pady=4)
        ctk.CTkLabel(stats_quick, text=f"Attaquants: {a}", font=("Segoe UI", 14), text_color="#bdc3c7").pack(pady=4)

    def create_sidebar(self):
        # Sidebar avec fond sombre
        sidebar = ctk.CTkFrame(
            self,
            fg_color=self.colors["darker"],
            corner_radius=0,
            width=280
        )
        sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        sidebar.pack_propagate(False)

        # Logo et titre
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent", height=120)
        logo_frame.pack(fill="x", pady=(20, 10))
        logo_frame.pack_propagate(False)

        ctk.CTkLabel(
            logo_frame,
            text="⚽",
            font=("Segoe UI", 40),
            text_color=self.colors["primary"]
        ).pack(pady=(10, 0))

        ctk.CTkLabel(
            logo_frame,
            text="TEAM MANAGER",
            font=("Segoe UI", 18, "bold"),
            text_color="#ecf0f1"
        ).pack()

        ctk.CTkLabel(
            logo_frame,
            text="PRO EDITION",
            font=("Segoe UI", 10),
            text_color="#7f8c8d"
        ).pack()

        # Menu de navigation
        nav_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", padx=20, pady=20)

        menu_items = [
            ("🏠 Tableau de Bord", "dashboard"),
            ("👥 Gestion Joueurs", "players"),
            ("📊 Statistiques", "stats"),
            ("⚙️ Paramètres", "settings")
        ]

        for text, command in menu_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=lambda cmd=command: self.navigate(cmd),
                fg_color="transparent",
                hover_color="#2c3e50",
                font=("Segoe UI", 14),
                height=50,
                anchor="w"
            )
            btn.pack(fill="x", pady=2)

        # Statistiques en bas de sidebar
        stats_frame = ctk.CTkFrame(sidebar, fg_color="#2c3e50", corner_radius=10)
        stats_frame.pack(side="bottom", fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            stats_frame,
            text="📈 STATISTIQUES",
            font=("Segoe UI", 12, "bold"),
            text_color="#bdc3c7"
        ).pack(pady=(10, 5))

        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text=f"Joueurs: {len(self.players)}",
            font=("Segoe UI", 14, "bold"),
            text_color="#ecf0f1"
        )
        self.stats_label.pack(pady=(0, 10))

    def create_content_area(self):
        # Zone de contenu principale (exposée en tant qu'attribut)
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.colors["secondary"],
            height=80,
            corner_radius=15
        )
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header.grid_columnconfigure(0, weight=1)
        header.pack_propagate(False)

        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", padx=30, pady=15)

        ctk.CTkLabel(
            header_content,
            text="👥 GESTION DES JOUEURS",
            font=("Segoe UI", 24, "bold"),
            text_color="#ecf0f1"
        ).pack(side="left")


    def create_main_tabs(self, parent):
        # Frame pour les onglets (placé mais caché dans dashboard view)
        tabs_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tabs_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        self.tabview = ctk.CTkTabview(
            tabs_frame,
            fg_color=self.colors["dark"],
            segmented_button_fg_color=self.colors["secondary"],
            segmented_button_selected_color=self.colors["primary"],
            segmented_button_selected_hover_color=self.colors["primary"],
            corner_radius=15
        )
        self.tabview.pack(fill="both", expand=True)

        # Onglet Ajouter/Modifier
        self.add_tab = self.tabview.add("➕ AJOUTER")
        # Onglet Liste
        self.list_tab = self.tabview.add("📋 LISTE")

        self.create_add_tab()
        self.create_list_tab()

    def create_add_tab(self):
        # Configuration de la grille pour l'onglet d'ajout
        self.add_tab.grid_columnconfigure(0, weight=1)
        self.add_tab.grid_rowconfigure(0, weight=1)

        # Frame scrollable
        scroll_frame = ctk.CTkScrollableFrame(
            self.add_tab,
            fg_color="transparent"
        )
        scroll_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Carte du formulaire
        form_card = ctk.CTkFrame(
            scroll_frame,
            fg_color="#1e1e1e",
            corner_radius=15
        )
        form_card.pack(fill="both", expand=True, padx=10, pady=10)

        # Titre du formulaire
        ctk.CTkLabel(
            form_card,
            text="🎯 INFORMATIONS DU JOUEUR",
            font=("Segoe UI", 20, "bold"),
            text_color=self.colors["primary"]
        ).pack(pady=30)

        # Photo de profil
        self.create_photo_section(form_card)

        # Champs du formulaire
        form_fields = ctk.CTkFrame(form_card, fg_color="transparent")
        form_fields.pack(fill="both", expand=True, padx=40, pady=20)

        self.nom_entry = self.create_modern_field(form_fields, "👤 Nom Complet", 0)
        self.tel_entry = self.create_modern_field(form_fields, "📞 Téléphone", 1)
        self.date_entry = self.create_modern_field(form_fields, "🎂 Date de Naissance (JJ/MM/AAAA)", 2)

        # Poste et Numéro sur la même ligne
        poste_num_frame = ctk.CTkFrame(form_fields, fg_color="transparent")
        poste_num_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
        poste_num_frame.grid_columnconfigure(0, weight=1)
        poste_num_frame.grid_columnconfigure(1, weight=1)

        # Poste de jeu
        ctk.CTkLabel(
            poste_num_frame,
            text="⚽ Poste de Jeu",
            font=("Segoe UI", 14, "bold"),
            text_color="#bdc3c7"
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.poste_var = ctk.StringVar(value="Attaquant")
        postes = ["Gardien", "Défenseur", "Milieu", "Attaquant"]
        self.poste_menu = ctk.CTkOptionMenu(
            poste_num_frame,
            variable=self.poste_var,
            values=postes,
            fg_color="#2c3e50",
            button_color=self.colors["primary"],
            button_hover_color="#2980b9",
            dropdown_fg_color="#2c3e50",
            dropdown_hover_color="#34495e"
        )
        self.poste_menu.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        # Numéro de maillot
        ctk.CTkLabel(
            poste_num_frame,
            text="🔢 Numéro de Maillot",
            font=("Segoe UI", 14, "bold"),
            text_color="#bdc3c7"
        ).grid(row=0, column=1, sticky="w", pady=(0, 5))

        self.numero_entry = ctk.CTkEntry(
            poste_num_frame,
            height=40,
            fg_color="#2c3e50",
            border_color=self.colors["primary"],
            border_width=2,
            font=("Segoe UI", 14),
            placeholder_text="ex: 10"
        )
        self.numero_entry.grid(row=1, column=1, sticky="ew")

        # Boutons d'action
        buttons_frame = ctk.CTkFrame(form_card, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=40, pady=30)

        action_buttons = [
            ("💾 SAUVEGARDER", self.save_player, self.colors["success"]),
            ("🔄 RÉINITIALISER", self.clear_form, self.colors["warning"]),
            ("❌ ANNULER", self.cancel_edit, self.colors["danger"])
        ]

        for i, (text, command, color) in enumerate(action_buttons):
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                command=command,
                fg_color=color,
                hover_color=self.adjust_brightness(color, -20),
                font=("Segoe UI", 14, "bold"),
                height=50,
                corner_radius=10
            )
            btn.grid(row=0, column=i, padx=5, sticky="ew")
            buttons_frame.grid_columnconfigure(i, weight=1)

    def create_photo_section(self, parent):
        photo_container = ctk.CTkFrame(parent, fg_color="transparent")
        photo_container.pack(pady=20)

        # Cadre de la photo
        self.photo_frame = ctk.CTkFrame(
            photo_container,
            fg_color="#2c3e50",
            width=150,
            height=150,
            corner_radius=20,
            border_color=self.colors["primary"],
            border_width=3
        )
        self.photo_frame.pack()
        self.photo_frame.pack_propagate(False)

        self.photo_label = ctk.CTkLabel(
            self.photo_frame,
            text="📷\nCliquer pour\najouter une photo",
            font=("Segoe UI", 12),
            text_color="#bdc3c7",
            wraplength=120
        )
        self.photo_label.pack(expand=True)
        self.photo_label.bind("<Button-1>", lambda e: self.upload_image())

        # Bouton de téléchargement
        ctk.CTkButton(
            photo_container,
            text="📁 CHOISIR UNE PHOTO",
            command=self.upload_image,
            fg_color=self.colors["primary"],
            hover_color="#2980b9",
            height=40,
            font=("Segoe UI", 12, "bold"),
            corner_radius=10
        ).pack(pady=10)

    def create_modern_field(self, parent, label, row):
        ctk.CTkLabel(
            parent,
            text=label,
            font=("Segoe UI", 14, "bold"),
            text_color="#bdc3c7"
        ).grid(row=row, column=0, sticky="w", pady=(15, 5))

        entry = ctk.CTkEntry(
            parent,
            height=45,
            fg_color="#2c3e50",
            border_color=self.colors["primary"],
            border_width=2,
            font=("Segoe UI", 14),
            corner_radius=10
        )
        entry.grid(row=row, column=1, sticky="ew", pady=(15, 5), padx=(20, 0))

        parent.grid_columnconfigure(1, weight=1)
        return entry

    def create_list_tab(self):
        # Configuration de la grille pour l'onglet liste
        self.list_tab.grid_columnconfigure(0, weight=1)
        self.list_tab.grid_rowconfigure(1, weight=1)

        # Barre de recherche et filtres
        search_frame = ctk.CTkFrame(self.list_tab, fg_color="transparent")
        search_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        # Barre de recherche
        search_container = ctk.CTkFrame(search_frame, fg_color="#2c3e50", corner_radius=10)
        search_container.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", self.filter_players)

        search_entry = ctk.CTkEntry(
            search_container,
            textvariable=self.search_var,
            height=45,
            fg_color="transparent",
            border_width=0,
            font=("Segoe UI", 14),
            placeholder_text="🔍 Rechercher un joueur..."
        )
        search_entry.pack(fill="x", padx=15, pady=10)

        # Filtre par poste
        filter_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        filter_frame.pack(side="right")

        ctk.CTkLabel(
            filter_frame,
            text="Filtrer par poste:",
            font=("Segoe UI", 12, "bold"),
            text_color="#bdc3c7"
        ).pack(side="left", padx=(0, 10))

        self.filter_var = ctk.StringVar(value="Tous")
        filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            variable=self.filter_var,
            values=["Tous", "Gardien", "Défenseur", "Milieu", "Attaquant"],
            command=self.filter_players,
            fg_color="#2c3e50",
            button_color=self.colors["primary"],
            height=45,
            width=120
        )
        filter_menu.pack(side="left")

        # Liste des joueurs
        self.players_container = ctk.CTkScrollableFrame(
            self.list_tab,
            fg_color="transparent"
        )
        self.players_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        self.refresh_players_list()

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Choisir une photo de profil",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Tous les fichiers", "*.*")
            ]
        )
        if file_path:
            self.selected_image_path = file_path
            # Afficher l'aperçu
            try:
                img = Image.open(file_path)
                img = ImageOps.fit(img, (144, 144), method=Image.Resampling.LANCZOS)
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(144, 144))
                self.photo_label.configure(image=photo, text="")
                self.photo_label.image = photo
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger l'image: {e}")

    def save_player(self):
        nom = self.nom_entry.get().strip()
        tel = self.tel_entry.get().strip()
        date = self.date_entry.get().strip()
        poste = self.poste_var.get()
        numero = self.numero_entry.get().strip()

        if not all([nom, tel, date, numero]):
            messagebox.showerror("Erreur", "❌ Veuillez remplir tous les champs obligatoires!")
            return

        # Copier l'image si sélectionnée
        image_path = ""
        if self.selected_image_path:
            ext = os.path.splitext(self.selected_image_path)[1]
            image_path = os.path.join(self.images_dir, f"player_{self.next_id}{ext}")
            try:
                shutil.copy2(self.selected_image_path, image_path)
            except Exception:
                image_path = ""

        if self.current_edit_id:
            # Mode édition
            player = next((p for p in self.players if p.id == self.current_edit_id), None)
            if player:
                # Supprimer l'ancienne image si une nouvelle est sélectionnée
                if self.selected_image_path and player.image_path and os.path.exists(player.image_path):
                    try:
                        os.remove(player.image_path)
                    except Exception:
                        pass

                player.nom_complet = nom
                player.telephone = tel
                player.image_path = image_path if self.selected_image_path else player.image_path
                player.date_naissance = date
                player.poste = poste
                player.numero = numero

                messagebox.showinfo("Succès", f"✅ Joueur {nom} modifié avec succès!")
        else:
            # Mode ajout
            player = Player(self.next_id, nom, tel, image_path, date, poste, numero)
            self.players.append(player)
            self.next_id += 1
            messagebox.showinfo("Succès", f"✅ Joueur {nom} ajouté avec succès!")

        self.save_data()
        self.refresh_players_list()
        self.clear_form()
        self.tabview.set("📋 LISTE")

    def clear_form(self):
        try:
            self.nom_entry.delete(0, 'end')
            self.tel_entry.delete(0, 'end')
            self.date_entry.delete(0, 'end')
            self.numero_entry.delete(0, 'end')
        except Exception:
            pass
        self.poste_var.set("Attaquant")
        self.selected_image_path = None
        self.current_edit_id = None
        self.photo_label.configure(image=None, text="📷\nCliquer pour\najouter une photo")

    def cancel_edit(self):
        self.clear_form()
        self.tabview.set("📋 LISTE")

    def edit_player(self, player):
        self.current_edit_id = player.id
        # Vider d'abord
        try:
            self.nom_entry.delete(0, 'end')
            self.tel_entry.delete(0, 'end')
            self.date_entry.delete(0, 'end')
            self.numero_entry.delete(0, 'end')
        except Exception:
            pass

        self.nom_entry.insert(0, player.nom_complet)
        self.tel_entry.insert(0, player.telephone)
        self.date_entry.insert(0, player.date_naissance)
        self.poste_var.set(player.poste)
        self.numero_entry.insert(0, player.numero)

        if player.image_path and os.path.exists(player.image_path):
            try:
                img = Image.open(player.image_path)
                img = ImageOps.fit(img, (144, 144), method=Image.Resampling.LANCZOS)
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(144, 144))
                self.photo_label.configure(image=photo, text="")
                self.photo_label.image = photo
                self.selected_image_path = player.image_path
            except Exception:
                pass

        self.tabview.set("➕ AJOUTER")
        self.nom_entry.focus()

    def refresh_players_list(self):
        for widget in self.players_container.winfo_children():
            widget.destroy()

        self.stats_label.configure(text=f"Joueurs: {len(self.players)}")

        if not self.players:
            empty_frame = ctk.CTkFrame(
                self.players_container,
                fg_color="#1e1e1e",
                corner_radius=15,
                height=200
            )
            empty_frame.pack(fill="x", pady=10)
            empty_frame.pack_propagate(False)

            ctk.CTkLabel(
                empty_frame,
                text="👥 Aucun joueur dans l'équipe",
                font=("Segoe UI", 18, "bold"),
                text_color="#7f8c8d"
            ).pack(expand=True)

            ctk.CTkLabel(
                empty_frame,
                text="Commencez par ajouter votre premier joueur!",
                font=("Segoe UI", 14),
                text_color="#95a5a6"
            ).pack(pady=(0, 20))
            return

        for player in self.players:
            self.create_player_card(player)

    def create_player_card(self, player):
        card = ctk.CTkFrame(
            self.players_container,
            fg_color="#1e1e1e",
            corner_radius=15,
            border_color="#34495e",
            border_width=2
        )
        card.pack(fill="x", pady=8)

        # Contenu de la carte
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)

        # Photo et informations
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)

        # Photo
        if player.image_path and os.path.exists(player.image_path):
            try:
                img = Image.open(player.image_path)
                img = img.resize((60, 60), Image.Resampling.LANCZOS)
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(60, 60))
                img_label = ctk.CTkLabel(info_frame, image=photo, text="")
                img_label.image = photo
                img_label.pack(side="left", padx=(0, 15))
            except Exception:
                self.create_default_avatar(info_frame, player.nom_complet[0])
        else:
            self.create_default_avatar(info_frame, player.nom_complet[0])

        # Détails du joueur
        details_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        details_frame.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            details_frame,
            text=f"{player.nom_complet}",
            font=("Segoe UI", 16, "bold"),
            anchor="w"
        ).pack(anchor="w")

        info_text = f"#{player.numero} | {player.poste} | 📞 {player.telephone}"
        ctk.CTkLabel(
            details_frame,
            text=info_text,
            font=("Segoe UI", 12),
            text_color="#bdc3c7",
            anchor="w"
        ).pack(anchor="w", pady=(2, 0))

        # Boutons d'action
        actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        actions_frame.pack(side="right")

        ctk.CTkButton(
            actions_frame,
            text="👁️ Voir",
            command=lambda p=player: self.show_player_details(p),
            fg_color=self.colors["primary"],
            hover_color="#2980b9",
            width=80,
            height=35
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            actions_frame,
            text="✏️ Modifier",
            command=lambda p=player: self.edit_player(p),
            fg_color=self.colors["warning"],
            hover_color="#e67e22",
            width=80,
            height=35
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            actions_frame,
            text="🗑️ Supprimer",
            command=lambda p=player: self.delete_player(p),
            fg_color=self.colors["danger"],
            hover_color="#c0392b",
            width=80,
            height=35
        ).pack(side="left", padx=5)

    def create_default_avatar(self, parent, initial):
        avatar = ctk.CTkFrame(
            parent,
            fg_color="#3498db",
            width=60,
            height=60,
            corner_radius=30
        )
        avatar.pack(side="left", padx=(0, 15))
        avatar.pack_propagate(False)

        ctk.CTkLabel(
            avatar,
            text=initial.upper(),
            font=("Segoe UI", 18, "bold"),
            text_color="white"
        ).pack(expand=True)

    def show_player_details(self, player):
        ModernPlayerModal(self, player)

    def delete_player(self, player):
        if messagebox.askyesno(
            "Confirmation de suppression",
            f"Êtes-vous sûr de vouloir supprimer le joueur:\n\n{player.nom_complet} - #{player.numero} ?",
            icon="warning"
        ):
            if player.image_path and os.path.exists(player.image_path):
                try:
                    os.remove(player.image_path)
                except Exception:
                    pass

            self.players.remove(player)
            self.save_data()
            self.refresh_players_list()
            messagebox.showinfo("Succès", "✅ Joueur supprimé avec succès!")

    def filter_players(self, *args):
        # Filtrer selon search_var et filter_var
        query = self.search_var.get().strip().lower() if hasattr(self, "search_var") else ""
        poste = self.filter_var.get() if hasattr(self, "filter_var") else "Tous"

        def matches(p):
            if query and query not in p.nom_complet.lower() and query not in p.telephone.lower():
                return False
            if poste != "Tous" and p.poste != poste:
                return False
            return True

        # rebuild list
        for widget in self.players_container.winfo_children():
            widget.destroy()

        filtered = [p for p in self.players if matches(p)]
        if not filtered:
            empty_frame = ctk.CTkFrame(
                self.players_container,
                fg_color="#1e1e1e",
                corner_radius=15,
                height=120
            )
            empty_frame.pack(fill="x", pady=10)
            empty_frame.pack_propagate(False)
            ctk.CTkLabel(empty_frame, text="Aucun joueur trouvé.", font=("Segoe UI", 14), text_color="#7f8c8d").pack(expand=True)
            return

        for p in filtered:
            self.create_player_card(p)

    def navigate(self, page):
    # D'abord, détruire tout le contenu actuel
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if page == "dashboard":
            self.show_dashboard()
        elif page == "players":
            # Recréer les onglets à chaque fois qu'on y va
            self.create_main_tabs(self.content_frame)
            self.tabview.set("LISTE")  # Maintenant c'est sûr
        elif page == "stats":
            self.show_stats_placeholder()
        elif page == "settings":
            self.show_settings_placeholder()

    def adjust_brightness(self, color, amount):
        """Ajuste la luminosité d'une couleur hexadécimale (simple)"""
        try:
            color = color.lstrip("#")
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            def clamp(v): return max(0, min(255, v))
            r = clamp(r + amount)
            g = clamp(g + amount)
            b = clamp(b + amount)
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return color

    def save_data(self):
        data = {
            'next_id': self.next_id,
            'players': [
                {
                    'id': p.id,
                    'nom_complet': p.nom_complet,
                    'telephone': p.telephone,
                    'image_path': p.image_path,
                    'date_naissance': p.date_naissance,
                    'poste': p.poste,
                    'numero': p.numero
                }
                for p in self.players
            ]
        }
        try:
            with open('team_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")

    def load_data(self):
        if os.path.exists('team_data.json'):
            try:
                with open('team_data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.next_id = data.get('next_id', 1)
                    for p_data in data.get('players', []):
                        player = Player(
                            p_data.get('id'),
                            p_data.get('nom_complet'),
                            p_data.get('telephone'),
                            p_data.get('image_path'),
                            p_data.get('date_naissance'),
                            p_data.get('poste'),
                            p_data.get('numero')
                        )
                        self.players.append(player)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement: {e}")

if __name__ == "__main__":
    app = ModernTeamManagementSystem()
    app.mainloop()
