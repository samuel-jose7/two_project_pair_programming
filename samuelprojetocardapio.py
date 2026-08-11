import json
import os
import subprocess
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

PALETA_CLARA = {
    "fundo": "#0e0b6d",
    "painel": "#ffffff",
    "texto": "#212529",
    "subtexto": "#6c757d",
    "primaria": "#c0392b",
    "verde": "#27ae60",
    "vermelho": "#e74c3c",
    "amarelo": "#f39c12",
    "borda": "#e5e7eb",
}

PALETA_ESCURA = {
    "fundo": "#121212",
    "painel": "#1e1e2e",
    "texto": "#ffffff",
    "subtexto": "#a1a1aa",
    "primaria": "#e74c3c",
    "verde": "#2ecc71",
    "vermelho": "#ef4444",
    "amarelo": "#f1c40f",
    "borda": "#3f3f46",
}

cores = PALETA_CLARA
modo_escuro = False

CARDAPIO = {
    "🥖 Entradas & Antipasti": [
        {
            "id": 101,
            "nome": "Bruschetta Pomodoro e Basilico",
            "preco": 24.90,
            "desc": "Fatias de pão italiano tostado, tomates frescos picados, alho, manjericão e azeite extravirgem.",
        },
        {
            "id": 102,
            "nome": "Carpaccio di Manzo",
            "preco": 38.90,
            "desc": "Lâminas finas de carne bovina, molho de alcaparras, lascas de parmesão e rúcula fresca.",
        },
        {
            "id": 103,
            "nome": "Arancini al Formaggio",
            "preco": 29.90,
            "desc": "Bolinhos de risoto crocantes recheados com queijo muçarela derretido (6 unidades).",
        },
        {
            "id": 104,
            "nome": "Polpette al Sugo",
            "preco": 32.00,
            "desc": "Alpôndegas artesanais servidas em molho pomodoro rústico com bastante queijo parmesão ralado.",
        },
        {
            "id": 105,
            "nome": "Focaccia Alecrim e Sal Grosso",
            "preco": 22.00,
            "desc": "Massa de focaccia artesanal assada com azeite de oliva, alecrim fresco e flor de sal.",
        },
    ],
    "🍝 Massas Tradicionais": [
        {
            "id": 201,
            "nome": "Spaghetti alla Carbonara",
            "preco": 48.90,
            "desc": "Massa italiana com guanciale, gemas de ovos frescas, queijo Pecorino Romano e pimenta-do-reino.",
        },
        {
            "id": 202,
            "nome": "Fettuccine Alfredo com Tiras de Mignon",
            "preco": 54.90,
            "desc": "Fettuccine artesanal envolto em molho cremoso de manteiga, parmesão e suculentas tiras de filet mignon.",
        },
        {
            "id": 203,
            "nome": "Penne all'Arrabbiata",
            "preco": 42.90,
            "desc": "Penne ao molho de tomate italiano temperado com pimenta calabresa, alho e azeite extravirgem.",
        },
        {
            "id": 204,
            "nome": "Lasagna alla Bolognese",
            "preco": 52.00,
            "desc": "Camadas de massa fresca intercaladas com ragù de carne moída, molho bechamel e muçarela gratinada.",
        },
        {
            "id": 205,
            "nome": "Tagliatelle al Funghi Porcini",
            "preco": 56.90,
            "desc": "Tagliatelle ao molho cremoso de cogumelos Funghi Porcini, alho-poró e toque de azeite trufado.",
        },
        {
            "id": 206,
            "nome": "Spaghetti al Pomodoro e Basílico",
            "preco": 39.90,
            "desc": "O clássico spaghetti ao molho de tomate pelado italiano artesanal com manjericão fresco.",
        },
    ],
    "🥟 Massas Recheadas & Gnocchi": [
        {
            "id": 301,
            "nome": "Ravioli de Ricota e Espinafre",
            "preco": 46.90,
            "desc": "Ravioli artesanal recheado com ricota fresca e espinafre ao molho de manteiga e sálvia.",
        },
        {
            "id": 302,
            "nome": "Gnocchi al Pesto Genovese",
            "preco": 45.90,
            "desc": "Nhoque artesanal de batata ao tradicional molho pesto de manjericão, nozes, azeite e parmesão.",
        },
        {
            "id": 303,
            "nome": "Gnocchi 4 Formaggi Gratinado",
            "preco": 49.90,
            "desc": "Nhoque leve de batata ao molho aveludado de Parmesão, Gorgonzola, Provolone e Mozzarella.",
        },
        {
            "id": 304,
            "nome": "Rondelli de Presunto e Queijo",
            "preco": 44.00,
            "desc": "Massa recheada com presunto cozido e muçarela, coberta por molho rosê e gratinada no forno.",
        },
        {
            "id": 305,
            "nome": "Ravioli de Costela ao Ragu",
            "preco": 58.90,
            "desc": "Ravioli recheado com costela bovina desfiada lentamente, servido ao molho ragu rústico.",
        },
    ],
    "🍰 Sobremesas": [
        {
            "id": 401,
            "nome": "Tiramisù Tradicional",
            "preco": 26.90,
            "desc": "Clássico italiano com biscoitos savoiardi embebidos em café espresso, creme de mascarpone e cacau.",
        },
        {
            "id": 402,
            "nome": "Panna Cotta com Calda de Frutas Vermelhas",
            "preco": 22.90,
            "desc": "Sobremesa gelada à base de creme de leite fresco e fava de baunilha com coulis de frutas vermelhas.",
        },
        {
            "id": 403,
            "nome": "Cannoli Siciliani (2 un)",
            "preco": 24.90,
            "desc": "Massa crocante aromatizada com vinho marçala, recheada com creme de ricota doce e gotas de chocolate.",
        },
        {
            "id": 404,
            "nome": "Gelato Artigianale (2 bolas)",
            "preco": 18.90,
            "desc": "Sorvete artesanal estilo italiano. Sabores disponíveis: Pistache, Chocolate Belga ou Baunilha.",
        },
    ],
    "🍷 Bebidas & Vinhos": [
        {
            "id": 501,
            "nome": "Vinho Chianti DOCG (Taça)",
            "preco": 28.00,
            "desc": "Vinho tinto seco italiano proveniente da região da Toscana (Taça 150ml).",
        },
        {
            "id": 502,
            "nome": "Vinho Pinot Grigio (Taça)",
            "preco": 26.00,
            "desc": "Vinho branco seco refrescante e frutado (Taça 150ml).",
        },
        {
            "id": 503,
            "nome": "Aperol Spritz",
            "preco": 32.00,
            "desc": "Cocktail refrescante com Aperol, Prosecco, água com gás e fatia de laranja.",
        },
        {
            "id": 504,
            "nome": "Água San Pellegrino 500ml",
            "preco": 14.00,
            "desc": "Água mineral gaseificada italiana importada.",
        },
        {
            "id": 505,
            "nome": "Suco de Uva Integral 300ml",
            "preco": 10.50,
            "desc": "Suco de uva tinto 100% natural, sem adição de açúcares ou conservantes.",
        },
        {
            "id": 506,
            "nome": "Coca-Cola / Guaraná Lata 350ml",
            "preco": 7.00,
            "desc": "Lata gelada 350ml (Normal ou Zero).",
        },
        {
            "id": 507,
            "nome": "Espresso Italiano (Xícara)",
            "preco": 6.50,
            "desc": "Café espresso forte e encorpado com grãos selecionados.",
        },
    ],
}

