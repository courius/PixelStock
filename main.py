# main.py
# Name: Sandu Stati Suman
# Description: Main module for Murphy's General Store Inventory System.
#              Full GUI implementation using customtkinter.
#              All operations are handled via GUI forms and screens.

"""
Main programme module for inventory management system.

This programme uses the Product and Inventory classes to manage Murphy's
General Store inventory with proper object-oriented design.
Transactions remain as a simple list (not a class).
The entire user interface is built with customtkinter — no terminal prompts.
"""

# =============================================================================
# IMPORTS
# =============================================================================
from datetime import datetime
from customtkinter import *
from PIL import Image

import data_handler
import transaction_operations


# =============================================================================
# COLOUR & STYLE CONSTANTS
# =============================================================================
BG_BEIGE       = "#E7CEA8"   # left panel / window background tint
DARK_PURPLE    = "#473E6D"   # accent colour for titles, buttons
SCREEN_BG      = "#FDFAF4"   # main display area background
ERROR_RED      = "#B00020"   # validation error messages
SUCCESS_GREEN  = "#2E6B3E"   # success messages
WARN_AMBER     = "#7A4F00"   # warning / low-stock colour
FORM_BG        = "#FDFAF4"   # form overlay background


# =============================================================================
# MAIN
# =============================================================================

