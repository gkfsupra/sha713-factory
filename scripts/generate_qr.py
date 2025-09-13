import qrcode
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Archivo fuente (ej. PDF firmado)")
    parser.add_argument("--output", required=True, help="Ruta de salida del PNG QR")
    args = parser.parse_args()

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(f"SHA-713 Proof :: {args.input}")
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img.save(args.output)


if __name__ == "__main__":
    main()

