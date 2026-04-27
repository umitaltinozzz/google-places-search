import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import time
import pandas as pd
import os
from threading import Thread
from datetime import datetime

class GooglePlacesUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Places İşletme Arama")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Ana frame
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Giriş alanları
        ttk.Label(main_frame, text="Google Places API Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.api_key_var = tk.StringVar(value="")
        ttk.Entry(main_frame, width=50, textvariable=self.api_key_var).grid(row=0, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(main_frame, text="Anahtar Kelimeler (her satıra bir tane):").grid(row=1, column=0, sticky=tk.W + tk.N, pady=5)
        self.keywords_text = scrolledtext.ScrolledText(main_frame, width=40, height=5)
        self.keywords_text.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)
        self.keywords_text.insert(tk.END, "restoran\nkafe\nbar\npastane")
        
        ttk.Label(main_frame, text="İlçeler (her satıra bir tane):").grid(row=2, column=0, sticky=tk.W + tk.N, pady=5)
        self.districts_text = scrolledtext.ScrolledText(main_frame, width=40, height=5)
        self.districts_text.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=5)
        self.districts_text.insert(tk.END, "Kadıköy\nBeşiktaş\nŞişli\nÜsküdar")
        
        ttk.Label(main_frame, text="Maksimum Puan:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.max_rating_var = tk.StringVar(value="4.0")
        ttk.Entry(main_frame, width=10, textvariable=self.max_rating_var).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Arama butonu
        self.search_button = ttk.Button(main_frame, text="Aramayı Başlat", command=self.start_search)
        self.search_button.grid(row=4, column=0, columnspan=3, pady=10)
        
        # İlerleme çubuğu
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress.grid(row=5, column=0, columnspan=3, sticky=tk.EW, pady=5)
        
        # Durum etiketi
        self.status_var = tk.StringVar(value="Hazır")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Arama Geçmişi Frame
        self.history_frame = ttk.LabelFrame(main_frame, text="Arama Geçmişi")
        self.history_frame.grid(row=7, column=0, columnspan=3, sticky=tk.NSEW, pady=10)
        main_frame.grid_rowconfigure(7, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        
        # Arama Geçmişi Tablosu
        self.history_tree = ttk.Treeview(self.history_frame, columns=("time", "keywords", "districts", "max_rating", "results", "file"), show="headings")
        self.history_tree.heading("time", text="Zaman")
        self.history_tree.heading("keywords", text="Anahtar Kelimeler")
        self.history_tree.heading("districts", text="İlçeler")
        self.history_tree.heading("max_rating", text="Maks. Puan")
        self.history_tree.heading("results", text="Sonuç Sayısı")
        self.history_tree.heading("file", text="Dosya")
        
        # Sütun genişlikleri
        self.history_tree.column("time", width=120)
        self.history_tree.column("keywords", width=150)
        self.history_tree.column("districts", width=150)
        self.history_tree.column("max_rating", width=80)
        self.history_tree.column("results", width=80)
        self.history_tree.column("file", width=200)
        
        # Geçmiş tablosu için scrollbar
        history_scrollbar = ttk.Scrollbar(self.history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        history_scrollbar_x = ttk.Scrollbar(self.history_frame, orient=tk.HORIZONTAL, command=self.history_tree.xview)
        self.history_tree.configure(yscroll=history_scrollbar.set, xscroll=history_scrollbar_x.set)
        
        # Geçmiş tablosunu yerleştirme
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        history_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.history_tree.pack(fill=tk.BOTH, expand=True)
        
        # Sonuç gösterme butonu
        self.view_button = ttk.Button(main_frame, text="Seçili Aramayı Göster", command=self.show_selected_search)
        self.view_button.grid(row=8, column=0, columnspan=3, pady=5)
        
        # Sonuç tablosu
        self.result_frame = ttk.LabelFrame(main_frame, text="Sonuçlar")
        self.result_frame.grid(row=9, column=0, columnspan=3, sticky=tk.NSEW, pady=10)
        main_frame.grid_rowconfigure(9, weight=2)
        
        # Treeview (tablo) oluşturma
        self.tree = ttk.Treeview(self.result_frame, columns=("name", "rating", "address", "reviews", "lat", "lng", "query"), show="headings")
        self.tree.heading("name", text="İşletme Adı")
        self.tree.heading("rating", text="Puan")
        self.tree.heading("address", text="Adres")
        self.tree.heading("reviews", text="Yorum Sayısı")
        self.tree.heading("lat", text="Enlem")
        self.tree.heading("lng", text="Boylam")
        self.tree.heading("query", text="Arama Kelimesi")
        
        # Sütun genişlikleri
        self.tree.column("name", width=150)
        self.tree.column("rating", width=50)
        self.tree.column("address", width=200)
        self.tree.column("reviews", width=80)
        self.tree.column("lat", width=80)
        self.tree.column("lng", width=80)
        self.tree.column("query", width=100)
        
        # Scrollbar ekleme
        scrollbar = ttk.Scrollbar(self.result_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self.result_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=scrollbar.set, xscroll=scrollbar_x.set)
        
        # Treeview ve scrollbar'ları yerleştirme
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Veri saklama listesi
        self.results = []
        
        # Arama geçmişi
        self.search_history = []
    
    def search_places(self, keyword, district, max_rating):
        """Google Places API'den işletme arar"""
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        query = f"{keyword} in {district}, Istanbul, Turkey"
        params = {
            "query": query,
            "key": self.api_key_var.get()
        }
        
        places = []
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if data["status"] == "OK" and "results" in data:
                for place in data["results"]:
                    rating = place.get("rating", 0)
                    if rating <= float(max_rating):
                        place_data = {
                            "name": place.get("name", ""),
                            "rating": rating,
                            "formatted_address": place.get("formatted_address", ""),
                            "user_ratings_total": place.get("user_ratings_total", 0),
                            "lat": place.get("geometry", {}).get("location", {}).get("lat", ""),
                            "lng": place.get("geometry", {}).get("location", {}).get("lng", ""),
                            "query": keyword
                        }
                        places.append(place_data)
                        
                # Next page token işleme (istenirse eklenebilir)
                # if "next_page_token" in data:
                #     time.sleep(2)  # Token hazır olana kadar bekleme
                #     # Sonraki sayfa işlemleri...
            
        except Exception as e:
            print(f"Hata: {e}")
        
        return places
    
    def update_progress(self, current, total):
        """İlerleme çubuğunu günceller"""
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.root.update_idletasks()
    
    def update_status(self, text):
        """Durum metnini günceller"""
        self.status_var.set(text)
        self.root.update_idletasks()
    
    def add_to_table(self, places):
        """Sonuçları tabloya ekler"""
        for place in places:
            self.tree.insert("", tk.END, values=(
                place["name"],
                place["rating"],
                place["formatted_address"],
                place["user_ratings_total"],
                place["lat"],
                place["lng"],
                place["query"]
            ))
            self.results.append(place)
    
    def save_to_csv(self, keywords, districts, max_rating):
        """Sonuçları CSV dosyasına kaydeder ve arama geçmişine ekler"""
        if not self.results:
            return None
        
        try:
            # Benzersiz dosya adı oluştur
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"arama_{timestamp}.csv"
            
            # DataFrame'e çevir ve kaydet
            df = pd.DataFrame(self.results)
            df.to_csv(filename, index=False, encoding="utf-8-sig")
            
            # Arama geçmişi için bilgiler
            search_info = {
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "keywords": ", ".join(keywords),
                "districts": ", ".join(districts),
                "max_rating": max_rating,
                "results_count": len(self.results),
                "filename": filename,
                "results": self.results.copy()
            }
            
            # Geçmişe ekle
            self.search_history.append(search_info)
            
            # Geçmiş tablosunu güncelle
            self.update_history_table()
            
            messagebox.showinfo("Bilgi", f"Veriler başarıyla kaydedildi: {os.path.abspath(filename)}")
            return filename
        except Exception as e:
            messagebox.showerror("Hata", f"CSV kaydetme hatası: {e}")
            return None
    
    def update_history_table(self):
        """Arama geçmişi tablosunu günceller"""
        # Önce tabloyu temizle
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Geçmiş kayıtlarını ekle
        for search in self.search_history:
            self.history_tree.insert("", tk.END, values=(
                search["time"],
                search["keywords"],
                search["districts"],
                search["max_rating"],
                search["results_count"],
                search["filename"]
            ))
    
    def show_selected_search(self):
        """Seçili aramayı sonuç tablosunda gösterir"""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showinfo("Bilgi", "Lütfen geçmişten bir arama seçin")
            return
        
        # Seçili aramanın indeksini bul
        selected_idx = self.history_tree.index(selection[0])
        
        if 0 <= selected_idx < len(self.search_history):
            # Tabloyu temizle
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Seçili arama sonuçlarını tabloya ekle
            for place in self.search_history[selected_idx]["results"]:
                self.tree.insert("", tk.END, values=(
                    place["name"],
                    place["rating"],
                    place["formatted_address"],
                    place["user_ratings_total"],
                    place["lat"],
                    place["lng"],
                    place["query"]
                ))
            
            # Durum çubuğunu güncelle
            search_info = self.search_history[selected_idx]
            self.update_status(f"Gösterilen arama: {search_info['keywords']} in {search_info['districts']} ({search_info['results_count']} sonuç)")
    
    def search_thread(self):
        """Arama işlemini ayrı bir thread'de yapar"""
        # Temizlik
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.results = []
        
        # Girişleri al
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showerror("Hata", "API Key boş olamaz!")
            self.search_button.config(state=tk.NORMAL)
            return
        
        keywords = [k.strip() for k in self.keywords_text.get("1.0", tk.END).split("\n") if k.strip()]
        districts = [d.strip() for d in self.districts_text.get("1.0", tk.END).split("\n") if d.strip()]
        
        try:
            max_rating = float(self.max_rating_var.get())
        except ValueError:
            messagebox.showerror("Hata", "Maksimum puan sayısal bir değer olmalıdır!")
            self.search_button.config(state=tk.NORMAL)
            return
        
        if not keywords or not districts:
            messagebox.showerror("Hata", "Anahtar kelimeler ve ilçeler boş olamaz!")
            self.search_button.config(state=tk.NORMAL)
            return
        
        # Toplam işlem sayısı
        total_operations = len(keywords) * len(districts)
        current_operation = 0
        
        # Her anahtar kelime ve ilçe kombinasyonu için arama yap
        for keyword in keywords:
            for district in districts:
                self.update_status(f"Aranıyor: {keyword} in {district}")
                places = self.search_places(keyword, district, max_rating)
                self.add_to_table(places)
                
                current_operation += 1
                self.update_progress(current_operation, total_operations)
                
                # Rate limit için bekleme
                time.sleep(1)
        
        # İşlem tamamlandı
        self.update_status(f"Arama tamamlandı. {len(self.results)} sonuç bulundu.")
        
        # Sonuçları kaydet ve geçmişe ekle
        filename = self.save_to_csv(keywords, districts, max_rating)
        
        # Geçmiş tablosunu güncelle
        self.update_history_table()
        
        self.search_button.config(state=tk.NORMAL)
    
    def start_search(self):
        """Arama işlemini başlatır"""
        self.search_button.config(state=tk.DISABLED)
        self.update_status("Hazırlanıyor...")
        self.progress_var.set(0)
        
        # Aramayı ayrı bir thread'de başlat
        search_thread = Thread(target=self.search_thread)
        search_thread.daemon = True
        search_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = GooglePlacesUygulamasi(root)
    root.mainloop() 