qtd_variaveis = {}
cards_widgets = []
canvases = []


def calcular_total():
    total = 0.0
    for categoria, itens in CARDAPIO.items():
        for item in itens:
            qtd = qtd_variaveis[item["id"]].get()
            total += qtd * item["preco"]
    lbl_total_valor.config(text=f"R$ {total:.2f}")
    return total


def zerar_quantidades():
    for var in qtd_variaveis.values():
        var.set(0)
    calcular_total()


def finalizar_pedido_json():
    itens_pedido = []
    total_geral = 0.0

    for categoria, itens in CARDAPIO.items():
        for item in itens:
            qtd = qtd_variaveis[item["id"]].get()
            if qtd > 0:
                subtotal = qtd * item["preco"]
                total_geral += subtotal
                itens_pedido.append(
                    {
                        "item": item["nome"],
                        "categoria": categoria,
                        "quantidade": qtd,
                        "preco_unitario": item["preco"],
                        "subtotal": subtotal,
                    }
                )

    if not itens_pedido:
        messagebox.showwarning(
            "Carrinho Vazio", "Selecione pelo menos um item para finalizar!"
        )
        return

    dados_pedido = {
        "restaurante": "Trattoria & Pastificio Italiano",
        "data_pedido": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_pedido": total_geral,
        "itens": itens_pedido,
    }

    nome_arquivo = f"ticket_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    pasta_repositorio = os.path.join(os.getcwd(), "ticket")
    os.makedirs(pasta_repositorio, exist_ok=True)

    caminho_local_repo = os.path.join(pasta_repositorio, nome_arquivo)

    try:
        with open(caminho_local_repo, "w", encoding="utf-8") as f:
            json.dump(dados_pedido, f, indent=4, ensure_ascii=False)
    except Exception as e_repo:
        messagebox.showerror("Erro", f"Falha ao salvar no repositório local: {e_repo}")
        return

    caminho_copia_extra = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Arquivos JSON", "*.json")],
        initialfile=nome_arquivo,
        title="Salvar uma cópia extra do Pedido JSON (Opcional)",
    )

    if caminho_copia_extra:
        try:
            with open(caminho_copia_extra, "w", encoding="utf-8") as f_extra:
                json.dump(dados_pedido, f_extra, indent=4, ensure_ascii=False)
        except Exception as e_copia:
            print(f"Não foi possível salvar a cópia extra: {e_copia}")

    try:
        subprocess.run(["code", caminho_local_repo], shell=True)
        messagebox.showinfo(
            "Sucesso",
            f"Pedido armazenado no repositório em:\n'ticket/{nome_arquivo}'\ne aberto no VS Code!",
        )
    except Exception as ex_vscode:
        messagebox.showinfo(
            "Sucesso",
            f"Pedido salvo no repositório em:\n'ticket/{nome_arquivo}'",
        )

    zerar_quantidades()


