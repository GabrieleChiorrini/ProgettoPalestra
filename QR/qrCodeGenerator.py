import qrcode

# Configurazione del codice QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Inserimento del testo richiesto
data = input("Dato di cui generare il codice QR: ")
qr.add_data(data)
qr.make(fit=True)

# Creazione dell'immagine (QR nero su sfondo bianco)
img = qr.make_image(fill_color="black", back_color="white")

# Salvataggio del file sul computer
img.save("QR/qrcode_" + data +".png")
print(f"Codice QR generato con successo e salvato come 'qrcode_{data}.png'")