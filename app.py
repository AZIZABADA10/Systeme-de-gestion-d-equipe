import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json
import os
from datetime import datetime
import shutil

class Player:
    def __init__(self, id, nom_complet, telephone, image_path, date_naissance, poste, numero):
        self.id = id
        self.nom_complet = nom_complet
        self.telephone = telephone
        self.image_path = image_path
        self.date_naissance = date_naissance
        self.poste = poste
        self.numero = numero

class PlayerModal(ctk.CTkToplevel):
    def __init__(self, parent, player):
        super().__init__(parent)
        self.title("Détails du Joueur")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Configuration
        self.configure(fg_color="#1a1a1a")
        
        # Container principal
        main_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Photo du joueur
        if player.image_path and os.path.exists(player.image_path):
            img = Image.open(player.image_path)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
            img_label = ctk.CTkLabel(main_frame, image=photo, text="")
            img_label.pack(pady=20)
        
        # Informations
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        details = [
            ("Nom Complet:", player.nom_complet),
            ("Téléphone:", player.telephone),
            ("Date de Naissance:", player.date_naissance),
            ("Poste:", player.poste),
            ("Numéro:", player.numero)
        ]
        
        for label, value in details:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", pady=8)
            
            ctk.CTkLabel(
                row, 
                text=label, 
                font=("Helvetica", 14, "bold"),
                text_color="#888888"
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                row, 
                text=value, 
                font=("Helvetica", 16),
                text_color="#ffffff"
            ).pack(anchor="w", padx=10)
        
        # Bouton fermer
        ctk.CTkButton(
            main_frame,
            text="Fermer",
            command=self.destroy,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            font=("Helvetica", 14, "bold"),
            height=40
        ).pack(pady=20, padx=30, fill="x")

class TeamManagementSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Gestion d'Équipe")
        self.geometry("1200x700")
        
        # Configuration du thème
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.players = []
        self.next_id = 1
        self.selected_image_path = None
        
        # Créer le dossier pour les images
        self.images_dir = "player_images"
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
        
        self.load_data()
        self.create_ui()
        
    def create_ui(self):
        # Container principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Titre
        title_frame = ctk.CTkFrame(main_container, fg_color="#2b2b2b", height=80, corner_radius=10)
        title_frame.pack(fill="x", pady=(0, 10))
        title_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            title_frame,
            text="⚽ Gestion d'Équipe",
            font=("Helvetica", 32, "bold"),
            text_color="#3498db"
        ).pack(pady=20)
        
        # Frame principal divisé
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Panel gauche - Formulaire
        left_panel = ctk.CTkFrame(content_frame, fg_color="#2b2b2b", corner_radius=10)
        left_panel.pack(side="left", fill="both", padx=(0, 5), expand=True)
        
        self.create_form(left_panel)
        
        # Panel droit - Liste des joueurs
        right_panel = ctk.CTkFrame(content_frame, fg_color="#2b2b2b", corner_radius=10)
        right_panel.pack(side="right", fill="both", padx=(5, 0), expand=True)
        
        self.create_players_list(right_panel)
        
    def create_form(self, parent):
        # Titre du formulaire
        ctk.CTkLabel(
            parent,
            text="Ajouter un Joueur",
            font=("Helvetica", 24, "bold")
        ).pack(pady=20)
        
        # Frame scrollable pour le formulaire
        form_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Photo de profil
        self.photo_frame = ctk.CTkFrame(form_frame, fg_color="#1a1a1a", height=150, corner_radius=10)
        self.photo_frame.pack(fill="x", pady=10)
        
        self.photo_label = ctk.CTkLabel(
            self.photo_frame,
            text="📷 Aucune photo",
            font=("Helvetica", 14),
            text_color="#888888"
        )
        self.photo_label.pack(pady=55)
        
        ctk.CTkButton(
            form_frame,
            text="📁 Choisir une photo",
            command=self.upload_image,
            fg_color="#3498db",
            hover_color="#2980b9",
            height=35
        ).pack(fill="x", pady=5)
        
        # Champs du formulaire
        self.nom_entry = self.create_field(form_frame, "Nom Complet")
        self.tel_entry = self.create_field(form_frame, "Téléphone")
        self.date_entry = self.create_field(form_frame, "Date de Naissance (JJ/MM/AAAA)")
        
        # Poste de jeu
        ctk.CTkLabel(form_frame, text="Poste de Jeu", font=("Helvetica", 12)).pack(anchor="w", pady=(10, 5))
        self.poste_var = ctk.StringVar(value="Attaquant")
        postes = ["Gardien", "Défenseur", "Milieu", "Attaquant"]
        self.poste_menu = ctk.CTkOptionMenu(
            form_frame,
            variable=self.poste_var,
            values=postes,
            fg_color="#1a1a1a",
            button_color="#3498db",
            button_hover_color="#2980b9"
        )
        self.poste_menu.pack(fill="x", pady=5)
        
        self.numero_entry = self.create_field(form_frame, "Numéro de Maillot")
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(
            buttons_frame,
            text="✓ Ajouter Joueur",
            command=self.add_player,
            fg_color="#27ae60",
            hover_color="#229954",
            height=45,
            font=("Helvetica", 14, "bold")
        ).pack(fill="x", pady=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="🔄 Réinitialiser",
            command=self.clear_form,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            height=40
        ).pack(fill="x", pady=5)
    
    def create_field(self, parent, label_text):
        ctk.CTkLabel(parent, text=label_text, font=("Helvetica", 12)).pack(anchor="w", pady=(10, 5))
        entry = ctk.CTkEntry(parent, height=35, fg_color="#1a1a1a", border_color="#3498db")
        entry.pack(fill="x", pady=5)
        return entry
    
    def create_players_list(self, parent):
        # Titre
        ctk.CTkLabel(
            parent,
            text="Liste des Joueurs",
            font=("Helvetica", 24, "bold")
        ).pack(pady=20)
        
        # Frame scrollable pour la liste
        self.players_frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.players_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.refresh_players_list()
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Choisir une photo",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.selected_image_path = file_path
            # Afficher l'aperçu
            img = Image.open(file_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ctk.CTkImage(light_image=img, dark_image=img, size=(100, 100))
            self.photo_label.configure(image=photo, text="")
            self.photo_label.image = photo
    
    def add_player(self):
        nom = self.nom_entry.get().strip()
        tel = self.tel_entry.get().strip()
        date = self.date_entry.get().strip()
        poste = self.poste_var.get()
        numero = self.numero_entry.get().strip()
        
        if not all([nom, tel, date, numero]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs!")
            return
        
        # Copier l'image si sélectionnée
        image_path = ""
        if self.selected_image_path:
            ext = os.path.splitext(self.selected_image_path)[1]
            image_path = os.path.join(self.images_dir, f"player_{self.next_id}{ext}")
            shutil.copy2(self.selected_image_path, image_path)
        
        player = Player(self.next_id, nom, tel, image_path, date, poste, numero)
        self.players.append(player)
        self.next_id += 1
        
        self.save_data()
        self.refresh_players_list()
        self.clear_form()
        
        messagebox.showinfo("Succès", f"Joueur {nom} ajouté avec succès!")
    
    def clear_form(self):
        self.nom_entry.delete(0, 'end')
        self.tel_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.numero_entry.delete(0, 'end')
        self.poste_var.set("Attaquant")
        self.selected_image_path = None
        self.photo_label.configure(image=None, text="📷 Aucune photo")
    
    def refresh_players_list(self):
        for widget in self.players_frame.winfo_children():
            widget.destroy()
        
        if not self.players:
            ctk.CTkLabel(
                self.players_frame,
                text="Aucun joueur dans l'équipe",
                font=("Helvetica", 14),
                text_color="#888888"
            ).pack(pady=50)
            return
        
        for player in self.players:
            player_card = ctk.CTkFrame(self.players_frame, fg_color="#1a1a1a", corner_radius=10)
            player_card.pack(fill="x", pady=5)
            
            # Frame cliquable
            click_frame = ctk.CTkFrame(player_card, fg_color="transparent")
            click_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            click_frame.bind("<Button-1>", lambda e, p=player: self.show_player_details(p))
            
            # Photo miniature
            if player.image_path and os.path.exists(player.image_path):
                img = Image.open(player.image_path)
                img = img.resize((60, 60), Image.Resampling.LANCZOS)
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(60, 60))
                img_label = ctk.CTkLabel(click_frame, image=photo, text="")
                img_label.image = photo
                img_label.pack(side="left", padx=10)
                img_label.bind("<Button-1>", lambda e, p=player: self.show_player_details(p))
            
            # Informations
            info_frame = ctk.CTkFrame(click_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True)
            info_frame.bind("<Button-1>", lambda e, p=player: self.show_player_details(p))
            
            name_label = ctk.CTkLabel(
                info_frame,
                text=f"{player.nom_complet} - #{player.numero}",
                font=("Helvetica", 16, "bold"),
                anchor="w"
            )
            name_label.pack(anchor="w")
            name_label.bind("<Button-1>", lambda e, p=player: self.show_player_details(p))
            
            poste_label = ctk.CTkLabel(
                info_frame,
                text=f"{player.poste} | {player.telephone}",
                font=("Helvetica", 12),
                text_color="#888888",
                anchor="w"
            )
            poste_label.pack(anchor="w")
            poste_label.bind("<Button-1>", lambda e, p=player: self.show_player_details(p))
            
            # Boutons d'action
            buttons_frame = ctk.CTkFrame(player_card, fg_color="transparent")
            buttons_frame.pack(side="right", padx=10)
            
            ctk.CTkButton(
                buttons_frame,
                text="🗑️",
                width=40,
                command=lambda p=player: self.delete_player(p),
                fg_color="#e74c3c",
                hover_color="#c0392b"
            ).pack(side="right", padx=2)
    
    def show_player_details(self, player):
        PlayerModal(self, player)
    
    def delete_player(self, player):
        if messagebox.askyesno("Confirmation", f"Supprimer {player.nom_complet}?"):
            if player.image_path and os.path.exists(player.image_path):
                os.remove(player.image_path)
            self.players.remove(player)
            self.save_data()
            self.refresh_players_list()
            messagebox.showinfo("Succès", "Joueur supprimé!")
    
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
        with open('team_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_data(self):
        if os.path.exists('team_data.json'):
            try:
                with open('team_data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.next_id = data.get('next_id', 1)
                    for p_data in data.get('players', []):
                        player = Player(
                            p_data['id'],
                            p_data['nom_complet'],
                            p_data['telephone'],
                            p_data['image_path'],
                            p_data['date_naissance'],
                            p_data['poste'],
                            p_data['numero']
                        )
                        self.players.append(player)
            except Exception as e:
                print(f"Erreur de chargement: {e}")

if __name__ == "__main__":
    app = TeamManagementSystem()
    app.mainloop()