def alternar_tema():
    global modo_escuro, cores
    modo_escuro = not modo_escuro
    cores = PALETA_ESCURA if modo_escuro else PALETA_CLARA

    janela.configure(bg=cores["fundo"])
    bar_topo.configure(bg=cores["fundo"])
    lbl_titulo_app.configure(bg=cores["fundo"], fg=cores["texto"])
    frame_rodape.configure(bg=cores["painel"])
    lbl_total_texto.configure(bg=cores["painel"], fg=cores["texto"])
    lbl_total_valor.configure(bg=cores["painel"], fg=cores["primaria"])

    btn_tema.config(text="☀️ Modo Claro" if modo_escuro else "🌙 Modo Escuro")

    style.configure("TNotebook", background=cores["fundo"], borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background=cores["painel"],
        foreground=cores["texto"],
        padding=[10, 5],
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", cores["primaria"])],
        foreground=[("selected", "#ffffff")],
    )

    for cv in canvases:
        cv.configure(bg=cores["fundo"])
        cv.master.configure(bg=cores["fundo"])

    for card, frame in cards_widgets:
        frame.configure(bg=cores["fundo"])
        card.configure(bg=cores["painel"], highlightbackground=cores["borda"])
        for sub in card.winfo_children():
            if isinstance(sub, tk.Label):
                if sub.cget("fg") in [
                    PALETA_CLARA["subtexto"],
                    PALETA_ESCURA["subtexto"],
                ]:
                    sub.configure(bg=cores["painel"], fg=cores["subtexto"])
                elif sub.cget("fg") in [
                    PALETA_CLARA["verde"],
                    PALETA_ESCURA["verde"],
                ]:
                    sub.configure(bg=cores["painel"], fg=cores["verde"])
                else:
                    sub.configure(bg=cores["painel"], fg=cores["texto"])
            elif isinstance(sub, tk.Spinbox):
                sub.configure(
                    bg=cores["fundo"],
                    fg=cores["texto"],
                    readonlybackground=cores["fundo"],
                    buttonbackground=cores["painel"],
                )


def _ao_rolar_mouse(event, canvas):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


janela = tk.Tk()
janela.title("Trattoria & Pastificio Italiano - Cardápio Digital")
janela.geometry("780x700")
janela.configure(bg=cores["fundo"])

style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background=cores["fundo"], borderwidth=0)
style.configure(
    "TNotebook.Tab",
    background=cores["painel"],
    foreground=cores["texto"],
    padding=[10, 5],
)
style.map(
    "TNotebook.Tab",
    background=[("selected", cores["primaria"])],
    foreground=[("selected", "#ffffff")],
)

bar_topo = tk.Frame(janela, bg=cores["fundo"])
bar_topo.pack(fill="x", padx=15, pady=10)

lbl_titulo_app = tk.Label(
    bar_topo,
    text="🍝 Trattoria & Pastificio Italiano",
    font=("Arial", 16, "bold"),
    bg=cores["fundo"],
    fg=cores["texto"],
)
lbl_titulo_app.pack(side="left")