def main():

    # -------------------------------------------------------------------------
    # APP WINDOW
    # -------------------------------------------------------------------------
    app = CTk()
    app.geometry("1000x620")
    set_appearance_mode("light")
    app.resizable(False, False)
    app.title("SSS's General Store — Inventory Manager")
    app.configure(fg_color=BG_BEIGE)

    # Fonts
    pixel_font   = CTkFont(family="Mini Pixel-7",  size=30)
    screen_font  = CTkFont(family="Courier",     size=15)
    label_font   = CTkFont(family="Pixelon",     size=14, weight="bold")
    small_font   = CTkFont(family="Pixelon",     size=14)
    stat_font    = CTkFont(family="Pixel Emulator",   size=16, weight="bold")
    entry_font   = CTkFont(family="Pixelon",     size=14)

    # -------------------------------------------------------------------------
    # BACKGROUND IMAGE  (graceful fallback if not found)
    # -------------------------------------------------------------------------
    try:
        bg_img  = Image.open("ASSETS/bg.png")
        bg_ctk  = CTkImage(light_image=bg_img, size=(1000, 620))
        bg_lbl  = CTkLabel(master=app, image=bg_ctk, text="")
        bg_lbl.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        pass   # run without background image

    # -------------------------------------------------------------------------
    # LOAD DATA  (before building widgets that reference inventory)
    # -------------------------------------------------------------------------
    _inv_msg,   inventory    = data_handler.load_inventory("inventory.json")
    _trans_msg, transactions = data_handler.load_transactions("transactions.json")

    # =========================================================================
    # LOGIN SCREEN  — shown first, covers the whole window
    # =========================================================================
    VALID_USERNAME = "iamtheuser"
    VALID_PASSWORD = "1234"

    login_overlay = CTkFrame(master=app, width=1000, height=620,
                             fg_color=BG_BEIGE, corner_radius=0)
    login_overlay.place(x=0, y=0)

    login_card = CTkFrame(master=login_overlay, width=420, height=460,
                          fg_color=FORM_BG, corner_radius=10)
    login_card.place(relx=0.5, rely=0.5, anchor="center")

    CTkLabel(login_card, text="SSS's General Store",
             font=pixel_font, text_color=DARK_PURPLE,
             fg_color="transparent").place(relx=0.5, y=40, anchor="center")
    CTkLabel(login_card, text="Inventory Manager — Sign In",
             font=label_font, text_color=DARK_PURPLE,
             fg_color="transparent").place(relx=0.5, y=68, anchor="center")

    # User account image frame (placeholder circle; swap in your own image)
    avatar_frame = CTkFrame(login_card, width=140, height=140,
                            fg_color="transparent", corner_radius=55)
    avatar_frame.place(relx=0.5, y=160, anchor="center")

    try:
        avatar_img = Image.open("ASSETS/user_avatar.png")
        avatar_ctk = CTkImage(light_image=avatar_img, size=(140, 140))
        CTkLabel(avatar_frame, image=avatar_ctk, text="",
                 fg_color="transparent").place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        # Fallback placeholder if no avatar image is supplied yet
        CTkLabel(avatar_frame, text="👤", font=CTkFont(size=40),
                 text_color=DARK_PURPLE, fg_color="transparent"
                 ).place(relx=0.5, rely=0.5, anchor="center")

    ent_login_user = CTkEntry(login_card, placeholder_text="Username  (iamtheuser)", width=300, font=entry_font)
    ent_login_user.place(relx=0.5, y=270, anchor="center")

    ent_login_pass = CTkEntry(login_card, placeholder_text="Password  (1234)", width=300, show="•", font=entry_font)
    ent_login_pass.place(relx=0.5, y=315, anchor="center")

    var_login_status = StringVar()
    CTkLabel(login_card, textvariable=var_login_status, font=small_font,
             text_color=ERROR_RED, fg_color="transparent"
             ).place(relx=0.5, y=350, anchor="center")

    def attempt_login(event=None):
        user = ent_login_user.get().strip()
        pwd  = ent_login_pass.get().strip()
        if user == VALID_USERNAME and pwd == VALID_PASSWORD:
            login_overlay.place_forget()
        else:
            var_login_status.set("Incorrect username or password.")
            ent_login_pass.delete(0, "end")

    CTkButton(login_card, text="Log In", width=160, height=36,
              fg_color=DARK_PURPLE, hover_color="#6B5FA0",
              font=label_font, command=attempt_login
              ).place(relx=0.5, y=400, anchor="center")

    ent_login_user.bind("<Return>", attempt_login)
    ent_login_pass.bind("<Return>", attempt_login)

    # =========================================================================
    # SAVING / SAVED SCREEN  — shown when the user clicks Save & Exit
    # =========================================================================
    saving_overlay = CTkFrame(master=app, width=1000, height=620,
                              fg_color=BG_BEIGE, corner_radius=0)
    # not placed yet — only shown when Save & Exit is clicked

    saving_card = CTkFrame(master=saving_overlay, width=420, height=220,
                           fg_color=FORM_BG, corner_radius=10)
    saving_card.place(relx=0.5, rely=0.5, anchor="center")

    var_saving_status = StringVar(value="Saving...")
    CTkLabel(saving_card, textvariable=var_saving_status,
             font=pixel_font, text_color=DARK_PURPLE,
             fg_color="transparent").place(relx=0.5, rely=0.45, anchor="center")

    saving_spinner = CTkProgressBar(saving_card, width=260, mode="indeterminate")
    saving_spinner.place(relx=0.5, rely=0.65, anchor="center")

    def run_save_and_exit():
        """Show the Saving overlay, save data, flip to Saved, then close."""
        saving_overlay.place(x=0, y=0)
        saving_overlay.lift()
        var_saving_status.set("Saving...")
        saving_spinner.set(0)
        saving_spinner.start()
        app.update()  # force the "Saving..." frame to render before we block on I/O

        data_handler.save_inventory(inventory, "inventory.json")
        data_handler.save_transactions(transactions, "transactions.json")

        saving_spinner.stop()
        saving_spinner.set(1)
        var_saving_status.set("Saved ✓")

        app.after(1500, app.destroy)

    # =========================================================================
    # TOP BAR  — live stats (top-right)
    # =========================================================================
    top_bar = CTkFrame(master=app, width=500, height=60,
                       fg_color=BG_BEIGE, bg_color=BG_BEIGE, corner_radius=0)
    top_bar.place(x=470, y=30)

    # Stat boxes (top-left area)
    stats_frame = CTkFrame(top_bar, fg_color=BG_BEIGE, bg_color=BG_BEIGE, corner_radius=0)
    stats_frame.place(x=0, y=4)

    var_total_value    = StringVar(value="Total Value:  €0.00")
    var_total_products = StringVar(value="Products:  0")

    lbl_value = CTkLabel(stats_frame, textvariable=var_total_value,
                         font=stat_font, text_color="#442E65", 
                         fg_color="#D4B88A", corner_radius=6,
                         padx=10, pady=12)
    lbl_value.grid(row=0, column=0, padx=(0, 12))

    lbl_count = CTkLabel(stats_frame, textvariable=var_total_products,
                         font=stat_font, text_color="#442E65",
                         fg_color="#D4B88A", corner_radius=4,
                         padx=10, pady=12)
    lbl_count.grid(row=0, column=1)

    def refresh_stats():
        """Recalculate and update top-bar stats."""
        total_val  = inventory.calculate_total_value()
        total_prod = len(inventory)
        var_total_value.set(f"Total Value:  €{total_val:,.2f}")
        var_total_products.set(f"Products:  {total_prod}")

    refresh_stats()

    # =========================================================================
    # LEFT SIDE PANEL  — navigation buttons
    # =========================================================================
    left_panel = CTkFrame(master=app, width=200, height=460,
                          fg_color=BG_BEIGE, bg_color=BG_BEIGE, corner_radius=8)
    left_panel.place(x=37, y=82)

    # Plain coloured buttons, no image assets required.
    BTN_W = 190

    def _nav_btn(parent, text, cmd, y):
        CTkButton(
            master=parent, text=text, command=cmd,
            width=BTN_W, height=36,
            fg_color=DARK_PURPLE, hover_color="#6B5FA0",
            text_color="#FFFFFF", font=label_font,
            corner_radius=6
        ).place(x=10, y=y)

    # =========================================================================
    # CENTRAL DISPLAY SCREEN
    # =========================================================================
    SCREEN_X, SCREEN_Y, SCREEN_W, SCREEN_H = 265, 90, 700, 440

    display_screen = CTkTextbox(
        master=app,
        width=SCREEN_W, height=SCREEN_H,
        font=screen_font,
        fg_color=SCREEN_BG,
        text_color=DARK_PURPLE,
        corner_radius=6
    )
    display_screen.place(x=SCREEN_X, y=SCREEN_Y)
    display_screen.configure(state="disabled")

    # Active overlay frame (one at a time)
    _active_form = [None]

    def _hide_form():
        if _active_form[0] is not None:
            _active_form[0].place_forget()
            _active_form[0] = None

    def output(text, clear=True):
        """Write text to the central display screen."""
        _hide_form()
        display_screen.configure(state="normal")
        if clear:
            display_screen.delete("1.0", "end")
        display_screen.insert("end", text + "\n")
        display_screen.configure(state="disabled")

    def _show_form(frame):
        """Place a form frame exactly over the display screen."""
        _hide_form()
        frame.place(x=SCREEN_X, y=SCREEN_Y)
        _active_form[0] = frame

    # Helper: build a standard overlay form frame
    def _make_form_frame():
        return CTkFrame(master=app, width=SCREEN_W, height=SCREEN_H,
                        fg_color=FORM_BG, corner_radius=6)

    # Helper: form title label inside a frame
    def _form_title(frame, text):
        CTkLabel(frame, text=text, font=pixel_font,
                 text_color=DARK_PURPLE, fg_color="transparent"
                 ).place(relx=0.5, y=30, anchor="center")

    # Helper: labelled entry
    def _labelled_entry(frame, label_text, y, placeholder="", width=320, show=""):
        CTkLabel(frame, text=label_text, font=label_font,
                 text_color=DARK_PURPLE, fg_color="transparent"
                 ).place(x=60, y=y)
        e = CTkEntry(frame, placeholder_text=placeholder,
                     width=width, show=show, font=entry_font)
        e.place(x=60, y=y + 22)
        return e

    # Helper: status message label inside a form
    def _status_label(frame, y=420):
        var = StringVar()
        lbl = CTkLabel(frame, textvariable=var, font=small_font,
                       fg_color="transparent", text_color=ERROR_RED,
                       wraplength=600)
        lbl.place(relx=0.5, y=y, anchor="center")
        return var

    # Helper: cancel button
    def _cancel_btn(frame, y=430):
        CTkButton(frame, text="Cancel", width=100, height=30,
                  fg_color="#9E9E9E", hover_color="#757575",
                  font=label_font,
                  command=lambda: output("Operation cancelled.")
                  ).place(relx=0.38, y=y, anchor="center")

    # =========================================================================
    # WELCOME SCREEN
    # =========================================================================
    welcome = (
        "=" * 66 + "\n"
        "         Welcome to SSS's General Store\n"
        "                 Inventory Manager\n"
        "=" * 66 + "\n\n"
        f"  {_inv_msg}\n"
        f"  {_trans_msg}\n\n"
        "  Use the buttons on the left to manage your inventory.\n"
    )

    # Shown once the window has finished laying out, so the textbox
    # doesn't insert the welcome text more than once while still settling.
    _welcome_shown = [False]

    def _show_welcome_once():
        if not _welcome_shown[0]:
            _welcome_shown[0] = True
            output(welcome)

    app.after(150, _show_welcome_once)

    # =========================================================================
    # 1. VIEW ALL PRODUCTS
    # =========================================================================
    def handle_view_products():
        products = inventory.get_all_products()
        if not products:
            output("No products in inventory.")
            return
        lines  = "--- All Products ---\n\n"
        lines += f"{'ID':<7} {'Product':<20} {'Category':<14} {'Price':>8}  {'Stock':>6}  {'Min':>5}\n"
        lines += "─" * 69 + "\n"
        for p in products:
            low_marker = " ⚠" if p.is_low_stock() else ""
            lines += (f"{p.product_id:<7} {p.name:<20} {p.category:<14} "
                      f"€{p.price:>7.2f}  {p.quantity:>6}  {p.min_stock:>5}{low_marker}\n")
        lines += "─" * 69 + "\n"
        lines += f"  Total products: {len(inventory)}\n"
        lines += f"  Total value:    €{inventory.calculate_total_value():,.2f}\n"
        output(lines)

    # =========================================================================
    # 2. ADD NEW PRODUCT
    # =========================================================================
    frm_add = _make_form_frame()
    _form_title(frm_add, "Add New Product")

    ent_add_name     = _labelled_entry(frm_add, "Product Name",         45,  "e.g. Butter")
    ent_add_cat      = _labelled_entry(frm_add, "Category",            105,  "e.g. Dairy")
    ent_add_price    = _labelled_entry(frm_add, "Price (€)",           165,  "e.g. 1.99")
    ent_add_qty      = _labelled_entry(frm_add, "Current Quantity",    225,  "e.g. 50")
    ent_add_min      = _labelled_entry(frm_add, "Minimum Stock Level", 285,  "e.g. 20")
    var_add_status   = _status_label(frm_add, y=410)

    def _clear_add_form():
        for e in (ent_add_name, ent_add_cat, ent_add_price, ent_add_qty, ent_add_min):
            e.delete(0, "end")
        var_add_status.set("")

    def submit_add_product():
        name     = ent_add_name.get().strip()
        category = ent_add_cat.get().strip()
        if not name or not category:
            var_add_status.set("Error: Name and Category cannot be empty.")
            return
        if inventory.find_by_name(name) is not None:
            var_add_status.set(f"Error: '{name}' already exists in inventory.")
            return
        try:
            price     = float(ent_add_price.get())
            qty       = int(ent_add_qty.get())
            min_stock = int(ent_add_min.get())
        except ValueError:
            var_add_status.set("Error: Price, Quantity and Min Stock must be valid numbers.")
            return
        if price < 0.01:
            var_add_status.set("Error: Price must be at least €0.01.")
            return
        if qty < 0 or min_stock < 0:
            var_add_status.set("Error: Quantity and Min Stock cannot be negative.")
            return

        product_id = inventory.add_product(name, category, price, qty, min_stock)
        transaction_operations.log_transaction(transactions, "added", product_id, name, qty)
        refresh_stats()
        _clear_add_form()
        output(f"✓ Product '{name}' added successfully!\n\n"
               f"  Assigned ID:  {product_id}\n"
               f"  Category:     {category}\n"
               f"  Price:        €{price:.2f}\n"
               f"  Quantity:     {qty}\n"
               f"  Min Stock:    {min_stock}\n")

    CTkButton(frm_add, text="Add Product", width=140, height=34,
              fg_color=DARK_PURPLE, hover_color="#6B5FA0",
              font=label_font, command=submit_add_product
              ).place(relx=0.62, y=375, anchor="center")
    _cancel_btn(frm_add, y=375)

    def show_add_form():
        _clear_add_form()
        _show_form(frm_add)

    # =========================================================================
    # 3. UPDATE STOCK  (Sale / Delivery)
    # =========================================================================
    frm_stock = _make_form_frame()
    _form_title(frm_stock, "Update Stock")

    ent_stock_name = _labelled_entry(frm_stock, "Product Name (press ENTER to see details)", 60, "exact name")
    var_stock_info = StringVar()
    CTkLabel(frm_stock, textvariable=var_stock_info, font=small_font,
             fg_color="transparent", text_color="#555555"
             ).place(x=60, y=112)

    CTkLabel(frm_stock, text="Transaction Type", font=label_font,
             text_color=DARK_PURPLE, fg_color="transparent").place(x=60, y=150)
    var_trans_type = StringVar(value="sale")
    CTkRadioButton(frm_stock, text="Sale  (stock goes down)",
                   variable=var_trans_type, value="sale",
                   font=small_font, text_color=DARK_PURPLE
                   ).place(x=70, y=178)
    CTkRadioButton(frm_stock, text="Delivery  (stock comes in)",
                   variable=var_trans_type, value="delivery",
                   font=small_font, text_color=DARK_PURPLE
                   ).place(x=70, y=208)

    ent_stock_qty = _labelled_entry(frm_stock, "Quantity", 265, "e.g. 10")
    var_stock_status = _status_label(frm_stock, y=410)

    def _lookup_stock_product(*_):
        name = ent_stock_name.get().strip()
        if not name:
            var_stock_info.set("")
            return
        pid  = inventory.find_by_name(name)
        if pid:
            p = inventory.get_product(pid)
            var_stock_info.set(f"  Found: {p.product_id}  |  Current stock: {p.quantity}  |  Min: {p.min_stock}")
        else:
            var_stock_info.set("  Product does not exist.")

    ent_stock_name.bind("<FocusOut>", _lookup_stock_product)
    ent_stock_name.bind("<Return>",   _lookup_stock_product)

    def submit_update_stock():
        name = ent_stock_name.get().strip()
        pid  = inventory.find_by_name(name)
        if pid is None:
            var_stock_status.set(f"Error: '{name}' not found in inventory.")
            return
        try:
            qty = int(ent_stock_qty.get())
        except ValueError:
            var_stock_status.set("Error: Quantity must be a whole number.")
            return
        if qty < 1:
            var_stock_status.set("Error: Quantity must be at least 1.")
            return

        product    = inventory.get_product(pid)
        trans_type = var_trans_type.get()
        change     = -qty if trans_type == "sale" else qty

        try:
            product.update_stock(change)
        except ValueError as e:
            var_stock_status.set(f"Error: {e}")
            return

        transaction_operations.log_transaction(transactions, trans_type, pid, product.name, change)
        refresh_stats()
        ent_stock_name.delete(0, "end")
        ent_stock_qty.delete(0, "end")
        var_stock_info.set("")
        var_stock_status.set("")

        action = "sold" if trans_type == "sale" else "delivered"
        output(f"✓ Stock updated!\n\n"
               f"  Product:     {product.name}  ({pid})\n"
               f"  Action:      {qty} unit(s) {action}\n"
               f"  New Stock:   {product.quantity}\n"
               + ("  ⚠ Warning: Stock is below minimum!\n" if product.is_low_stock() else ""))

    CTkButton(frm_stock, text="Update Stock", width=140, height=34,
              fg_color=DARK_PURPLE, hover_color="#6B5FA0",
              font=label_font, command=submit_update_stock
              ).place(relx=0.62, y=375, anchor="center")
    _cancel_btn(frm_stock, y=375)

    def show_stock_form():
        ent_stock_name.delete(0, "end")
        ent_stock_qty.delete(0, "end")
        var_stock_info.set("")
        var_stock_status.set("")
        _show_form(frm_stock)

    # =========================================================================
    # 4. UPDATE PRODUCT DETAILS
    # =========================================================================
    frm_upd = _make_form_frame()
    _form_title(frm_upd, "Update Product Details")

    ent_upd_name = _labelled_entry(frm_upd, "Product Name (press ENTER to see details)", 70, "exact name")
    var_upd_current = StringVar()
    CTkLabel(frm_upd, textvariable=var_upd_current, font=small_font,
             text_color="#555555", fg_color="transparent",
             wraplength=580).place(x=60, y=122)

    CTkLabel(frm_upd, text="Field to Update", font=label_font,
             text_color=DARK_PURPLE, fg_color="transparent").place(x=60, y=160)
    var_upd_field = StringVar(value="name")
    fields = [("Name", "name"), ("Category", "category"),
              ("Price", "price"), ("Min Stock", "min_stock")]
    for i, (label, val) in enumerate(fields):
        CTkRadioButton(frm_upd, text=label, variable=var_upd_field, value=val,
                       font=small_font, text_color=DARK_PURPLE
                       ).place(x=70 + i * 150, y=188)

    ent_upd_value = _labelled_entry(frm_upd, "New Value", 240, "enter new value")
    var_upd_status = _status_label(frm_upd, y=410)

    def _lookup_upd_product(*_):
        name = ent_upd_name.get().strip()
        if not name:
            var_upd_current.set("")
            return
        pid  = inventory.find_by_name(name)
        if pid:
            p = inventory.get_product(pid)
            var_upd_current.set(
                f"  Found: {p.product_id}  |  Category: {p.category}  |  "
                f"Price: €{p.price:.2f}  |  Min Stock: {p.min_stock}")
        else:
            var_upd_current.set("  Product does not exist.")

    ent_upd_name.bind("<FocusOut>", _lookup_upd_product)
    ent_upd_name.bind("<Return>",   _lookup_upd_product)

    def submit_update_details():
        name  = ent_upd_name.get().strip()
        pid   = inventory.find_by_name(name)
        if pid is None:
            var_upd_status.set(f"Error: '{name}' not found.")
            return
        product   = inventory.get_product(pid)
        field     = var_upd_field.get()
        new_raw   = ent_upd_value.get().strip()
        if not new_raw:
            var_upd_status.set("Error: New value cannot be empty.")
            return
        try:
            if field == "name":
                if inventory.find_by_name(new_raw) is not None:
                    var_upd_status.set(f"Error: A product named '{new_raw}' already exists.")
                    return
                product.name = new_raw
                display_val = new_raw
            elif field == "category":
                product.category = new_raw
                display_val = new_raw
            elif field == "price":
                price = float(new_raw)
                if price < 0.01:
                    var_upd_status.set("Error: Price must be at least €0.01.")
                    return
                product.price = price
                display_val = f"€{price:.2f}"
            elif field == "min_stock":
                ms = int(new_raw)
                if ms < 0:
                    var_upd_status.set("Error: Min stock cannot be negative.")
                    return
                product.min_stock = ms
                display_val = str(ms)
        except ValueError as e:
            var_upd_status.set(f"Error: {e}")
            return

        refresh_stats()
        ent_upd_name.delete(0, "end")
        ent_upd_value.delete(0, "end")
        var_upd_current.set("")
        var_upd_status.set("")
        output(f"✓ Product updated!\n\n"
               f"  Product:  {product.name}  ({pid})\n"
               f"  Field:    {field.replace('_', ' ').title()}\n"
               f"  New value: {display_val}\n")

    CTkButton(frm_upd, text="Save Changes", width=140, height=34,
              fg_color=DARK_PURPLE, hover_color="#6B5FA0",
              font=label_font, command=submit_update_details
              ).place(relx=0.62, y=375, anchor="center")
    _cancel_btn(frm_upd, y=375)

    def show_update_form():
        ent_upd_name.delete(0, "end")
        ent_upd_value.delete(0, "end")
        var_upd_current.set("")
        var_upd_status.set("")
        _show_form(frm_upd)

    # =========================================================================
    # 5. REMOVE PRODUCT
    # =========================================================================
    frm_remove = _make_form_frame()
    _form_title(frm_remove, "Remove Product")

    ent_rm_name = _labelled_entry(frm_remove, "Product Name (press ENTER to see details)", 80, "exact name")
    var_rm_info = StringVar()
    CTkLabel(frm_remove, textvariable=var_rm_info, font=small_font,
             fg_color="transparent", text_color="#555555"
             ).place(x=60, y=132)

    CTkLabel(frm_remove,
             text="⚠  This action cannot be undone.",
             font=label_font, text_color=WARN_AMBER,
             fg_color="transparent").place(x=60, y=170)

    var_rm_status = _status_label(frm_remove, y=340)

    # --- NEW CONFIRMATION UI ELEMENTS ---
    lbl_confirm = CTkLabel(frm_remove, text="Are you sure?", font=label_font, text_color=ERROR_RED, fg_color="transparent")
    btn_confirm_yes = CTkButton(frm_remove, text="YES", width=50, height=28, fg_color=ERROR_RED, hover_color="#7F0015", font=label_font)
    btn_confirm_no = CTkButton(frm_remove, text="NO", width=50, height=28, fg_color="#9E9E9E", hover_color="#757575", font=label_font)

    def hide_confirmation():
        lbl_confirm.place_forget()
        btn_confirm_yes.place_forget()
        btn_confirm_no.place_forget()

    def _lookup_rm_product(*_):
        name = ent_rm_name.get().strip()
        if not name:
            var_rm_info.set("")
            hide_confirmation()
            return
        pid  = inventory.find_by_name(name)
        if pid:
            p = inventory.get_product(pid)
            var_rm_info.set(
                f"  Found: {p.product_id}  |  {p.category}  |  "
                f"€{p.price:.2f}  |  Stock: {p.quantity}")
        else:
            var_rm_info.set("  Product does not exist.")
        hide_confirmation()

    ent_rm_name.bind("<FocusOut>", _lookup_rm_product)
    ent_rm_name.bind("<Return>",   _lookup_rm_product)

    def execute_remove():
        name = ent_rm_name.get().strip()
        pid  = inventory.find_by_name(name)
        if pid is None:
            return
        removed = inventory.remove_product(pid)
        if removed:
            transaction_operations.log_transaction(
                transactions, "removed", pid, removed.name, 0)
            refresh_stats()
            ent_rm_name.delete(0, "end")
            var_rm_info.set("")
            var_rm_status.set("")
            hide_confirmation()
            output(f"✓ Product removed.\n\n"
                   f"  Name:       {removed.name}\n"
                   f"  ID:         {pid}\n"
                   f"  Category:   {removed.category}\n")

    btn_confirm_yes.configure(command=execute_remove)
    btn_confirm_no.configure(command=hide_confirmation)

    def submit_remove():
        name = ent_rm_name.get().strip()
        pid  = inventory.find_by_name(name)
        if pid is None:
            var_rm_status.set(f"Error: '{name}' not found in inventory.")
            hide_confirmation()
            return
        
        # Show confirmation instead of removing immediately
        var_rm_status.set("")
        lbl_confirm.place(relx=0.43, y=300, anchor="e")
        btn_confirm_yes.place(relx=0.49, y=300, anchor="center")
        btn_confirm_no.place(relx=0.58, y=300, anchor="center")

    CTkButton(frm_remove, text="Remove Product", width=150, height=34,
              fg_color="#B00020", hover_color="#7F0015",
              font=label_font, command=submit_remove
              ).place(relx=0.62, y=375, anchor="center")
    _cancel_btn(frm_remove, y=375)

    def show_remove_form():
        ent_rm_name.delete(0, "end")
        var_rm_info.set("")
        var_rm_status.set("")
        hide_confirmation()
        _show_form(frm_remove)

    # =========================================================================
    # 6. SEARCH PRODUCTS
    # =========================================================================
    frm_search = _make_form_frame()
    _form_title(frm_search, "Search Products")

    CTkLabel(frm_search, text="Search By", font=label_font,
             text_color=DARK_PURPLE, fg_color="transparent").place(x=60, y=70)
    var_search_type = StringVar(value="name")
    CTkRadioButton(frm_search, text="Name (partial match)",
                   variable=var_search_type, value="name",
                   font=small_font, text_color=DARK_PURPLE).place(x=70, y=100)
    CTkRadioButton(frm_search, text="Category (exact)",
                   variable=var_search_type, value="category",
                   font=small_font, text_color=DARK_PURPLE).place(x=70, y=130)

    ent_search_term = _labelled_entry(frm_search, "Search Term", 185, "enter term...")
    var_search_status = _status_label(frm_search, y=340)

    def submit_search():
        term = ent_search_term.get().strip()
        if not term:
            var_search_status.set("Error: Search term cannot be empty.")
            return
        if var_search_type.get() == "name":
            results = inventory.search_by_name(term)
            mode    = f"name containing '{term}'"
        else:
            results = inventory.search_by_category(term)
            mode    = f"category '{term}'"

        if not results:
            output(f"No products found matching {mode}.")
            return

        lines  = f"--- Search Results: {mode} ---\n\n"
        lines += f"{'ID':<7} {'Product':<20} {'Category':<14} {'Price':>8}  {'Stock':>6}\n"
        lines += "─" * 60 + "\n"
        for p in results:
            lines += (f"{p.product_id:<7} {p.name:<20} {p.category:<14} "
                      f"€{p.price:>7.2f}  {p.quantity:>6}\n")
        lines += "─" * 60 + "\n"
        lines += f"  {len(results)} product(s) found.\n"
        output(lines)

    CTkButton(frm_search, text="Search", width=120, height=34,
              fg_color=DARK_PURPLE, hover_color="#6B5FA0",
              font=label_font, command=submit_search
              ).place(relx=0.62, y=375, anchor="center")
    _cancel_btn(frm_search, y=375)

    def show_search_form():
        ent_search_term.delete(0, "end")
        var_search_status.set("")
        _show_form(frm_search)

    # =========================================================================
    # 7. LOW STOCK ALERTS
    # =========================================================================
    def handle_low_stock():
        low = inventory.get_low_stock_products()
        if len(inventory) == 0:
            output("No products in inventory.")
            return
        if not low:
            output("✓ All products are adequately stocked.")
            return
        lines  = f"--- Low Stock Alerts ({len(low)} item(s)) ---\n\n"
        lines += f"{'ID':<7} {'Product':<20} {'Category':<14} {'Current':>8}  {'Min':>6}  {'Order':>6}\n"
        lines += "─" * 68 + "\n"
        for p in low:
            order_qty = p.min_stock - p.quantity + 5
            lines += (f"{p.product_id:<7} {p.name:<20} {p.category:<14} "
                      f"{p.quantity:>8}  {p.min_stock:>6}  {order_qty:>6}\n")
        lines += "─" * 68 + "\n"
        lines += "  'Order' = suggested reorder quantity (to min + 5).\n"
        output(lines)

    # =========================================================================
    # 8. CATEGORY REPORT
    # =========================================================================
    frm_category = _make_form_frame()
    _form_title(frm_category, "Category Report")

    CTkLabel(frm_category, text="Report Scope", font=label_font,
             text_color=DARK_PURPLE, fg_color="transparent").place(x=60, y=70)
    var_category_scope = StringVar(value="all")
    CTkRadioButton(frm_category, text="All categories",
                   variable=var_category_scope, value="all",
                   font=small_font, text_color=DARK_PURPLE).place(x=70, y=100)
    CTkRadioButton(frm_category, text="One category",
                   variable=var_category_scope, value="one",
                   font=small_font, text_color=DARK_PURPLE).place(x=70, y=130)

    ent_category_name = _labelled_entry(frm_category, "Category Name", 185, "e.g. Dairy")
    var_category_status = _status_label(frm_category, y=340)

    def submit_category_report():
        report = inventory.generate_category_report()
        if not report:
            output("No products in inventory.")
            return

        if var_category_scope.get() == "one":
            name = ent_category_name.get().strip()
            if not name:
                var_category_status.set("Error: Enter a category name.")
                return
            match = next((c for c in report if c.lower() == name.lower()), None)
            if match is None:
                var_category_status.set(f"Error: Category '{name}' not found.")
                return
            report = {match: report[match]}

        lines  = "--- Category Report ---\n\n"
        lines += f"{'Category':<20} {'Count':>6}  {'Total Value':>13}\n"
        lines += "─" * 44 + "\n"
        total_p = 0
        total_v = 0.0
        for cat, stats in sorted(report.items()):
            lines += f"{cat:<20} {stats['count']:>6}  €{stats['value']:>12.2f}\n"
            total_p += stats['count']
            total_v += stats['value']
        lines += "─" * 44 + "\n"
        lines += f"{'TOTAL':<20} {total_p:>6}  €{total_v:>12.2f}\n"
        output(lines)

    CTkButton(frm_category, text="Generate", width=140, height=34,
              fg_color=DARK_PURPLE, hover_color="#6B5FA0",
              font=label_font, command=submit_category_report
              ).place(relx=0.62, y=375, anchor="center")
    _cancel_btn(frm_category, y=375)

    def show_category_form():
        ent_category_name.delete(0, "end")
        var_category_status.set("")
        _show_form(frm_category)

    # =========================================================================
    # 9. TRANSACTION LOG
    # =========================================================================
    frm_trans = _make_form_frame()
    _form_title(frm_trans, "Transaction Log")

    CTkLabel(frm_trans, text="Number of recent transactions to display:",
             font=label_font, text_color=DARK_PURPLE,
             fg_color="transparent").place(x=60, y=80)
    slider_var = IntVar(value=10)

    slider = CTkSlider(frm_trans, from_=5, to=50, number_of_steps=9,
                       variable=slider_var, width=340,
                       button_color=DARK_PURPLE, progress_color=DARK_PURPLE)
    slider.place(x=60, y=115)

    var_slider_lbl = StringVar(value="10")
    def _update_slider_lbl(val):
        var_slider_lbl.set(str(int(float(val))))
    slider.configure(command=_update_slider_lbl)

    CTkLabel(frm_trans, textvariable=var_slider_lbl, font=label_font,
             text_color=DARK_PURPLE, fg_color="transparent").place(x=410, y=108)

    def submit_trans_log():
        num = slider_var.get()
        if not transactions:
            output("No transactions recorded yet.")
            return
        recent = list(reversed(transactions[-num:]))
        lines  = f"--- Transaction Log (last {len(recent)}) ---\n\n"
        lines += f"{'Date & Time':<18} {'Type':<12} {'Product':<20} {'ID':<7} {'Qty':>5}\n"
        lines += "─" * 67 + "\n"
        for t in recent:
            ts      = datetime.fromisoformat(t["timestamp"]).strftime("%Y-%m-%d %H:%M")
            qty_str = f"{t['quantity']:+d}" if t['quantity'] != 0 else "—"
            lines  += (f"{ts:<18} {t['type'].upper():<12} "
                       f"{t['product_name']:<20} {t['product_id']:<7} {qty_str:>5}\n")
        lines += "─" * 67 + "\n"
        output(lines)

    CTkButton(frm_trans, text="Show Log", width=130, height=34,
              fg_color=DARK_PURPLE, hover_color="#6B5FA0",
              font=label_font, command=submit_trans_log
              ).place(relx=0.62, y=375, anchor="center")
    _cancel_btn(frm_trans, y=375)

    def show_trans_form():
        _show_form(frm_trans)

    # =========================================================================
    # 10. EXPORT REPORTS
    # =========================================================================
    frm_export = _make_form_frame()
    _form_title(frm_export, "Export Reports")

    CTkLabel(frm_export, text="Files are saved in the programme folder.",
             font=small_font, text_color="#666666",
             fg_color="transparent").place(relx=0.5, y=70, anchor="center")

    var_export_status = StringVar()
    CTkLabel(frm_export, textvariable=var_export_status,
             font=small_font, fg_color="transparent",
             text_color=SUCCESS_GREEN, wraplength=580
             ).place(relx=0.5, y=420, anchor="center")

    def _do_export(kind):
        ts = datetime.now().strftime("%Y%m%d_%H%M")
        msgs = []
        if kind in ("csv", "all"):
            fn = f"inventory_{ts}.csv"
            if data_handler.export_inventory_to_csv(inventory, fn):
                msgs.append(f"  ✓ Inventory CSV  →  {fn}")
        if kind in ("lowstock", "all"):
            fn = f"low_stock_{ts}.csv"
            if data_handler.export_low_stock_to_csv(inventory, fn):
                msgs.append(f"  ✓ Low-Stock CSV  →  {fn}")
        if kind in ("txt", "all"):
            fn = f"inventory_report_{ts}.txt"
            if data_handler.generate_text_report(inventory, fn):
                msgs.append(f"  ✓ Text Report    →  {fn}")
        result = "\n".join(msgs) if msgs else "Export failed."
        output(f"--- Export Complete ---\n\n{result}\n")

    btn_y = 110
    btn_data = [
        ("Export Inventory to CSV",        lambda: _do_export("csv")),
        ("Export Low-Stock Report to CSV", lambda: _do_export("lowstock")),
        ("Generate Text Report (.txt)",    lambda: _do_export("txt")),
        ("Export All Reports",             lambda: _do_export("all")),
    ]
    for label, cmd in btn_data:
        CTkButton(frm_export, text=label, width=360, height=36,
                  fg_color=DARK_PURPLE, hover_color="#6B5FA0",
                  font=label_font, command=cmd
                  ).place(relx=0.5, y=btn_y, anchor="center")
        btn_y += 60

    _cancel_btn(frm_export, y=375)

    def show_export_form():
        var_export_status.set("")
        _show_form(frm_export)

    # =========================================================================
    # NAV BUTTONS  (left panel) — wired up now that handlers exist
    # =========================================================================
    nav_items = [
        ("📋  View Products",        handle_view_products),
        ("🆕  Add Product",           show_add_form),
        ("📦  Update Stock",          show_stock_form),
        ("✏️   Edit Product",          show_update_form),
        ("🗑️   Remove Product",        show_remove_form),
        ("🔍  Search",                show_search_form),
        ("⚠️   Low Stock Alerts",     handle_low_stock),
        ("📊  Category Report",       show_category_form),
        ("🧾  Transaction Log",       show_trans_form),
        ("💾  Export Reports",        show_export_form),
    ]
    for i, (label, cmd) in enumerate(nav_items):
        _nav_btn(left_panel, label, cmd, y=10 + i * 44)

    # =========================================================================
    # BOTTOM BAR  — load status (left) + Save & Exit (right)
    # =========================================================================
    var_load_status = StringVar(
        value=f"{len(inventory)}  items  loaded  from  inventory.json"
    )
    CTkLabel(
        master=app,
        textvariable=var_load_status,
        font=small_font,
        text_color=DARK_PURPLE,
        fg_color="transparent"
    ).place(x=35, y=552)

    var_load_transactions_status = StringVar(
        value=f"{len(transactions)}  transactions loaded  from  transactions.json"
    )

    CTkLabel(
        master=app,
        textvariable=var_load_transactions_status,
        font=small_font,
        text_color=DARK_PURPLE,
        fg_color="transparent"
    ).place(x=35, y=572)

    def handle_save_exit():
        run_save_and_exit()

    CTkButton(
        master=app,
        text="💾  Save & Exit",
        width=160, height=38,
        fg_color="#61568F", hover_color=DARK_PURPLE,
        text_color="white", font=label_font,
        border_color=DARK_PURPLE,
        border_width=2,
        command=handle_save_exit
    ).place(x=810, y=555)

    # =========================================================================
    # START
    # =========================================================================
    # Ensure the login screen sits on top of every menu widget built above it.
    login_overlay.lift()

    # --- NEW: Intercept OS close to remind user to save ---
    def on_closing():
        # If login screen is still visible, allow normal exit
        if login_overlay.winfo_ismapped():
            app.destroy()
        else:
            # Otherwise, warn them to save
            output("\n\n  ⚠ DON'T FORGET TO SAVE ANY CHANGES ⚠\n\n  Please use the '💾 Save & Exit' button.")
        
    app.protocol("WM_DELETE_WINDOW", on_closing)

    app.mainloop()


if __name__ == "__main__":
    main()