btn_tema = tk.Button(
    bar_topo,
    text="🌙 Modo Escuro",
    bg=cores["amarelo"],
    fg="black",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    command=alternar_tema,
)
btn_tema.pack(side="right")

notebook = ttk.Notebook(janela)
notebook.pack(fill="both", expand=True, padx=15, pady=(0, 10))

for categoria, itens in CARDAPIO.items():
    frame_aba = tk.Frame(notebook, bg=cores["fundo"])
    notebook.add(frame_aba, text=categoria)

    canvas = tk.Canvas(frame_aba, bg=cores["fundo"], highlightthickness=0)
    scrollbar = ttk.Scrollbar(
        frame_aba, orient="vertical", command=canvas.yview
    )
    frame_itens = tk.Frame(canvas, bg=cores["fundo"])

    def _ajustar_largura(e, c=canvas, f=frame_itens):
        c.itemconfig(c.find_withtag("win")[0], width=e.width)

    frame_itens.bind(
        "<Configure>",
        lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")),
    )
    win_id = canvas.create_window(
        (0, 0), window=frame_itens, anchor="nw", tags="win"
    )
    canvas.bind("<Configure>", _ajustar_largura)

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    canvases.append(canvas)

    frame_itens.bind_all(
        "<MouseWheel>", lambda e, c=canvas: _ao_rolar_mouse(e, c)
    )

    for item in itens:
        var_qtd = tk.IntVar(value=0)
        qtd_variaveis[item["id"]] = var_qtd

        card = tk.Frame(
            frame_itens,
            bg=cores["painel"],
            bd=1,
            relief="solid",
            highlightbackground=cores["borda"],
        )
        card.pack(fill="x", pady=5, ipady=4, ipadx=6, expand=True)
        card.columnconfigure(0, weight=1)

        cards_widgets.append((card, frame_itens))

        lbl_nome = tk.Label(
            card,
            text=item["nome"],
            font=("Arial", 11, "bold"),
            fg=cores["texto"],
            bg=cores["painel"],
        )
        lbl_nome.grid(row=0, column=0, sticky="w", padx=8, pady=(4, 0))

        lbl_desc = tk.Label(
            card,
            text=item["desc"],
            font=("Arial", 8),
            fg=cores["subtexto"],
            bg=cores["painel"],
            wraplength=420,
            justify="left",
        )
        lbl_desc.grid(row=1, column=0, sticky="w", padx=8, pady=(0, 4))

        lbl_preco = tk.Label(
            card,
            text=f"R$ {item['preco']:.2f}",
            font=("Arial", 11, "bold"),
            fg=cores["verde"],
            bg=cores["painel"],
        )
        lbl_preco.grid(row=0, column=1, rowspan=2, padx=10)

        spn_qtd = tk.Spinbox(
            card,
            from_=0,
            to=20,
            width=3,
            textvariable=var_qtd,
            font=("Arial", 10),
            command=calcular_total,
            state="readonly",
            readonlybackground=cores["fundo"],
        )
        spn_qtd.grid(row=0, column=2, rowspan=2, padx=8)

frame_rodape = tk.Frame(janela, bg=cores["painel"], bd=1, relief="raised")
frame_rodape.pack(fill="x", ipady=8, ipadx=10)

lbl_total_texto = tk.Label(
    frame_rodape,
    text="Total do Pedido:",
    font=("Arial", 11, "bold"),
    bg=cores["painel"],
    fg=cores["texto"],
)
lbl_total_texto.pack(side="left", padx=(15, 5))

lbl_total_valor = tk.Label(
    frame_rodape,
    text="R$ 0.00",
    font=("Arial", 14, "bold"),
    bg=cores["painel"],
    fg=cores["primaria"],
)
lbl_total_valor.pack(side="left")

btn_finalizar = tk.Button(
    frame_rodape,
    text="🛒 Exportar Pedido (JSON)",
    bg=cores["verde"],
    fg="white",
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    command=finalizar_pedido_json,
)
btn_finalizar.pack(side="right", padx=15)

btn_limpar = tk.Button(
    frame_rodape,
    text="🗑️ Limpar",
    bg=cores["vermelho"],
    fg="white",
    font=("Arial", 9, "bold"),
    relief="flat",
    cursor="hand2",
    command=zerar_quantidades,
)
btn_limpar.pack(side="right", padx=5)

janela.mainloop()